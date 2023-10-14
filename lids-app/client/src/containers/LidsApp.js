import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LidsInitialUI from '../components/LidsInitialUI/LidsInitialUI';
import LidsLoadingPage from '../components/LidsLoadingPage/LidsLoadingPage';
import LidsDashboard from '../components/LidsDashboard/LidsDashboard';

function LidsApp() {
  const [view, setView] = useState('initial'); // 'initial', 'loading', or 'dashboard'
  const [uploadedFile, setUploadedFile] = useState(null);

  const handleConfigUpload = (fileContent) => {
    fetch('http://127.0.0.1:5000/upload-xml', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/xml', // Set the content type to XML
      },
      body: fileContent,
    })
    .then(response => response.text())
    .then(data => {
      console.log(data);
      view('/loading');
    })
    .catch(error => {
      console.error('Error:', error);
      view('/');
    });
  };

  const handleEnterPress = () => {
    view('/dashboard');
  };

  return (
    <Router>
      <div className="lids-app">
        <Routes>
          <Route path="/" element={<LidsInitialUI onUpload={handleConfigUpload} />} />
          <Route path="/loading" element={<LidsLoadingPage onEnterPress={handleEnterPress} />} />
          <Route path="/dashboard" element={<LidsDashboard />} />
        </Routes>
      
        {uploadedFile && <div><h2>Uploaded XML:</h2><pre>{uploadedFile}</pre></div>}
      </div>
    </Router>
  );
}

export default LidsApp;
