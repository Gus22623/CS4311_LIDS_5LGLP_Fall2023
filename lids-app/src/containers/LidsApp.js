import React, { useState } from 'react';
import LidsInitialUI from '../components/LidsInitialUI/LidsInitialUI';
import LidsLoadingPage from '../components/LidsLoadingPage/LidsLoadingPage';
import LidsDashboard from '../components/LidsDashboard/LidsDashboard';

function LidsApp() {
  const [view, setView] = useState('initial'); // 'initial', 'loading', or 'dashboard'

  const handleConfigUpload = () => {
    setView('loading');
    // Handle the actual file upload logic here if needed
  };

  const handleEnterPress = () => {
    setView('dashboard');
  };

  return (
    <div className="lids-app">
      {view === 'initial' && <LidsInitialUI onUpload={handleConfigUpload} />}
      {view === 'loading' && <LidsLoadingPage onEnterPress={handleEnterPress} />}
      {view === 'dashboard' && <LidsDashboard />}
    </div>
  );
}

export default LidsApp;
