import React from 'react';

function NotificationsDisplay({ notifications }) {
  return (
    <div className="notifications-display">
      <h1>Notifications</h1>
      {notifications.map((notification, index) => (
        <div key={index} className="notification-item">
          {notification.message}
        </div>
      ))}
    </div>
  );
}

export default NotificationsDisplay;
