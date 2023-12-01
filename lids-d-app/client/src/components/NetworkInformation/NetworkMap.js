/**
 * @author Joshua Shoemaker 
 * @created 10/20/23
 * @version 1.2
 * @modifers Brittany Madrigal 
 * @modified 11/6/23, 11/7/23, 11/10/23, 11/18 - 11/19/23
*/
import React, { useState, useEffect } from 'react';
import Axios from 'axios';
import { useNavigate } from 'react-router-dom';

function NetworkMap() {
  const [sourceIpData, setSourceIpData] = useState([]);
  const navigate = useNavigate();

  // Fetch source_ip data 
  useEffect(() => {
    Axios.get('http://127.0.0.1:5000/getAlertsIP')
      .then((response) => {
        setSourceIpData(response.data.map((item) => ({
          ip: item.source_ip,
          status: isIpRecognized(item.source_ip) ? 'recognized' : 'unrecognized',
        })));
      })
      .catch((error) => {
        console.error("Error fetching source_ip data:", error);
      });
  }, []);

  // Fetch the whitelist from the XML file
  const whiteList= () => {
    useEffect(() => {
      Axios.get('./ipAddresses_whitelist.xml')
        .then((response) => {
          const parser = new DOMParser();
          const xmlDoc = parser.parseFromString(response.data, 'text/xml');
  
          // Extract IP addresses from parsed XML data
          const whitelist = Array.from(xmlDoc.querySelectorAll('ip')).map((ipNode) => ipNode.textContent);
  
          // Update state based on the whitelist
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

  };

  // Handler for the back button
  const handleBack = () => {
    navigate('/view-alerts'); 
  };

  return (
    <div>
      <button onClick={handleBack}>Back to Network Information</button>
      <table>
        <thead>
          <tr>
            <th>IP Address</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {sourceIpData.map((item, index) => (
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

export default NetworkMap;
