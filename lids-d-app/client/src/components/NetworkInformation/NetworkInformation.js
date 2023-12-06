import React, { useState, useEffect } from 'react';
import Axios from 'axios';
import { Link, useNavigate } from 'react-router-dom';
import './NetworkInformation.css';

// Whitelist of authorized IPs
const AUTHORIZED_IPS = [
  '10.0.0.1', '10.0.0.2', '10.0.0.3', '10.0.0.4', '10.0.0.5', '10.0.0.245'
];

// Function to determine if an IP is recognized
const isIpRecognized = (ip) => AUTHORIZED_IPS.includes(ip) ? 'recognized' : 'unrecognized';

function NetworkInformation() {
  const [destIpData, setDestIpData] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    Axios.get('http://127.0.0.1:5000/getAlertsIP')
      .then((response) => {
        setDestIpData(response.data.map(item => ({
          ip: item.dest_ip,
          status: isIpRecognized(item.dest_ip)
        })));
      })
      .catch((error) => {
        console.error("Error fetching dest_ip data:", error);
      });
  }, []);

  // Handlers for navigation of buttons
  const handleConfigureServer = () => navigate('/config-server');
  const handleViewAlerts = () => navigate('/view-alerts');
  const handleNetworkMap = () => navigate('/network-map');

  return (
    <div className='network-info'>
      <button className="go-back-button" onClick={handleViewAlerts}>View Alerts</button>
      <button className="go-back-button" onClick={handleNetworkMap}>Network Map</button>
      
      <table>
        <thead>
          <tr>
            <th>IP Address</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {destIpData.map((item, index) => (
            <tr key={index}>
              <td>{item.ip}</td>
              <td style={{ color: item.status === 'recognized' ? 'green' : 'red' }}>
                {item.status === 'recognized' ? '✔' : '✖'}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default NetworkInformation;