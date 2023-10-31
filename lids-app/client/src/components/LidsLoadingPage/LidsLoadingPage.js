/**
 * @author X
 * @version 1.0, 05/05/23
*/

import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom'; // Import the useNavigate hook
import logo from './loading_gif.gif';
import './LidsLoadingPage.css';

function LidsLoadingPage({ onEnterPress }) {
  const navigate = useNavigate(); // Use the hook
  useEffect(() => {
    const timer = setTimeout(() => {
      navigate('/dashboard'); // Navigate to the dashboard after 5 seconds
    }, 5000); // 5 seconds

    // Cleanup the timer when the component is unmounted
    return () => {
      clearTimeout(timer);
    };
  }, [navigate]);

  return (
    <div className="lids-loading-page">
      <div className="top-section">
      {/* <button style = {{backgroundColor : "LightGray", padding: "10px 20px"}}onClick={onEnterPress}>Main Menu</button> */}
      <button style = {{backgroundColor : "LightGray", padding: "10px 20px"}}onClick={onEnterPress}>Go Back</button>
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
