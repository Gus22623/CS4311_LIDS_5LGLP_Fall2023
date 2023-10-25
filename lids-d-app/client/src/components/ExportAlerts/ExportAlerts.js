import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom'; 
import Axios from 'axios';
import './ExportAlerts.css'; 

function ExportAlerts() {
  const navigate = useNavigate();              
  const handleViewAlerts = () => {
    navigate('/view-alerts')
  };

  const exportDataAsJSON = () => {
    Axios.get('http://127.0.0.1:5000/getAlerts', { responseType: 'blob' })
      .then((response) => {
        const url = URL.createObjectURL(response.data);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'Alerts.json';
        a.style.display = 'none';
        document.body.appendChild(a);
        a.click();
        a.remove();
        URL.revokeObjectURL(url);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
    };
      const exportDataAsXML = () => {
        Axios.get('http://127.0.0.1:5000/getAlerts', { responseType: 'blob' })
          .then((response) => {
            const url = URL.createObjectURL(response.data);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'Alerts.xml';
            a.style.display = 'none';
            document.body.appendChild(a);
            a.click();
            a.remove();
            URL.revokeObjectURL(url);
          })
          .catch((error) => {
            console.error("Error fetching data:", error);
          });
        };   
        
const exportDataAsCSV = () => {
  Axios.get('http://127.0.0.1:5000/getAlerts')
    .then((response) => {
      const alertList = response.data;

      // Convert JSON data to CSV format
      const jsonToCsv = (jsonData) => {
        const header = Object.keys(jsonData[0]).join(',');
        const csvData = jsonData.map((record) => {
          return Object.values(record).join(',');
        });
        return header + '\n' + csvData.join('\n');
      };

      const csvContent = jsonToCsv(alertList);
      const blob = new Blob([csvContent], { type: 'text/csv' });

      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'Alerts.csv';
      a.style.display = 'none';
      document.body.appendChild(a);

      a.click();
      a.remove();
      URL.revokeObjectURL(url);
    })
    .catch((error) => {
      console.error("Error fetching data:", error);
    });
};

        
  return (
<div>
  <div className="top-section">
  <button className="go-back-button" onClick={handleViewAlerts}>Go Back</button>
    <h1 style={{ textAlign: 'center', color: 'white', fontFamily: 'Baskerville, serif', padding: '50px' }}>Export Format</h1>
  </div>
  <div className="bottom-section">
    <div style={{ textAlign: 'center' }}>
      <div style={{ border: '5px solid #11253D', padding: '20px', margin: '0 auto 0', width: '400px', display: 'block', 
      background: '#11253D', height: '300px', display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
        <button className="button-custom" onClick={exportDataAsJSON}>Export JSON</button>
        <button className="button-custom" onClick={exportDataAsXML}>Export XML</button>
        <button className="button-custom" onClick={exportDataAsCSV}>Export CSV</button>
      </div>
    </div>
  </div>
</div>
  )
}

export default ExportAlerts;
