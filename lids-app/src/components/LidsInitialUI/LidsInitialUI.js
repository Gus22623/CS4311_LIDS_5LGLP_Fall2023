// LidsInitialUI.js
import React from 'react';

function LidsInitialUI({ onUpload }) {
  return (
    <div className="lids-initial-ui">
      <h1>Welcome to LIDS</h1>
      <h2>Upload Configuration File</h2>
      <button onClick={onUpload}>Upload</button>
    </div>
  );
}

export default LidsInitialUI;
