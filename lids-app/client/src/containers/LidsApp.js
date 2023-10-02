import React, { useState } from 'react';
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
      setView('loading');
    })
    .catch(error => {
      console.error('Error:', error);
      setView('initial');
    });
  };

  const handleEnterPress = () => {
    setView('dashboard');
  };

  return (
    <div className="lids-app">
      {view === 'initial' && <LidsInitialUI onUpload={handleConfigUpload} />}
      {view === 'loading' && <LidsLoadingPage onEnterPress={handleEnterPress} />}
      {view === 'dashboard' && <LidsDashboard />}
      {uploadedFile && <div><h2>Uploaded XML:</h2><pre>{uploadedFile}</pre></div>}
    </div>
  );
}

export default LidsApp;
