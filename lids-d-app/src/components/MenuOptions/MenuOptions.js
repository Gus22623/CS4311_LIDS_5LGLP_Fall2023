import React from 'react';
import { Link } from 'react-router-dom';

class MenuOptions extends React.Component {
  render() {
    return (
      <div className="menu-options-container">
        <div className="menu-box">Malicious packet count</div> {/* If this needs linking later, you can add a route */}
        
        <Link to="/configure-server" className="menu-box button-style">Configure Server</Link>
        <Link to="/view-alerts" className="menu-box button-style">View Alerts</Link>
        <Link to="/network-information" className="menu-box button-style">Network information</Link>
      </div>
    );
  }
}

export default MenuOptions;
