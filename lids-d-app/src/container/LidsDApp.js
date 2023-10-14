import React, { Component } from 'react';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link
} from 'react-router-dom';
import ViewAlerts from '../components/ViewAlerts/ViewAlerts';
import ConfigureServer from '../components/ConfigureServer/ConfigureServer';
import NetworkInformation from '../components/NetworkInformation/NetworkInformation';
import AlertsExport from '../components/AlertsExport/AlertsExport';
import MenuOptions from '../components/MenuOptions/MenuOptions';
import NetworkMap from '../components/NetworkInformation/NetworkMap';

class LidsDApp extends Component {
  render() {
    return (
      <Router>
        <div className="lidsd-app-container">
          <ViewAlerts />
          <Routes>
            <Route path="/view-alerts" element={ViewAlerts} />
            <Route path="/configure-server" element={ConfigureServer} />
            <Route path="/network-information" element={NetworkInformation} />
            <Route path="/alerts-export" element={AlertsExport} />
            <Route path="/network-map" element={NetworkMap} />
            <Route path="/" element={ViewAlerts} />
          </Routes>
        </div>
      </Router>
    );
  }
}

export default LidsDApp;
