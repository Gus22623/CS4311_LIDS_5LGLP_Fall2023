import React from 'react';
import './AlertDisplay.css';

const AlertDisplay = () => {
  return (
    <div className="alert-display-container">
      <div className="header">
        <button className="go-back-button">Go Back</button>
        <h1>ALERTS</h1>
      </div>
      <div className="table-container">
        <table className="alert-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>System Name</th>
              <th>IP Address</th>
            </tr>
          </thead>
          <tbody>
            <tr className="green-row">
              <td>1992-05-25</td>
              <td>Work Station 1</td>
              <td>72.97.126.181</td>
            </tr>
            <tr className="gray-row">
              <td>1997-09-16</td>
              <td>Work Station 2</td>
              <td>1.42.52.99</td>
            </tr>
            {/* Can add more rows*/}
          </tbody>
        </table>
      </div>
      <div className="export-button-container">
        <button className="export-button">Export Alerts</button>
      </div>
    </div>
  );
};

export default AlertDisplay;
