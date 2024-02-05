// App.js
import React, { useState } from 'react';
import './App.css';
import YouTubeSentimentAnalyzer from './components/YouTubeSentimentAnalyzer';
import AnalysisResult from './components/AnalysisResult';
import utube from './images/youtube-logo.png';

function App() {
  const [analysisResult, setAnalysisResult] = useState(null);

  const handleAnalysisResult = (result) => {
    setAnalysisResult(result);
  };

  return (
    <div className="App">
      {!analysisResult && <img src={utube} alt="Example" className="logo" />}
      <YouTubeSentimentAnalyzer onAnalysisResult={handleAnalysisResult} />
      {analysisResult && <AnalysisResult result={analysisResult} />}
    </div>
  );
}

export default App;
