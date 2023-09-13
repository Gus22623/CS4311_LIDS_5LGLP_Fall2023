import React, { useState } from 'react';
import AlertsDisplay from '../AlertDisplay/AlertDisplay';
import ErrorsDisplay from '../ErrorsDisplay/ErrorsDisplay';
import NotificationsDisplay from '../NotificationsDisplay/NotificationsDisplay';
import SortByDropdown from '../SortByDropdown/SortByDropdown';

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
      <h1>LIDS Dashboard</h1>

      <SortByDropdown onSort={handleSort} />

      <AlertsDisplay alerts={alerts} />
      <ErrorsDisplay errors={errors} />
      <NotificationsDisplay notifications={notifications} />

      {/* Other components and logic for the dashboard */}
    </div>
  );
}

export default LidsDashboard;
