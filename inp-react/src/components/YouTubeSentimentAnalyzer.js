// YouTubeSentimentAnalyzer.js
import React, { useState } from 'react';
import './YouTubeSentimentAnalyzer.css';

const YouTubeSentimentAnalyzer = ({ onAnalysisResult }) => {
  const [youtubeUrl, setYoutubeUrl] = useState('');
  const [result, setResult] = useState(null);

  const handleUrlChange = (e) => {
    setYoutubeUrl(e.target.value);
  };

  const handleAnalyzeClick = async () => {
    try {
      console.log(`Analyzing sentiment for YouTube video: ${youtubeUrl}`);

      const response = await fetch('http://127.0.0.1:5000/process-data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ data: youtubeUrl }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const resultData = await response.json();
      setResult(resultData);

      // Pass the result to the parent component
      onAnalysisResult(resultData);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="analyzer-container">
      <input
        type="text"
        placeholder="Enter your YouTube URL "
        value={youtubeUrl}
        onChange={handleUrlChange}
        className="curved-input"
      />
      <button onClick={handleAnalyzeClick} className="curved-button">
        Analyze
      </button>
    </div>
  );
};

export default YouTubeSentimentAnalyzer;
