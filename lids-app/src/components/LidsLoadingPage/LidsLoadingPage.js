import React, { useEffect } from 'react';

function LidsLoadingPage({ onEnterPress }) {
  useEffect(() => {
    const handleKeyDown = (event) => {
      if (event.key === 'Enter') {
        onEnterPress();
      }
    };

    window.addEventListener('keydown', handleKeyDown);

    // Cleanup the event listener when the component is unmounted
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [onEnterPress]);

  return (
    <div className="lids-loading-page">
      <h1>Welcome to LIDS</h1>
      <h2>Loading Configuration...</h2>
      <div className="loading-spinner">🔄</div>
    </div>
  );
}

export default LidsLoadingPage;
