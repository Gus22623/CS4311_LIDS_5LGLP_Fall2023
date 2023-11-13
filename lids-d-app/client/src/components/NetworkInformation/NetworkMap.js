import React, { useState, useEffect } from 'react';
import Axios from 'axios';
import { Link } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import Windows_known from './lids-d-app/client/src/components/NetworkInformation/apple-logo-known.png';
import Windows_unknown from './lids-d-app/client/src/components/NetworkInformation/windows-logo-unknown.png';
import Linux_known from'./lids-d-app/client/src/components/NetworkInformation/linux-logo-known.png';
import Linux_unknown from './lids-d-app/client/src/components/NetworkInformation/linux-logo-unknown.png'; 
import Mac_known from './lids-d-app/client/src/components/NetworkInformation/apple-logo-known.png'; 
import Mac_unknown from './lids-d-app/client/src/components/NetworkInformation/apple-logo-unknown.png'; 

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
const imageData = {
  id: 1,
  name: "Device 1",
  status: "recognized",
  x: 50,
  y: 50,
  imagePath: getOsImage('Windows_known'),
  id: 2, name: "Device 2", status: "unknown", x: 100, y: 100, imagePath: getOsImage('Linux_unknown'),
  id: 3, name: "Device 3", status: "recognized", x: 150, y: 150, imagePath: getOsImage('Mac_known')
};

  const getOsImage = (osLogos) => {
        switch(osLogos) {
            case 'Windows_known' :
              return Windows_known; 
            case 'Windows_uknknown' :
              return Windows_unknown;    
            case 'Linux_known' :
                return Linux_known; 
            case 'Linux_uknknown' :
              return Linux_unknown; 
            case 'Mac_known' :
                return Mac_known; 
            case 'Mac_uknknown' :
              return Mac_unknown; 
          default:
              return null;
      }
};
function NetworkMap(){ 
  return(
    <div style={{ position: 'relative', left: imageData.x, top: imageData.y }}>
      <img
        src={imageData.imagePath}
        alt={'${imageData.name}, status: ${imageData.status}'}
        title={'ID: ${imageData.id}, Name: ${imageData.name}, Status: ${imageData.status}'}
      />
      <div className="image-info">
        <p>ID: {imageData.id}</p>
        <p>Name: {imageData.name}</p>
        <p>Status: {imageData.status}</p>
        <p>Coordinates: ({imageData.x}, {imageData.y})</p>
      </div>
    </div>
    
  );
}
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
