import React, { useState } from 'react';
import AlertsDisplay from '../AlertDisplay/AlertDisplay';
import ErrorsDisplay from '../ErrorsDisplay/ErrorsDisplay';
import NotificationsDisplay from '../NotificationsDisplay/NotificationsDisplay';
import SortByDropdown from '../SortByDropdown/SortByDropdown';
import './LidsDashboard.css';

function LidsDashboard() {
  const [alerts, setAlerts] = useState([]);
  const [errors, setErrors] = useState([]);
  const [notifications, setNotifications] = useState([]);
  const [connectionStatus, setConnectionStatus] = useState('Connected');

  const handleSort = (criteria) => {
    if (criteria === 'Level') {
      const sortedAlerts = [...alerts].sort((a, b) => a.level - b.level);
      setAlerts(sortedAlerts);
    }
  };

  const handleDisconnect = () => {
    setConnectionStatus('Disconnected');
  };

  return (
    <div className="lids-dashboard">
      <div className="top-section">
      <button className="go-back-button">Go Back</button>
      <button className="disconnect-button-top" onClick={handleDisconnect}>Disconnect</button>
        <h1 className="h1-custom">LIDS Dashboard</h1>
      </div>
      <div className="lids-ip-connection">
        <div className="lids-ip">LIDS IP: 192.168.1.100</div>
        <div></div>
        <div className="connection-status">{connectionStatus}</div>
      </div>
      <div className="bottom-section">
        <SortByDropdown onSort={handleSort} />
        <AlertsDisplay alerts={alerts} />
        <ErrorsDisplay errors={errors} />
        <NotificationsDisplay notifications={notifications} />
      </div>
    </div>
  );
}

export default LidsDashboard;
