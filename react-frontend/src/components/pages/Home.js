/**
 * HOME PAGE COMPONENT
 * 
 * BEGINNER EXPLANATION:
 * Landing page that users see when they visit your site.
 * Shows welcome message and active sessions.
 */

import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../../services/api';
import '../../styles/Home.css';

function Home() {
  const [activeSessions, setActiveSessions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchActiveSessions();
  }, []);

  const fetchActiveSessions = async () => {
    try {
      const sessions = await api.getActiveSessions();
      setActiveSessions(sessions);
    } catch (err) {
      console.error('Failed to load active sessions');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="home-page">
      {/* Hero Section */}
      <section className="hero">
        <div className="container">
          <h1 className="hero-title">Welcome to Ensate Workshops</h1>
          <p className="hero-subtitle">
            Join interactive workshops and test your knowledge with our quiz system
          </p>
          <div className="hero-actions">
            <Link to="/sessions" className="btn btn-primary btn-lg">
              Browse Sessions
            </Link>
            <Link to="/register" className="btn btn-outline btn-lg">
              Create Account
            </Link>
          </div>
        </div>
      </section>

      {/* Active Sessions Section */}
      <section className="active-sessions-section">
        <div className="container">
          <h2>Active Sessions Now</h2>
          
          {loading ? (
            <p>Loading...</p>
          ) : activeSessions.length === 0 ? (
            <p>No active sessions at the moment. Check back later!</p>
          ) : (
            <div className="sessions-grid">
              {activeSessions.map((session) => (
                <div key={session.id} className="session-card">
                  <span className="badge badge-success">● Live Now</span>
                  <h3>{session.title}</h3>
                  <p>by {session.teacher}</p>
                  <p>👥 {session.attendee_count} attendees</p>
                  <Link 
                    to={`/register/${session.session_code}`}
                    className="btn btn-primary btn-sm"
                  >
                    Join Now
                  </Link>
                </div>
              ))}
            </div>
          )}
        </div>
      </section>

      {/* Features Section */}
      <section className="features-section">
        <div className="container">
          <h2>How It Works</h2>
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">📋</div>
              <h3>1. Browse Sessions</h3>
              <p>Find workshops that interest you</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">✍️</div>
              <h3>2. Register</h3>
              <p>Sign up with your session code</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🎯</div>
              <h3>3. Take Quiz</h3>
              <p>Answer questions and test your knowledge</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">💬</div>
              <h3>4. Share Feedback</h3>
              <p>Help us improve your experience</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

export default Home;
