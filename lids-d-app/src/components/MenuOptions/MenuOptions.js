import React from 'react';

class MenuOptions extends React.Component {
  render() {
    return (
      <div className="menu-options-container">
        <div className="menu-box">Malicious packet count</div>
        <div className="menu-box">Configure Server</div>
        <div className="menu-box">View Alerts</div>
        <div className="menu-box">Network information</div>
      </div>
    );
  }
}

export default MenuOptions;
