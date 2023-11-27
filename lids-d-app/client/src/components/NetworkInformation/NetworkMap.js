import React, { useState, useEffect } from 'react';
import Axios from 'axios';
import { useNavigate } from 'react-router-dom';

function NetworkMap() {
  const [sourceIpData, setSourceIpData] = useState([]);
  const navigate = useNavigate();

  // Define the authorized IP addresses
  const AUTHORIZED_IPS = [
    '10.0.0.1', '10.0.0.2', '10.0.0.3', '10.0.0.4', '10.0.0.5', '10.0.0.245'
  ];

  // Fetch source_ip data along with OS information
  useEffect(() => {
    Axios.get('http://127.0.0.1:5000/getAlertsIP')
      .then((response) => {
        setSourceIpData(response.data.map((item) => ({
          ip: item.source_ip,
          os: '', // Initially set to blank
          status: isIpRecognized(item.source_ip) ? 'recognized' : 'unrecognized',
        })));
      })
      .catch((error) => {
        console.error("Error fetching source_ip data:", error);
      });
  }, []);

  // Fetch the whitelist from the JSON file
  useEffect(() => {
    Axios.get('./ipAddresses_whitelist.json')
      .then((response) => {
        const whitelist = response.data.ipAddresses || [];
        setSourceIpData((data) =>
          data.map((item) => ({
            ...item,
            status: isIpRecognized(item.ip, whitelist) ? 'recognized' : 'unrecognized',
          }))
        );
      })
      .catch((error) => {
        console.error('Error fetching whitelist:', error.message);
      });
  }, []);

  // Handler for the back button
  const handleBack = () => {
    navigate('/view-alerts'); // Update this path as per your route configuration
  };

  // Function to determine if an IP is recognized
  const isIpRecognized = (ip) => AUTHORIZED_IPS.includes(ip);

  return (
    <div>
      <button onClick={handleBack}>Back to Network Information</button>
      <table>
        <thead>
          <tr>
            <th>IP Address</th>
            <th>OS</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {sourceIpData.map((item, index) => (
            <tr key={index}>
              <td>{item.ip}</td>
              <td>{item.os}</td> {/* Display initially blank */}
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

export default NetworkMap;