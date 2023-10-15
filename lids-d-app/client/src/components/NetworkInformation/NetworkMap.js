import React from 'react';
import { Link } from 'react-router-dom';
import { useNavigate } from 'react-router-dom'; // Added import
//import * as d3 from 'd3';

function DeviceNode({ device }) {
    const color = device.status === 'recognized' ? 'green' : 'red';
    return (
        
        <circle cx={device.x} cy={device.y} r={10} fill={color} />
    );
}

function NetworkMap() {
    // For simplicity, we're using static data here.
    const [devices, setDevices] = React.useState([
        { id: 1, name: "Device 1", status: "recognized", x: 50, y: 50 },
        { id: 2, name: "Device 2", status: "unknown", x: 100, y: 100 },
        { id: 3, name: "Device 3", status: "recognized", x: 150, y: 150 },
    ]);
/*
function NetworkMap() {
    const [devices, setDevices] = React.useState([]);

    React.useEffect(() => {
        fetch("/api/devices")
            .then(response => response.json())
            .then(data => {
                // Assuming the API returns an array of devices
                setDevices(data);
            });
    }, []);
    */
    const navigate = useNavigate(); // Added hook

    const handleConfigureServer = () => { // Added function
        navigate('/config-server');
      };
    
      const handleViewAlerts = () => {
        navigate('/view-alerts')
      };
      
      const handleNetworkInfo = () => {
        navigate('/network-map')
      };

    return (
        <div>
            <button className="go-back-button" onClick={handleConfigureServer}>Configure Server</button>
            <button className="go-back-button" onClick={handleViewAlerts}>View Alerts</button>
            <button className="go-back-button" onClick={handleNetworkInfo}>Network Information</button>
            <svg width="400" height="400">
                {devices.map(device => (
                    <DeviceNode key={device.id} device={device} />
                ))}
            </svg>

            <Link to="/network-info">
                <button>Network Info</button>
            </Link>
        </div>
    );
}

export default NetworkMap;