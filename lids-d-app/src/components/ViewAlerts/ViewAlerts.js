import React from 'react';
import MenuOptions from '../MenuOptions/MenuOptions';

class ViewAlerts extends React.Component {
  render() {
    return (
      <div className="view-alerts-page">

        <div className="view-alerts-container">

          <div className="overlay-title">
            Sort Alerts by:
          </div>

          <div className="buttons-container">
            <button>Date</button>
            <button>Priority Level</button>
            <button>Protocol</button>
            <button>Source</button>
          </div>

          <div className="toolbar">
            <span>Level</span>
            <span>Time</span>
            <span>IP</span>
            <span>Port</span>
            <span>Protocol</span>
            <span>Description</span>
          </div>

          <div className="alerts-list">
            {/* This will list individual alerts. Consider fetching data from a backend or a state management system. */}
          </div>

        </div>

        <MenuOptions />

      </div>
    );
  }
}

export default ViewAlerts;
