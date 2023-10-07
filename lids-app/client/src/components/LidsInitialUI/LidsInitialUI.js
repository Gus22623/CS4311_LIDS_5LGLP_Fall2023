import React, { useRef } from 'react';
import './LidsInitialUI.css'; 

function LidsInitialUI({ onUpload }) {
  const fileInputRef = useRef(null);

  const handleUpload = () => {
    fileInputRef.current.click();
  }

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = () => {
        onUpload(reader.result);
      }
      reader.readAsText(file);
    }
  }

  return (
    <div className="lids-initial-ui">
        <div className="top-section">
          <h1 className="h1-custom">- - - - - - - - - - - - -</h1>
          <h1 className="h1-custom">Welcome to LIDS</h1>
          <h1 className="h1-custom">- - - - - - - - - - - - -</h1>
        </div>
        <div className="bottom-section">
          <button style={{backgroundColor: "LightGray", padding: "10px 20px", marginTop: "50px", height: "50px", width: "300px"}} onClick={handleUpload}>Load Config File</button>
          <input
            type="file"
            ref={fileInputRef}
            style={{display: "none"}}
            onChange={handleFileChange}
            accept=".xml"
          />
        </div>
    </div>
  );
}

export default LidsInitialUI;
