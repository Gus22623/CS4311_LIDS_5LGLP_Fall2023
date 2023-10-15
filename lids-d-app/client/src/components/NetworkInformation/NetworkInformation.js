import React from 'react';
import { Link } from 'react-router-dom';
import MenuOptions from '../MenuOptions/MenuOptions';

class NetworkInformation extends React.Component {
    render() {
        return (
            <div className="network-info-container">

                <div className="recognized-devices">
                    <div className="overlay-title">Recognized Devices</div>
                    <div className="devices-toolbar">
                        {/* Display recognized devices info like ID number, Name, IP address, and Connection Status */}
                    </div>
                </div>

                <div className="unknown-devices">
                    <div className="overlay-title">Unknown Devices</div>
                    <div className="devices-toolbar">
                        {/* Display unknown devices info like IP address, Port number, and Protocol used */}
                    </div>
                </div>

                <div className="alerts-textbox">
                    Alerts:
                    {/* Display alerts here */}
                </div>

                <div className="alerts-toolbar">
                    {/* Display the alerts info like Level, Time, IP, Port, Protocol, and Description */}
                </div>

                <button>View Node Map</button>

                <MenuOptions />
                <Link to="/network-map">
                    <button>Network Map</button>
                </Link>
            </div>
        );
    }
}

export default NetworkInformation;