import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
//import LidsInitialUI from '../components/LidsInitialUI/LidsInitialUI';
//import LidsLoadingPage from '../components/LidsLoadingPage/LidsLoadingPage';
import LidsDashboard from '../components/LidsDashboard/LidsDashboard';
import AlertDisplay from '../components/AlertDisplay/AlertDisplay';
import NetworkMap from '../components/NetworkInformation/NetworkMap';

function LidsApp() {

  
  return (
    <Router>
      <div className="lids-app">
        <Routes>
          <Route path="/" element={<LidsDashboard />} />
          <Route path="/network-map" element={<NetworkMap />} /> 
          <Route path="/view-alerts" element={<LidsDashboard />} />
        </Routes>
      
      </div>
    </Router>
  );
}

export default LidsApp;
