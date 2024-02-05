// AnalysisResult.js

import React from 'react';
import './AnalysisResult.css'; // Import the CSS file

const AnalysisResult = ({ result }) => {
  return (
    <div className="result-container">
      <div className="result-row">
        <div className="result-box1">
          <h3>Video ID: </h3>
          <p>{result.video_id}</p>
        </div>
        <div className="result-box1">
          <h3>Channel ID:</h3>
          <p>{result.channel_id}</p>
        </div>
      </div>

      <div className="result-row">
        <div className="result-box1">
          <h3>Average Polarity:</h3>
          <p>{result.average_polarity}</p>
        </div>
        <div className="result-box1">
          <h3>Overall Response:</h3>
          <p>{result.overall_response}</p>
        </div>
      </div>

      <div className="result-row">
        <div className="result-box">
          <h3>Most Positive Comment:</h3>
          <p>{result.most_positive_comment}</p>
        </div>
        <div className="result-box">
          <h3>Most Negative Comment: </h3>
          <p>{result.most_negative_comment}</p>
        </div>
      </div>
    </div>
  );
};

export default AnalysisResult;
