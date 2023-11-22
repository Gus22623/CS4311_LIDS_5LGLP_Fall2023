/**
 * @author X
 * @version 1.0, 05/05/23
*/
/**
 * @modifiers
 */

import React, { useRef } from 'react';
import './LidsInitialUI.css'; 
import { useNavigate } from 'react-router-dom';

function LidsInitialUI({ onUpload }) {
  const fileInputRef = useRef(null);
  const navigate = useNavigate();
  const handleUpload = () => {
    fileInputRef.current.click();
    navigate('/loading');
  }

  // Handles File Injection
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
    // Root Page
    <div className="lids-initial-ui">
        <div className="top-section-large">
          <h1 className="h1-custom">- - - - - - - - - - - - -</h1>
          <h1 className="h1-custom">Welcome to LIDS</h1>
          <h1 className="h1-custom">- - - - - - - - - - - - -</h1>
        </div>
        <div className="bottom-section">
          <button className="load-button" onClick={handleUpload}>Load Config File</button>
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
