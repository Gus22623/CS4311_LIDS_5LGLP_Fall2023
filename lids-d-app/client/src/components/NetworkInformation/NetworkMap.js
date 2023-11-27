/**
 * @author X
 * @version 1.0, 05/05/23
*/
/**
 * @modifiers
 */

import React, { useState, useEffect } from 'react';
import Axios from 'axios';
import { Link, useNavigate } from 'react-router-dom';

//Import the nessecary images for OS display
import Windows_known from './microsoft-logo-known.png';
import Windows_unknown from './windows-logo-unknown.png';
import Linux_known from './linux-logo-known.png';
import Linux_unknown from './linux-logo-unknown.png'; 
import Mac_known from './apple-logo-known.png'; 
import Mac_unknown from './apple-logo-unknown.png';

//Perameters for OS image for all users. 
//Includes known and unknown for Linux, Mac and Windows 
const getOsImage = (osName, status) => {
  const osStatus = status === 'recognized' ? 'known' : 'unknown';
  switch (`${osName}_${osStatus}`) {
    case 'Windows_known':
      return Windows_known;
    case 'Windows_unknown':
      return Windows_unknown;
    case 'Linux_known':
      return Linux_known;
    case 'Linux_unknown':
      return Linux_unknown;
    case 'Mac_known':
      return Mac_known;
    case 'Mac_unknown':
      return Mac_unknown;
    default:
      return null;
  }
};
//Perameters for the surrounding rectangle, padding and dimensions of the elements inside (text, OS image, status)
const DeviceNode = ({ device, destIp }) => {
  const osImage = getOsImage(device.os, device.status);
  const rectWidth = 120;
  const rectHeight = 150; 
  const padding = 10;
  const textSize = 14;
  
  //Return of the elements(surrounding rectangle, Host information text, status circle, OS image, IP Address text)
  return (
    <g>
      <rect
        x={device.x - rectWidth/2}
        y={device.y - rectHeight / 2}
        width={rectWidth}
        height={rectHeight}
        fill="none"
        stroke="black"
        strokeWidth="2"
      />
      <text 
      x={device.x - padding} 
      y={device.y + rectHeight/4 - padding} 
      textAnchor="middle" 
      fontSize={textSize}
      fill={device.host.toLowerCase() === 'unknown' ? 'red' : 'black'}>
      Host: {device.host} </text>

      <circle 
      cx={device.x + rectWidth/2-padding} 
      cy={device.y + rectHeight/4 - padding} 
      r={5} 
      fill={device.status === 'recognized' ? 'green' : 'red'} />
      
      {osImage && (
        <image
          x={device.x - rectWidth / 4 - 2}
          y={device.y - rectHeight / 2 + padding}
          href={osImage}
          width="65"
          height="65"
          textAnchor='left'
        />
      )}
      <text x={device.x - rectWidth / 3} 
      y={device.y + rectHeight / 2 - padding } 
      textAnchor="left" 
      fontSize={textSize}
      fill={device.host.toLowerCase() === 'unknown' ? 'red' : 'black'}>
      IP: {destIp}</text>
    </g>
  );
};
//Setup for hardcoded examples of users of the network
function NetworkMap() {
    // For simplicity, we're using static data here.
    const [devices, setDevices] = React.useState([
        { id: 1, name: "Device 1", status: "recognized", x: 50, y: 50 },
        { id: 2, name: "Device 2", status: "unknown", x: 100, y: 100 },
        { id: 3, name: "Device 3", status: "recognized", x: 150, y: 150 },
    ]);
/*
function NetworkMap() {
    const [devices, setDevices] = React.useState([]);

    React.useEffect(() => {
        fetch("/api/devices")
            .then(response => response.json())
            .then(data => {
                // Assuming the API returns an array of devices
                setDevices(data);
            });
    }, []);
    */
    const navigate = useNavigate(); // Added hook

    const handleConfigureServer = () => { // Added function
        navigate('/config-server');
      };
    
      const handleViewAlerts = () => {
        navigate('/view-alerts')
      };
      
      const handleNetworkInfo = () => {
        navigate('/network-map')
      };

    return (
        <div>
            <button className="go-back-button" onClick={handleConfigureServer}>Configure Server</button>
            <button className="go-back-button" onClick={handleViewAlerts}>View Alerts</button>
            <button className="go-back-button" onClick={handleNetworkInfo}>Network Information</button>
            <svg width="400" height="400">
                {devices.map(device => (
                    <DeviceNode key={device.id} device={device} />
                ))}
            </svg>

            <Link to="/network-info">
                <button>Network Info</button>
            </Link>
        </div>
    );
}

export default NetworkMap;
