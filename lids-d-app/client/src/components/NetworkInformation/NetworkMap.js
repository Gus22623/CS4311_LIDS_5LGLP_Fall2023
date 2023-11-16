import React, { useState, useEffect } from 'react';
import Axios from 'axios';
import { Link, useNavigate } from 'react-router-dom';

import Windows_known from './lids-d-app/client/src/components/NetworkInformation/windows-logo-known.png';
import Windows_unknown from './lids-d-app/client/src/components/NetworkInformation/windows-logo-unknown.png';
import Linux_known from './lids-d-app/client/src/components/NetworkInformation/linux-logo-known.png';
import Linux_unknown from './lids-d-app/client/src/components/NetworkInformation/linux-logo-unknown.png'; 
import Mac_known from './lids-d-app/client/src/components/NetworkInformation/apple-logo-known.png'; 
import Mac_unknown from './lids-d-app/client/src/components/NetworkInformation/apple-logo-unknown.png'; 

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

  return (
    <g>
      <circle cx={device.x} cy={device.y} r={10} fill={device.status === 'recognized' ? 'green' : 'red'} />
      {osImage && (
        <image
          x={device.x - 10}
          y={device.y - 30}
          href={osImage}
          width="20"
          height="20"
        />
      )}
      <text x={device.x} y={device.y + 15} textAnchor="middle">{destIp}</text>
    </g>
  );
};

function NetworkMap() {
  const [devices, setDevices] = useState([]);
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
      <svg width="400" height="400">
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
