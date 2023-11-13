import React, { useState, useEffect } from 'react';
import Axios from 'axios';
import { Link } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';

function DeviceNode({ device, destIp }) {
  const color = device.status === 'recognized' ? 'green' : 'red';
  const osImage = getOsImage(device.os);

  return (
    <g>
      <circle cx={device.x} cy={device.y} r={10} fill={color} />
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
}

function getOsImage(os) {

  const osImages = {
    'Windows_known': 'lids-d-app/client/src/components/NetworkInformation/apple-logo-known.png',
    'Windows_unknown': 'lids-d-app/client/src/components/NetworkInformation/windows-logo-unknown.png',
    'Linux_known': 'lids-d-app/client/src/components/NetworkInformation/linux-logo-known.png',
    'Linux_unknown': 'lids-d-app/client/src/components/NetworkInformation/linux-logo-unknown.png',
    'Mac_known': 'lids-d-app/client/src/components/NetworkInformation/apple-logo-known.png',
    'Mac_unknown': 'lids-d-app/client/src/components/NetworkInformation/apple-logo-unknown.png',
  };

  return osImages[os];
}

function NetworkMap() {
  const [devices, setDevices] = useState([
    { id: 1, name: "Device 1", status: "recognized", x: 50, y: 50, os: 'Windows_known' },
    { id: 2, name: "Device 2", status: "unknown", x: 100, y: 100, os: 'Linux_unknown' },
    { id: 3, name: "Device 3", status: "recognized", x: 150, y: 150, os: 'Mac_known' },
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
  const [destIpData, setDestIpData] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    Axios.get('http://127.0.0.1:5000/getAlertsIP')
      .then((response) => {
        const destIpData = response.data.map(item => item.dest_ip);
        setDestIpData(destIpData);
      })
      .catch((error) => {
        console.error("Error fetching dest_ip data:", error);
      });
  }, []);

  const handleConfigureServer = () => {
    navigate('/config-server');
  };

  const handleViewAlerts = () => {
    navigate('/view-alerts');
  };

  const handleNetworkInfo = () => {
    navigate('/network-map');
  };

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
