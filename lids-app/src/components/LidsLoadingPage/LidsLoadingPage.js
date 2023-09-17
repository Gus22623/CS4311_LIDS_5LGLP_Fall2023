import React, { useEffect } from 'react';
import logo from './loading_gif.gif'
import './LidsLoadingPage.css';

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
      <div className="top-section">
      <button style = {{backgroundColor : "LightGray", padding: "10px 60px", borderRadius: "5px", margin: "0px 1px"}}onClick={onEnterPress}>Main Menu</button>
      <button style = {{backgroundColor : "LightGray", padding: "10px 60px", borderRadius: "5px", margin: "0px 0px"}}onClick={onEnterPress}>Go Back</button>
      <h1 className="h1-custom">LIDS</h1>
      </div>
      <br></br>
      <div className="bottom-section">
      <h2 style = {{color: "white", textAlign: "center", }}>Loading Configuration File...</h2>
      <img  src = {logo} alt = "loading.." style = {{display: "block", margin: "0 auto"}}/>
      <h2 style = {{position: "fixed", left: "44%", bottom: "0" , color: "white",textAlign: "center", backgroundColor: "#11253D"}}>LIDS 000.000.00.000</h2> {/* Instead of 0s, get actual IP*/}
      </div>
    </div>
  );
}

export default LidsLoadingPage;
