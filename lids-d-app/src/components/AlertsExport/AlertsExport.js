import React from 'react';

class AlertsExport extends React.Component {
    render() {
        return (
            <div className="alerts-export-container">

                <button>Dashboard</button>
                <button>Alert</button>
                <button>Network</button>
                <button>Setting</button>
                <button>Exit & Close Application</button>

                <div className="export-popup">
                    <div className="title">Export All Alerts</div>
                    <button>Export As</button>
                    <button>Select</button>
                    <button>Save as</button>
                    <button>Select</button>
                    <button>Apply</button>
                    <button>Cancel</button>
                </div>

            </div>
        );
    }
}

export default AlertsExport;
