/**
 * NAVBAR COMPONENT
 * 
 * BEGINNER EXPLANATION:
 * Navigation bar that appears at the top of every page.
 * Shows different links based on whether user is logged in or not.
 */

import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../../services/api';
import '../../styles/Navbar.css';

function Navbar() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [showMobileMenu, setShowMobileMenu] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    // Check login status when component mounts
    setIsLoggedIn(api.isAuthenticated());
  }, []);

  const handleLogout = () => {
    api.logout();
    setIsLoggedIn(false);
    navigate('/');
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        {/* Logo/Brand */}
        <Link to="/" className="navbar-brand">
          Ensate Workshops
        </Link>

        {/* Mobile menu toggle */}
        <button 
          className="navbar-toggle"
          onClick={() => setShowMobileMenu(!showMobileMenu)}
        >
          ☰
        </button>

        {/* Navigation Links */}
        <div className={`navbar-menu ${showMobileMenu ? 'active' : ''}`}>
          <Link to="/" className="navbar-link">Home</Link>
          <Link to="/sessions" className="navbar-link">Sessions</Link>

          {isLoggedIn ? (
            <>
              <Link to="/dashboard" className="navbar-link">Dashboard</Link>
              <button onClick={handleLogout} className="navbar-link btn-logout">
                Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="navbar-link">Login</Link>
              <Link to="/register" className="navbar-link btn-register">
                Register
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
