/**
 * @author X
 * @version 1.0, 05/05/23
*/

import React, { useState } from 'react';
import './SortByDropdown.css'
import Axios from "axios";

function SortByDropdown({ onSort }) {
  const [selectedOption, setSelectedOption] = useState('None');
  const [alertListLevel, setAlertListLevel  ] = useState([]);

  const handleChange = (e) => {
    setSelectedOption(e.target.value);
    onSort(e.target.value);
  };

  return (
    // Sorting Alerts by specific category
    <div className="sort-by-dropdown">
      <center-label>Sort Alerts By</center-label>
      <select value={selectedOption} onChange={handleChange}>
        <option value="Level">Priority Level</option>
        <option value="Time">Date</option>
        <option value="IP">Source</option>
        <option value="Protocol">Protocol</option>
      </select>
    </div>
  );
}

export default SortByDropdown;
