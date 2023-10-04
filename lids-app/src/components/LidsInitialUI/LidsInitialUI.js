// LidsInitialUI.js
import React from 'react';
import './LidsInitialUI.css'; 

function LidsInitialUI({ onUpload }) {
  const handleLoadConfigClick = () => {
    document.getElementById("configFile").click();
  };

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      // TODO: Process the selected file if needed
      onUpload();
    }
  };

  return (
    <div className="lids-initial-ui">
        <div className="top-section">
          <h1 className="h1-custom">- - - - - - - - - - - - -</h1>
          <h1 className="h1-custom">Welcome to</h1>
          <h1 className="h1-custom">LIDS</h1>
          <h1 className="h1-custom">- - - - - - - - - - - - -</h1>
        </div>
        <input 
            type="file" 
            id="configFile" 
            style={{ display: 'none' }} 
            onChange={handleFileChange} 
        />
        <div className="bottom-section">
          <button style={{backgroundColor: "LighGray", padding: "10px 20px"}} onClick={handleLoadConfigClick}>Load Config File</button>
        </div>
    </div>
  );
}

export default LidsInitialUI;
