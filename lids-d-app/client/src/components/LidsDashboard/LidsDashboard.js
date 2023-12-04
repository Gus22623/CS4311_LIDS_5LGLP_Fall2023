/**
 * @author X
 * @version 1.0, 05/05/23
*/
/**
 * @modifiers
 */

import React, { useEffect, useState } from 'react';
import SortByDropdown from '../SortByDropdown/SortByDropdown';
import LidsApp from '../../containers/LidsDApp';
import { useNavigate } from 'react-router-dom'; // Added import
import './LidsDashboard.css';
import Axios from "axios";
import SortByDropdownFilter from '../SortByDropdownFilter/SortByDropdownFilter';

function LidsDashboard() {
  const [alerts, setAlerts] = useState([]);
  const [errors, setErrors] = useState([]);
  const [notifications, setNotifications] = useState([]);
  const [connectionStatus, setConnectionStatus] = useState('Connected');

  const [alertList, setAlertList] = useState([]);
  const [alertListLevel, setAlertListLevel  ] = useState([]);
  const [alertListTime, setAlertListTime  ] = useState([]);
  const [alertListIP, setAlertListIP  ] = useState([]);
  const [alertListProtocol, setAlertListProtocol ] = useState([]);
  const [criteria, setCriteria] = useState('');
  const [filterCriteria, setFilterCriteria] = useState('');
  const [ filterLevel1, setFilterLevel1 ] = useState([]);
  const [ filterLevel2, setFilterLevel2 ] = useState([]);
  const [ filterLevel3, setFilterLevel3 ] = useState([]);
  const [alertListLevel1, setAlertListLevel1  ] = useState([]);
  const [alertListLevel2, setAlertListLevel2 ] = useState([]);
  const [alertListLevel3, setAlertListLevel3  ] = useState([]);

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

  const navigate = useNavigate(); // Added hook

  // Sort Alerts by certain criteria
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
  }
  if (criteria === 'Protocol') {
    Axios.get('http://127.0.0.1:5000/getAlertsProtocol')
      .then((response) => {
        console.log(response.data);
        setAlertListProtocol(response.data);
        setCriteria('Protocol')
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
};
}

// Filter out alerts by certain criteria
const handleFilter = (criteria) => {
  if (criteria === '1') {
    Axios.get('http://127.0.0.1:5000/filterLevel_1')
      .then((response) => {
        console.log(response.data);
        setAlertListLevel1(response.data);
        setFilterCriteria('1')
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  }
  if (criteria === '2') {
    Axios.get('http://127.0.0.1:5000/filterLevel_2')
      .then((response) => {
        console.log(response.data);
        setAlertListLevel2(response.data);
        setFilterCriteria('2')
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  }
  if (criteria === '3') {
    Axios.get('http://127.0.0.1:5000/filterLevel_3')
      .then((response) => {
        console.log(response.data);
        setAlertListLevel3(response.data);
        setFilterCriteria('3')
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
};
}

  const handleDisconnect = () => {
    setConnectionStatus('Disconnected');
  };

  const handleConfigureServer = () => { // Added function
    navigate('/config-server');
  };

  const handleViewAlerts = () => {
    navigate('/view-alerts')
  };
  
  const handleNetworkInfo = () => {
    navigate('/network-info')
  };
  const handleExportAlerts = () => {
    navigate('/export-alerts')
  };

  return (
    <div className="lids-dashboard">
      <div className="top-section">
      
      <button className="go-back-button" onClick={handleNetworkInfo}>Network Information</button>
      <button className="go-back-button" onClick={handleExportAlerts}>Export Alerts</button>
        <h1 className="h1-custom">LIDS D</h1>
      </div>
      <div className="lids-ip-connection">
        <div className="connection-status">{connectionStatus}</div>
      </div>
      <div className="bottom-section">
        {/* Index Table with Filtered Alerts */}
        <SortByDropdownFilter onSort={handleFilter} />
        {filterCriteria === "1" ? (
            <div className="filter-section">
              <table className="filter-table">
                <thead>
                  <tr>
                    <th>Lvl</th>
                    <th>Time</th>
                    <th>Source IP</th>
                    <th>Dest IP</th>
                    <th>Port</th>
                    <th>Description</th>
                  </tr>
                </thead>
                <tbody>
                  {alertListLevel1.map((val, index) => (
                    <tr key={index} className={`level-${val.level}`}>
                      <td>{val.level}</td>
                      <td>{val.time}</td>
                      <td>{val.source_ip}</td>
                      <td>{val.dest_ip}</td>
                      <td>{val.port}</td>
                      <td>{val.desc}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : filterCriteria === "2" ? (
            <div className="filter-section">
              <table className="filter-table">
                <thead>
                  <tr>
                    <th>Lvl</th>
                    <th>Time</th>
                    <th>Source IP</th>
                    <th>Dest IP</th>
                    <th>Port</th>
                    <th>Description</th>
                  </tr>
                </thead>
                <tbody>
                  {alertListLevel2.map((val, index) => (
                    <tr key={index} className={`level-${val.level}`}>
                      <td>{val.level}</td>
                      <td>{val.time}</td>
                      <td>{val.source_ip}</td>
                      <td>{val.dest_ip}</td>
                      <td>{val.port}</td>
                      <td>{val.desc}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : filterCriteria === "3" ? (
            <div className="filter-section">
              <table className="filter-table">
                <thead>
                  <tr>
                    <th>Lvl</th>
                    <th>Time</th>
                    <th>Source IP</th>
                    <th>Dest IP</th>
                    <th>Port</th>
                    <th>Description</th>
                  </tr>
                </thead>
                <tbody>
                  {alertListLevel3.map((val, index) => (
                    <tr key={index} className={`level-${val.level}`}>
                      <td>{val.level}</td>
                      <td>{val.time}</td>
                      <td>{val.source_ip}</td>
                      <td>{val.dest_ip}</td>
                      <td>{val.port}</td>
                      <td>{val.desc}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="fitler-section">
              <table className="filter-table">
              </table>
            </div>
          )}

        {/*END OF FILTER*/}
        
        {/* Index Table with Sorted Alerts */}
        <SortByDropdown onSort={handleSort} />

        {criteria === "Level" ? (
            <div className="table-container">
              <table className="alert-table">
                <thead>
                  <tr>
                    <th>Lvl</th>
                    <th>Time</th>
                    <th>Source IP</th>
                    <th>Dest IP</th>
                    <th>Port</th>
                    <th>Protocol</th>
                    <th>Description</th>
                  </tr>
                </thead>
                <tbody>
                  {alertListLevel.map((val, index) => (
                    <tr key={index} className={`level-${val.level}`}>
                      <td>{val.level}</td>
                      <td>{val.time}</td>
                      <td>{val.source_ip}</td>
                      <td>{val.dest_ip}</td>
                      <td>{val.port}</td>
                      <td>{val.protocol}</td>
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
                    <th>Source IP</th>
                    <th>Dest IP</th>
                    <th>Port</th>
                    <th>Protocol</th>
                    <th>Description</th>
                  </tr>
                </thead>
                <tbody>
                  {alertListTime.map((val, index) => (
                    <tr key={index} className={`level-${val.level}`}>
                      <td>{val.level}</td>
                      <td>{val.time}</td>
                      <td>{val.source_ip}</td>
                      <td>{val.dest_ip}</td>
                      <td>{val.port}</td>
                      <td>{val.protocol}</td>
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
                    <th>Source IP</th>
                    <th>Dest IP</th>
                    <th>Port</th>
                    <th>Protocol</th>
                    <th>Description</th>
                  </tr>
                </thead>
                <tbody>
                  {alertListIP.map((val, index) => (
                    <tr key={index} className={`level-${val.level}`}>
                      <td>{val.level}</td>
                      <td>{val.time}</td>
                      <td>{val.source_ip}</td>
                      <td>{val.dest_ip}</td>
                      <td>{val.port}</td>
                      <td>{val.protocol}</td>
                      <td>{val.desc}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : criteria === "Protocol" ? (
            <div className="table-container">
              <table className="alert-table">
                <thead>
                  <tr>
                    <th>Lvl</th>
                    <th>Time</th>
                    <th>Source IP</th>
                    <th>Dest IP</th>
                    <th>Port</th>
                    <th>Protocol</th>
                    <th>Description</th>
                  </tr>
                </thead>
                <tbody>
                  {alertListProtocol.map((val, index) => (
                    <tr key={index} className={`level-${val.level}`}>
                      <td>{val.level}</td>
                      <td>{val.time}</td>
                      <td>{val.source_ip}</td>
                      <td>{val.dest_ip}</td>
                      <td>{val.port}</td>
                      <td>{val.protocol}</td>
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
                    <th>Source IP</th>
                    <th>Dest IP</th>
                    <th>Port</th>
                    <th>Protocol</th>
                    <th>Description</th>
                  </tr>
                </thead>
                <tbody>
                  {alertList.map((val, index) => (
                    <tr key={index} className={`level-${val.level}`}>
                      <td>{val.level}</td>
                      <td>{val.time}</td>
                      <td>{val.source_ip}</td>
                      <td>{val.dest_ip}</td>
                      <td>{val.port}</td>
                      <td>{val.protocol}</td>
                      <td>{val.desc}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}        
          
      </div>
    </div>
  );
}

export default LidsDashboard;
