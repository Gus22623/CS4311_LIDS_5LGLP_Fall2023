import React from 'react';
import MenuOptions from '../MenuOptions/MenuOptions';

class ConfigureServer extends React.Component {
  render() {
    return (
      <div className="configure-server-container">

        <div className="configuration-instructions">
          Text prompting users to provide their configuration file
        </div>

        <button>Browse</button>
        
        <div className="previous-configurations">
          Overlay text as “select the previous configuration”
          {/* Icons for previous configurations here */}
        </div>

        <MenuOptions />

        {/* Handle successful configuration and "Start Server" button logic here. */}
      </div>
    );
  }
}

export default ConfigureServer;
