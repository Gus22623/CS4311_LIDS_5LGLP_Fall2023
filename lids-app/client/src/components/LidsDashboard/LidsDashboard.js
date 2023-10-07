import React, { useEffect, useState } from 'react';
import AlertsDisplay from '../AlertDisplay/AlertDisplay';
import ErrorsDisplay from '../ErrorsDisplay/ErrorsDisplay';
import NotificationsDisplay from '../NotificationsDisplay/NotificationsDisplay';
import SortByDropdown from '../SortByDropdown/SortByDropdown';
import './LidsDashboard.css';
import Axios from "axios";

function LidsDashboard() {
  const [alerts, setAlerts] = useState([]);
  const [errors, setErrors] = useState([]);
  const [notifications, setNotifications] = useState([]);
  const [connectionStatus, setConnectionStatus] = useState('Connected');
  const [alertList, setAlertList] = useState([]);
  const [alertListLevel, setAlertListLevel  ] = useState([]);
  const [alertListTime, setAlertListTime  ] = useState([]);
  const [alertListIP, setAlertListIP  ] = useState([]);
  const [criteria, setCriteria] = useState('');

  useEffect(() => {
    const ourRequest = Axios.CancelToken.source()
    Axios.get('http://127.0.0.1:5000/getAlerts', {
      CancelToken: ourRequest.token
    })
      .then((response)=> {
        console.log(response.data);
        setAlertList(response.data);
      })
      .catch((error) => {
        if (Axios.isCancel(error)) {
          console.log('Request cancelled:', error.message);
        } else {
          console.error('ERROR:', error);
        }
      });
    return () => {
      ourRequest.cancel('Component unmounted');
    };
  }, []); 


  const handleSort = (criteria) => {
    if (criteria === 'Level') {
      //const sortedAlerts = [...alerts].sort((a, b) => a.level - b.level);
      //setAlerts(sortedAlerts);
      Axios.get('http://127.0.0.1:5000/getAlertsLevel')
        .then((response) => {
          console.log(response.data);
          setAlertListLevel(response.data);
          setCriteria('Level')
        })
        .catch((error) => {
          console.error("Error fetching data:", error);
        });
    }
    if (criteria === 'Time') {
      Axios.get('http://127.0.0.1:5000/getAlertsTime')
        .then((response) => {
          console.log(response.data);
          setAlertListTime(response.data);
          setCriteria('Time')
        })
        .catch((error) => {
          console.error("Error fetching data:", error);
        });
    }
    if (criteria === 'IP') {
      Axios.get('http://127.0.0.1:5000/getAlertsIP')
        .then((response) => {
          console.log(response.data);
          setAlertListIP(response.data);
          setCriteria('IP')
        })
        .catch((error) => {
          console.error("Error fetching data:", error);
        });
  };
}

  const handleDisconnect = () => {
    setConnectionStatus('Disconnected');
  };

  return (
    <div className="lids-dashboard">
      <div className="top-section">
      <button className="go-back-button">Go Back</button>
        <h1 className="h1-custom">LIDS Dashboard</h1>
      </div>
      <div className="lids-ip-connection">
        <div className="lids-ip">LIDS IP: 192.168.1.100</div>
        <div></div>
        <div className="connection-status">{connectionStatus}</div>
      </div>
      <div className="bottom-section">
        <SortByDropdown onSort={handleSort} />
        {/* <AlertsDisplay alerts={alerts} /> */}
        {criteria === "Level" ? (
            <div className="table-container">
              <table className="alert-table">
                <thead>
                  <tr>
                    <th>Lvl</th>
                    <th>Time</th>
                    <th>IP</th>
                    <th>Port</th>
                    <th>Description</th>
                  </tr>
                </thead>
                <tbody>
                  {alertListLevel.map((val, index) => (
                    <tr key={index}>
                      <td>{val.level}</td>
                      <td>{val.time}</td>
                      <td>{val.source_ip}</td>
                      <td>{val.port}</td>
                      <td>{val.desc}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : criteria === "Time" ? (
            <div className="table-container">
              <table className="alert-table">
                <thead>
                  <tr>
                    <th>Lvl</th>
                    <th>Time</th>
                    <th>IP</th>
                    <th>Port</th>
                    <th>Description</th>
                  </tr>
                </thead>
                <tbody>
                  {alertListTime.map((val, index) => (
                    <tr key={index}>
                      <td>{val.level}</td>
                      <td>{val.time}</td>
                      <td>{val.source_ip}</td>
                      <td>{val.port}</td>
                      <td>{val.desc}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : criteria === "IP" ? (
            <div className="table-container">
              <table className="alert-table">
                <thead>
                  <tr>
                    <th>Lvl</th>
                    <th>Time</th>
                    <th>IP</th>
                    <th>Port</th>
                    <th>Description</th>
                  </tr>
                </thead>
                <tbody>
                  {alertListIP.map((val, index) => (
                    <tr key={index}>
                      <td>{val.level}</td>
                      <td>{val.time}</td>
                      <td>{val.source_ip}</td>
                      <td>{val.port}</td>
                      <td>{val.desc}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="table-container">
              <table className="alert-table">
                <thead>
                  <tr>
                    <th>Lvl</th>
                    <th>Time</th>
                    <th>IP</th>
                    <th>Port</th>
                    <th>Description</th>
                  </tr>
                </thead>
                <tbody>
                  {alertList.map((val, index) => (
                    <tr key={index}>
                      <td>{val.level}</td>
                      <td>{val.time}</td>
                      <td>{val.source_ip}</td>
                      <td>{val.port}</td>
                      <td>{val.desc}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}        
          
        <ErrorsDisplay errors={errors} />
        <NotificationsDisplay notifications={notifications} />
      </div>
      <div className="disconnect-button-container">
        <button className="disconnect-button" onClick={handleDisconnect}>
          Disconnect
        </button>
      </div>
    </div>
  );
}

export default LidsDashboard;
