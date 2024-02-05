import googleapiclient.discovery
import pandas as pd
import emoji
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def analyze_youtube_video(video_url):
    API_KEY = 'AIzaSyCea5u6xGUjuIT8t6qw3BBu75L8KesChdc'
    youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=API_KEY)

    # Extracting video ID from the URL
    video_id = video_url[-11:]

    # Getting the channelId of the video uploader
    video_response = youtube.videos().list(
        part='snippet',
        id=video_id
    ).execute()

    video_snippet = video_response['items'][0]['snippet']
    uploader_channel_id = video_snippet['channelId']

    # Fetch comments
    comments = []
    nextPageToken = None
    while len(comments) < 600:
        request = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=100,
            pageToken=nextPageToken
        )
        response = request.execute()
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            if comment['authorChannelId']['value'] != uploader_channel_id:
                comments.append(comment['textDisplay'])
        nextPageToken = response.get('nextPageToken')

        if not nextPageToken:
            break

    hyperlink_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    threshold_ratio = 0.65
    relevant_comments = []

    for comment_text in comments:
        # Remove HTML <br> tags
        comment_text = re.sub(r'<br\s*\/?>', ' ', comment_text)
        
        comment_text = comment_text.lower().strip()
        emojis = emoji.emoji_count(comment_text)
        text_characters = len(re.sub(r'\s', '', comment_text))
        if (any(char.isalnum() for char in comment_text)) and not hyperlink_pattern.search(comment_text):
            if emojis == 0 or (text_characters / (text_characters + emojis)) > threshold_ratio:
                relevant_comments.append(comment_text)

    # Sentiment Analysis
    polarity = []
    positive_comments = []
    negative_comments = []
    neutral_comments = []

    for comment in relevant_comments:
        sentiment_object = SentimentIntensityAnalyzer()
        sentiment_dict = sentiment_object.polarity_scores(comment)
        polarity.append(sentiment_dict['compound'])

        if polarity[-1] > 0.05:
            positive_comments.append(comment)
        elif polarity[-1] < -0.05:
            negative_comments.append(comment)
        else:
            neutral_comments.append(comment)

    # Calculate Average Polarity
    avg_polarity = sum(polarity) / len(polarity)

    # Determine Overall Response
    overall_response = ""
    if avg_polarity > 0.05:
        overall_response = "Positive"
    elif avg_polarity < -0.05:
        overall_response = "Negative"
    else:
        overall_response = "Neutral"

    # Find Most Positive and Most Negative Comments
    most_positive_comment = relevant_comments[polarity.index(max(polarity))]
    most_negative_comment = relevant_comments[polarity.index(min(polarity))]

    # Create and return the result dictionary
    result_dict = {
        "video_id": video_id,
        "channel_id": uploader_channel_id,
        "average_polarity": avg_polarity,
        "overall_response": overall_response,
        "most_positive_comment": most_positive_comment,
        "most_negative_comment": most_negative_comment
    }

    return result_dict
