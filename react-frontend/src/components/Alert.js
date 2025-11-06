import React from 'react';
import './Alert.css';

/**
 * Alert Component
 * 
 * Displays success, error, warning, or info messages
 * 
 * Props:
 * - type: 'success', 'error', 'warning', 'info' (default: 'info')
 * - message: The message to display
 * - onClose: Optional callback when alert is dismissed
 * - dismissible: Whether alert can be closed (default: true)
 */
const Alert = ({ type = 'info', message, onClose, dismissible = true }) => {
  const alertTypes = {
    success: 'alert-success',
    error: 'alert-danger',
    warning: 'alert-warning',
    info: 'alert-info',
  };

  const icons = {
    success: '✓',
    error: '✕',
    warning: '⚠',
    info: 'ℹ',
  };

  if (!message) return null;

  return (
    <div className={`alert ${alertTypes[type]} ${dismissible ? 'alert-dismissible fade show' : ''}`} role="alert">
      <span className="alert-icon">{icons[type]}</span>
      <span className="alert-message">{message}</span>
      {dismissible && onClose && (
        <button type="button" className="btn-close" onClick={onClose} aria-label="Close"></button>
      )}
    </div>
  );
};

export default Alert;
