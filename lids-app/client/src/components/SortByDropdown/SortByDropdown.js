/**
 * @author X
 * @version 1.0, 05/05/23
*/
/**
 * @modifiers
 */

import React, { useState } from 'react';
import Axios from "axios";
import './SortByDropdown.css';

function SortByDropdown({ onSort }) {
  const [selectedOption, setSelectedOption] = useState('None');
  const [alertListLevel, setAlertListLevel  ] = useState([]);

  const handleChange = (e) => {
    setSelectedOption(e.target.value);
    onSort(e.target.value);
  };

  return (
    // Sorting Alerts by specific category
    <div className="sort-by-dropdown" class="sort-by-container">
      <label class="sort-by">Sort by: </label>
      <select value={selectedOption} onChange={handleChange}>
        <option value="Level">Level</option>
        <option value="Time">Time</option>
        <option value="IP">IP</option>
        <option value="None">None</option>
      </select>
    </div>
  );
}

export default SortByDropdown;
