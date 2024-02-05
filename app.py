from flask import Flask, request, jsonify
from flask_cors import CORS  # Import the CORS module
from Sentiment_Analyzer import analyze_youtube_video

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/process-data', methods=['POST'])
def process_data():
    try:
        data = request.json.get('data')
        result = analyze_youtube_video(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
