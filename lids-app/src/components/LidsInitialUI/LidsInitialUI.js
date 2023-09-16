// LidsInitialUI.js
import React from 'react';
import './LidsInitialUI.css'; 

function LidsInitialUI({ onUpload }) {
  return (
    <div className="lids-initial-ui">
        <div className="top-section">
          <h1 className="h1-custom">- - - - - - - - - - - - -</h1>
          <h1 className="h1-custom">Welcome to</h1>
          <h1 className="h1-custom">LIDS</h1>
          <h1 className="h1-custom">- - - - - - - - - - - - -</h1>
        </div>
        <div className="bottom-section">
          <button onClick={onUpload}>Load Config File</button>
        </div>
    </div>
  );
}

export default LidsInitialUI;
