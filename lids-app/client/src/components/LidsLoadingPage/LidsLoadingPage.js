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
      <div className="top-section-medium">
      {/* <button style = {{backgroundColor : "LightGray", padding: "10px 20px"}}onClick={onEnterPress}>Main Menu</button> */}
      <button style = {{backgroundColor : "LightGray", padding: "10px 20px", marginLeft: "25px", marginTop: "25px"}}onClick={onEnterPress}>Go Back</button>
      <h1 className="h1-custom">LIDS</h1>
      </div>
      <br></br>
      <div className="bottom-section">
      <img  src = {logo} alt = "loading.." style = {{display: "block", margin: "0 auto", marginTop: "25px"}}/>
      <h2 style={{ color: "white", textAlign: "center" }}>
          Loading<br />Configuration File...
        </h2>
      <h2 style = {{position: "fixed", left: "44%", bottom: "0" , color: "white",textAlign: "center", backgroundColor: "#11253D"}}>LIDS 123.456.78.900</h2> {/* Instead of 0s, get actual IP*/}
      </div>
    </div>
  );
}

export default LidsLoadingPage;
