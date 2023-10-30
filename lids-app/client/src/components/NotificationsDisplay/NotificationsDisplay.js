/**
 * @author X
 * @version 1.0, 05/05/23
*/

import React from 'react';
import PropTypes from 'prop-types';
import './NotificationsDisplay.css';

const NotificationsDisplay = ({ notifications }) => {
  return (
    <div className="notifications-display-container">
      <div className="header">
        <h1>NOTIFICATIONS</h1>
      </div>
      <div className="table-container">
        <table className="notifications-table">
          <thead>
            <tr>
              <th>Id</th>
              <th>Message</th>
            </tr>
          </thead>
          <tbody>
            {notifications.map((notification, index) => (
              <tr key={notification.id} className={index % 2 === 0 ? "gray-row" : "gray-row"}>
                <td>{notification.id}</td>
                <td>{notification.message}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

// Sample notifications to display
const sampleNotifications = [
  { id: '1', message: 'User logged in' },
  { id: '2', message: 'Configuration File uploaded' },
  // Add more as needed
];

NotificationsDisplay.propTypes = {
  notifications: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.string.isRequired,
      message: PropTypes.string.isRequired,
    })
  ).isRequired,
};

export default function() {
  return <NotificationsDisplay notifications={sampleNotifications} />
};
