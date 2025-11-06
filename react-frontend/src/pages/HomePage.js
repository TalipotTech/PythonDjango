import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import APIService from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';
import Alert from '../components/Alert';
import './HomePage.css';

/**
 * HomePage Component
 * 
 * This is the landing page students see when they first visit the site.
 * Shows active sessions and allows students to join or login.
 */
const HomePage = () => {
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  // Fetch active sessions on component mount
  useEffect(() => {
    fetchActiveSessions();
  }, []);

  const fetchActiveSessions = async () => {
    try {
      setLoading(true);
      const data = await APIService.getActiveSessions();
      setSessions(data.results || data);
    } catch (err) {
      console.error('Error fetching sessions:', err);
      setError('Failed to load sessions. Please refresh the page.');
    } finally {
      setLoading(false);
    }
  };

  // Handle session card click - navigate to email entry
  const handleSessionClick = (session) => {
    navigate(`/session-code-request/${session.id}`, { state: { session } });
  };

  return (
    <div className="homepage">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="container">
          <div className="text-center">
            <h1 className="display-4 fw-bold mb-4">
              Welcome to Ensate Workshops
            </h1>
            <p className="lead mb-4">
              Join interactive quiz sessions, track your progress, and enhance your learning experience.
            </p>
          </div>
        </div>
      </section>

      {/* Active Sessions Section */}
      <section className="sessions-section py-5 bg-light">
        <div className="container">
          <div className="mb-4">
            <h2 className="mb-2">Active Sessions</h2>
            <p className="text-muted mb-0">
              Click on a session to request your session code
            </p>
          </div>

          {error && <Alert type="error" message={error} onClose={() => setError('')} />}
          
          {/* Sessions Grid */}
          {loading ? (
            <LoadingSpinner message="Loading active sessions..." />
          ) : sessions.length === 0 ? (
            <div className="text-center py-5">
              <i className="bi bi-calendar-x fs-1 text-muted"></i>
              <p className="text-muted mt-3">No active sessions available at the moment.</p>
              <p className="text-muted">Check back later or contact your instructor.</p>
            </div>
          ) : (
            <div className="row g-4">
              {sessions.map((session) => (
                <div key={session.id} className="col-md-6 col-lg-4">
                  <div className="session-card" onClick={() => handleSessionClick(session)}>
                    <div className="session-card-header">
                      <h5 className="session-title">{session.title}</h5>
                      <span className="badge bg-success">Active</span>
                    </div>
                    <div className="session-card-body">
                      <div className="session-info">
                        <i className="bi bi-person-circle me-2"></i>
                        <span>{session.teacher}</span>
                      </div>
                      <div className="session-info">
                        <i className="bi bi-calendar me-2"></i>
                        <span>
                          {new Date(session.start_time).toLocaleDateString('en-US', { 
                            month: 'short', 
                            day: 'numeric'
                          })} - {new Date(session.end_time).toLocaleDateString('en-US', { 
                            month: 'short', 
                            day: 'numeric',
                            year: 'numeric'
                          })}
                        </span>
                      </div>
                      <div className="session-info">
                        <i className="bi bi-clock me-2"></i>
                        <span>
                          {new Date(session.start_time).toLocaleTimeString('en-US', {
                            hour: '2-digit', 
                            minute: '2-digit',
                            hour12: true
                          })} - {new Date(session.end_time).toLocaleTimeString('en-US', {
                            hour: '2-digit', 
                            minute: '2-digit',
                            hour12: true
                          })}
                        </span>
                      </div>
                    </div>
                    <div className="session-card-footer">
                      <button className="btn btn-primary w-100">
                        Request Session Code
                        <i className="bi bi-arrow-right ms-2"></i>
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </section>

      {/* Features Section */}
      <section className="features-section py-5">
        <div className="container">
          <h2 className="text-center mb-5">How It Works</h2>
          <div className="row g-4">
            <div className="col-md-4">
              <div className="feature-card text-center">
                <div className="feature-icon mb-3">
                  <i className="bi bi-envelope-check fs-1 text-primary"></i>
                </div>
                <h4>1. Request Session Code</h4>
                <p>Enter your email to receive a unique session code</p>
              </div>
            </div>
            <div className="col-md-4">
              <div className="feature-card text-center">
                <div className="feature-icon mb-3">
                  <i className="bi bi-person-check fs-1 text-success"></i>
                </div>
                <h4>2. Register or Login</h4>
                <p>Create your account or login with existing credentials</p>
              </div>
            </div>
            <div className="col-md-4">
              <div className="feature-card text-center">
                <div className="feature-icon mb-3">
                  <i className="bi bi-clipboard-check fs-1 text-info"></i>
                </div>
                <h4>3. Take the Quiz</h4>
                <p>Answer questions and track your progress in real-time</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="footer py-4 bg-dark text-white">
        <div className="container text-center">
          <p className="mb-0">&copy; 2025 Ensate Workshops. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};

export default HomePage;
