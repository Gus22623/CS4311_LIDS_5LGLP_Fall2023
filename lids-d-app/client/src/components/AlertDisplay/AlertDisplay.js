/**
 * @author X
 * @version 1.0, 05/05/23
*/
/**
 * @modifiers
 */

import React from 'react';
import './AlertDisplay.css';
import '../../containers/LidsDApp';

const AlertDisplay = () => {
  return (
    <div className="alert-display-container">
      <div className="header">
        <h1>ALERTS</h1>
      </div>
      <div className="table-container">
        <table className="alert-table">
          <thead>
            <tr>
              <th>Lvl</th>
              <th>Time</th>
              <th>IP</th>
              <th>Port</th>
              <th>Protocol</th>
              <th>Description</th>
            </tr>
          </thead>
          <tbody>
            <tr className="yellow-row">
              <td>2</td>
              <td>11.6565</td>
              <td>192.168.0.8</td>
              <td>88</td>
              <td>Unknown host ping</td>
            </tr>
            <tr className="red-row">
              <td>3</td>
              <td>193.175.0.4</td>
              <td>27</td>
              <td>22</td>
              <td>Port Scan</td>
            </tr>
            <tr className="gray-row">
              <td>1</td>
              <td>5.6565</td>
              <td>191.156.0.2</td>
              <td>56</td>
              <td>Fail login attempts</td>
            </tr>
            {/* we can add more rows */}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default AlertDisplay;
