/**
 * LOGIN COMPONENT
 * 
 * BEGINNER EXPLANATION:
 * This is a form where users enter username and password to log in.
 * When they submit, it sends a request to Django and saves the login token.
 * 
 * Key React concepts:
 * - useState: Stores data that can change (like form inputs, errors)
 * - useNavigate: Moves to different pages programmatically
 * - async/await: Waits for server response before continuing
 */

import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../../services/api';
import '../../styles/Auth.css';

function Login() {
  // STATE: Variables that React tracks for changes
  const [username, setUsername] = useState('');  // Stores username input
  const [password, setPassword] = useState('');  // Stores password input
  const [error, setError] = useState('');        // Stores error messages
  const [loading, setLoading] = useState(false); // Shows if we're waiting for response

  // NAVIGATION: Hook to change pages
  const navigate = useNavigate();

  /**
   * Handle form submission
   * This function runs when user clicks "Login" button
   */
  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevent page reload on form submit
    setError('');       // Clear any previous errors
    setLoading(true);   // Show loading state

    try {
      // Call API to login (defined in api.js)
      await api.login(username, password);
      
      // If successful, redirect to dashboard
      navigate('/dashboard');
      
    } catch (err) {
      // If login fails, show error message
      const errorMessage = err.response?.data?.detail || 'Login failed. Please check your credentials.';
      setError(errorMessage);
    } finally {
      // Always stop loading, whether success or fail
      setLoading(false);
    }
  };

  // RENDER: What the user sees
  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2>Login</h2>
        <p className="auth-subtitle">Access your account</p>

        {/* Show error message if exists */}
        {error && (
          <div className="alert alert-error">
            {error}
          </div>
        )}

        {/* Login Form */}
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)} // Update state on input change
              placeholder="Enter your username"
              required
              disabled={loading} // Disable while loading
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              required
              disabled={loading}
            />
          </div>

          <button 
            type="submit" 
            className="btn btn-primary btn-block"
            disabled={loading}
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>

        {/* Link to registration page */}
        <p className="auth-footer">
          Don't have an account? <Link to="/register">Register here</Link>
        </p>
      </div>
    </div>
  );
}

export default Login;
