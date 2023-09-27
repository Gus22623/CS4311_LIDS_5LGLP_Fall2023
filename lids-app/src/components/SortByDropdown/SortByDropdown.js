import React, { useState } from 'react';

function SortByDropdown({ onSort }) {
  const [selectedOption, setSelectedOption] = useState('None');

  const handleChange = (e) => {
    setSelectedOption(e.target.value);
    onSort(e.target.value);
  };

  return (
    <div className="sort-by-dropdown">
      <label>Sort by: </label>
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
