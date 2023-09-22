import React from 'react';

function ErrorsDisplay({ errors }) {
  return (
    <div className="errors-display">
      <h1>Errors</h1>
      {errors.map((error, index) => (
        <div key={index} className="error-item">
          {error.message}
        </div>
      ))}
    </div>
  );
}

export default ErrorsDisplay;
