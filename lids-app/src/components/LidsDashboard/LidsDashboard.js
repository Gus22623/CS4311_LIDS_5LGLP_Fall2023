import React, { useState } from 'react';
import AlertsDisplay from '../AlertDisplay/AlertDisplay';
import ErrorsDisplay from '../ErrorsDisplay/ErrorsDisplay';
import NotificationsDisplay from '../NotificationsDisplay/NotificationsDisplay';
import SortByDropdown from '../SortByDropdown/SortByDropdown';
import './LidsDashboard.css';

function LidsDashboard() {
  // Mock data for demonstration purposes
  const [alerts, setAlerts] = useState([]); // You'd typically fetch this data or manage it in a global state
  //eslint-disable-next-line
  const [errors, setErrors] = useState([]);
  //eslint-disable-next-line
  const [notifications, setNotifications] = useState([]);

  const handleSort = (criteria) => {
    // Implement sorting logic based on the criteria
    // For example, if sorting alerts by level:
    if (criteria === 'Level') {
      const sortedAlerts = [...alerts].sort((a, b) => a.level - b.level);
      setAlerts(sortedAlerts);
    }
    // Implement other sorting criteria similarly
  };

  return (
    <div className="lids-dashboard">
      <div className="top-section">
      <h1 className="h1-custom" style ={{textAlign: "center"}}>LIDS Dashboard</h1>
      </div>
      <div className="bottom-section">
      <SortByDropdown onSort={handleSort} />
      <AlertsDisplay alerts={alerts} />
      <ErrorsDisplay errors={errors} />
      <NotificationsDisplay notifications={notifications} />
      </div>
      {/* Other components and logic for the dashboard */}
    </div>
  );
}

export default LidsDashboard;
