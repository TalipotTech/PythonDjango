import React from 'react';
import './LoadingSpinner.css';

/**
 * Loading Spinner Component
 * 
 * Shows a loading animation when data is being fetched
 * 
 * Props:
 * - message: Optional loading message to display
 * - size: 'sm', 'md', or 'lg' (default: 'md')
 */
const LoadingSpinner = ({ message = 'Loading...', size = 'md' }) => {
  const sizeClasses = {
    sm: 'spinner-border-sm',
    md: '',
    lg: 'spinner-border-lg',
  };

  return (
    <div className="loading-spinner-container">
      <div className={`spinner-border text-primary ${sizeClasses[size]}`} role="status">
        <span className="visually-hidden">{message}</span>
      </div>
      {message && <p className="loading-message mt-3">{message}</p>}
    </div>
  );
};

export default LoadingSpinner;
