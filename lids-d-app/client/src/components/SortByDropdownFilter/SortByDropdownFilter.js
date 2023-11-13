/**
 * @author X
 * @version 1.0, 05/05/23
*/

import React, { useState } from 'react';
import Axios from "axios";

function SortByDropdownFilter({ onSort }) {
  const [selectedOption, setSelectedOption] = useState('None');
  const [alertListLevel, setAlertListLevel  ] = useState([]);

  const handleChange = (e) => {
    setSelectedOption(e.target.value);
    onSort(e.target.value);
  };

  return (
    // Filter Alerts by Level
    <div className="sort-by-dropdown-filter">
      <label>Filter by Level: </label>
      <select value={selectedOption} onChange={handleChange}>
        <option value="None">None</option>
        <option value="1">1</option>
        <option value="2">2</option>
        <option value="3">3</option>
      </select>
    </div>
  );
}

export default SortByDropdownFilter;
