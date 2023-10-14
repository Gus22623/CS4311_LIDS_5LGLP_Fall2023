import React, { Component } from 'react';
import ViewAlerts from '../components/ViewAlerts/ViewAlerts';
import ConfigureServer from '../components/ConfigureServer/ConfigureServer';
import NetworkInformation from '../components/NetworkInformation/NetworkInformation';
import AlertsExport from '../components/AlertsExport/AlertsExport';
import MenuOptions from '../components/MenuOptions/MenuOptions';

class LidsDApp extends Component {
  constructor(props) {
    super(props);
    this.state = {
      currentScreen: 'viewAlerts'  // Default screen
    };
  }

  switchScreen = (screen) => {
    this.setState({ currentScreen: screen });
  }

  renderScreen = () => {
    switch (this.state.currentScreen) {
      case 'viewAlerts':
        return <ViewAlerts />;
      case 'configureServer':
        return <ConfigureServer />;
      case 'networkInformation':
        return <NetworkInformation />;
      case 'alertsExport':
        return <AlertsExport />;
      default:
        return <ViewAlerts />;
    }
  }

  render() {
    return (
      <div className="lidsd-app-container">
        
        {/* Render the appropriate screen */}
        {this.renderScreen()}

        {/* MenuOptions on the right */}
        <MenuOptions switchScreen={this.switchScreen} />

      </div>
    );
  }
}

export default LidsDApp;
