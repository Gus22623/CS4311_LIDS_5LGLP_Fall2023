import React from 'react';
import PropTypes from 'prop-types';
import './ErrorsDisplay.css';

const ErrorsDisplay = ({ errors }) => {
  return (
    <div className="errors-display-container">
      <div className="header">
        <h1 className="error">ERRORS</h1>
      </div>
      <div className="table-container">
        <table className="errors-table">
          <thead>
            <tr>
              <th>Id</th>
              <th>Message</th>
            </tr>
          </thead>
          <tbody>
            {errors.map((error, index) => (
              <tr key={error.id} className={index % 2 === 0 ? "gray-row" : "gray-row"}>
                <td>{error.id}</td>
                <td>{error.message}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

// Sample errors to display
const sampleErrors = [
  { id: '1', message: 'Database connection failed' },
  { id: '2', message: 'User authentication failed' },
  // Add more as needed
];

ErrorsDisplay.propTypes = {
  errors: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.string.isRequired,
      message: PropTypes.string.isRequired,
    })
  ).isRequired,
};

export default function() {
  return <ErrorsDisplay errors={sampleErrors} />;
};

