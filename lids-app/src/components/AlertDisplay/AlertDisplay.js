import React from 'react';

function AlertDisplay({ alerts }) {
  return (
    <div className="alert-display">
      <h1>Alerts</h1>
      <div className="alert-header">
        <span>Lvl</span>
        <span>Time</span>
        <span>IP</span>
        <span>Port</span>
        <span>Description</span>
      </div>
      {alerts.map((alert, index) => (
        <div key={index} className="alert-item">
          <span>{alert.level}</span>
          <span>{alert.time}</span>
          <span>{alert.ip}</span>
          <span>{alert.port}</span>
          <span>{alert.description}</span>
        </div>
      ))}
    </div>
  );
}

export default AlertDisplay;
