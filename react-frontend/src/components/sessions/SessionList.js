/**
 * SESSION LIST COMPONENT
 * 
 * BEGINNER EXPLANATION:
 * Shows a list of all available workshop sessions.
 * Users can see active and upcoming sessions, and click to join them.
 * 
 * Key concepts:
 * - useEffect: Runs code when component loads (like fetching data)
 * - map(): Creates HTML for each item in an array
 */

import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../../services/api';
import '../../styles/Sessions.css';

function SessionList() {
  const [sessions, setSessions] = useState([]);     // All sessions
  const [loading, setLoading] = useState(true);     // Loading state
  const [error, setError] = useState('');           // Error message
  const [filter, setFilter] = useState('all');      // Filter: all, active, upcoming

  /**
   * Fetch sessions when component loads
   * useEffect runs after the component renders
   */
  useEffect(() => {
    fetchSessions();
  }, []); // Empty array means "run only once when component mounts"

  /**
   * Fetch sessions from API
   */
  const fetchSessions = async () => {
    try {
      const data = await api.getSessions();
      // data.results contains the array of sessions (Django pagination)
      setSessions(data.results || data);
    } catch (err) {
      setError('Failed to load sessions. Please try again later.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Filter sessions based on selected filter
   */
  const getFilteredSessions = () => {
    if (filter === 'active') {
      return sessions.filter(session => session.is_active);
    } else if (filter === 'upcoming') {
      return sessions.filter(session => !session.is_active && session.time_until_start > 0);
    }
    return sessions; // 'all'
  };

  /**
   * Format time remaining for display
   */
  const formatTimeRemaining = (seconds) => {
    if (seconds <= 0) return 'Session ended';
    
    const days = Math.floor(seconds / 86400);
    const hours = Math.floor((seconds % 86400) / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    
    if (days > 0) return `${days}d ${hours}h remaining`;
    if (hours > 0) return `${hours}h ${minutes}m remaining`;
    return `${minutes}m remaining`;
  };

  // Show loading spinner
  if (loading) {
    return (
      <div className="container">
        <div className="loading">
          <div className="spinner"></div>
          <p>Loading sessions...</p>
        </div>
      </div>
    );
  }

  // Show error message
  if (error) {
    return (
      <div className="container">
        <div className="alert alert-error">{error}</div>
      </div>
    );
  }

  const filteredSessions = getFilteredSessions();

  return (
    <div className="container">
      <div className="page-header">
        <h1>Workshop Sessions</h1>
        <p>Browse and join available workshops</p>
      </div>

      {/* Filter Buttons */}
      <div className="filter-tabs">
        <button 
          className={filter === 'all' ? 'tab-active' : ''}
          onClick={() => setFilter('all')}
        >
          All Sessions ({sessions.length})
        </button>
        <button 
          className={filter === 'active' ? 'tab-active' : ''}
          onClick={() => setFilter('active')}
        >
          Active Now ({sessions.filter(s => s.is_active).length})
        </button>
        <button 
          className={filter === 'upcoming' ? 'tab-active' : ''}
          onClick={() => setFilter('upcoming')}
        >
          Upcoming ({sessions.filter(s => !s.is_active && s.time_until_start > 0).length})
        </button>
      </div>

      {/* Sessions Grid */}
      {filteredSessions.length === 0 ? (
        <div className="empty-state">
          <p>No {filter !== 'all' ? filter : ''} sessions found</p>
        </div>
      ) : (
        <div className="sessions-grid">
          {filteredSessions.map((session) => (
            <div key={session.id} className="session-card">
              {/* Session Status Badge */}
              <div className="session-header">
                {session.is_active ? (
                  <span className="badge badge-success">● Active Now</span>
                ) : (
                  <span className="badge badge-secondary">Upcoming</span>
                )}
              </div>

              {/* Session Info */}
              <h3>{session.title}</h3>
              <p className="session-teacher">
                <strong>Teacher:</strong> {session.teacher}
              </p>
              <p className="session-code">
                <strong>Session Code:</strong> 
                <code>{session.session_code}</code>
              </p>

              {/* Time Info */}
              <div className="session-time">
                {session.is_active ? (
                  <p className="time-remaining">
                    {formatTimeRemaining(session.time_until_end)}
                  </p>
                ) : (
                  <p className="time-remaining">
                    Starts in {formatTimeRemaining(session.time_until_start)}
                  </p>
                )}
              </div>

              {/* Attendee Count */}
              <p className="session-attendees">
                👥 {session.attendee_count} attendees
              </p>

              {/* Action Buttons */}
              <div className="session-actions">
                <Link 
                  to={`/sessions/${session.id}`} 
                  className="btn btn-primary btn-sm"
                >
                  View Details
                </Link>
                <Link 
                  to={`/register/${session.session_code}`} 
                  className="btn btn-outline btn-sm"
                >
                  Join Session
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default SessionList;
