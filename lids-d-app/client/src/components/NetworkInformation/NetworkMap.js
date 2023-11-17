import React, { useState, useEffect } from 'react';
import Axios from 'axios';
import { Link, useNavigate } from 'react-router-dom';

import Windows_known from './microsoft-logo-known.png';
import Windows_unknown from './windows-logo-unknown.png';
import Linux_known from './linux-logo-known.png';
import Linux_unknown from './linux-logo-unknown.png'; 
import Mac_known from './apple-logo-known.png'; 
import Mac_unknown from './apple-logo-unknown.png';

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

const DeviceNode = ({ device, destIp }) => {
  const osImage = getOsImage(device.os, device.status);
  const rectWidth = 150;
  const rectHeight = 180; 
  const padding = 10;

  return (
    <g>
      <rect
        x={device.x - rectWidth / 2}
        y={device.y - rectHeight / 2}
        width={rectWidth}
        height={rectHeight}
        fill="none"
        stroke="black"
        strokeWidth="2"
      />
      <text x={device.x} y={device.y - rectHeight / 2 + padding} textAnchor="middle">Host:{device.host}</text>
      <circle cx={device.x} cy={device.y - padding} r={10} fill={device.status === 'recognized' ? 'green' : 'red'} />
      {osImage && (
        <image
          x={device.x - rectWidth / 4}
          y={device.y - rectHeight / 2 + padding}
          href={osImage}
          width="45"
          height="45"
        />
      )}
      <text x={device.x} y={device.y + 15} textAnchor="middle">{destIp}</text>
    </g>
  );
};

function NetworkMap() {
  const [devices, setDevices] = useState([
    { id: 1, os: 'Windows', status: 'recognized', x: 150, y: 100, host: "Diana"},
    { id: 2, os: 'Linux', status: 'unknown', x: 300, y: 150, Host:"unknown"},
    { id: 3, os: 'Mac', status: 'recognized', x: 450, y: 175, Host:"Sebastian"}
  ]);
  const [destIpData, setDestIpData] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    // Fetch devices data
    // setDevices(fetchedData);

    Axios.get('http://127.0.0.1:5000/getAlertsIP')
      .then((response) => {
        const destIpData = response.data.map(item => item.dest_ip);
        setDestIpData(destIpData);
      })
      .catch((error) => {
        console.error("Error fetching dest_ip data:", error);
      });
  }, []);

  // Handlers for various actions
  const handleConfigureServer = () => navigate('/config-server');
  const handleViewAlerts = () => navigate('/view-alerts');
  const handleNetworkInfo = () => navigate('/network-map');

  return (
    <div>
      <button className="go-back-button" onClick={handleConfigureServer}>Configure Server</button>
      <button className="go-back-button" onClick={handleViewAlerts}>View Alerts</button>
      <button className="go-back-button" onClick={handleNetworkInfo}>Network Information</button>
      <svg width="1000" height="600">
        {devices.map((device, index) => (
          <DeviceNode key={device.id} device={device} destIp={destIpData[index]} />
        ))}
      </svg>
      <Link to="/network-info">
        <button>Network Info</button>
      </Link>
    </div>
  );
}

export default NetworkMap;
