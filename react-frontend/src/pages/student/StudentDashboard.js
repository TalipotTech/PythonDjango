import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import APIService from '../../services/api';
import LoadingSpinner from '../../components/LoadingSpinner';
import Alert from '../../components/Alert';
import './StudentDashboard.css';

/**
 * StudentDashboard Component
 * 
 * Shows student's enrolled sessions, quiz status, scores, and history
 */
const StudentDashboard = () => {
  const navigate = useNavigate();
  
  const [attendeeData, setAttendeeData] = useState(null);
  const [sessions, setSessions] = useState([]);
  const [completedSessionIds, setCompletedSessionIds] = useState([]);
  const [completedSessions, setCompletedSessions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Get attendee info from localStorage
  const attendeeId = localStorage.getItem('attendee_id');
  const attendeeEmail = localStorage.getItem('attendee_email');
  const attendeeName = localStorage.getItem('attendee_name');

  useEffect(() => {
    if (!attendeeId) {
      navigate('/');
      return;
    }
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      
      // Fetch attendee details
      const attendee = await APIService.getAttendeeById(attendeeId);
      setAttendeeData(attendee);

      // Fetch completed session IDs
      const completedData = await APIService.getCompletedSessions(attendeeId);
      const completedIds = completedData.completed_session_ids || [];
      setCompletedSessionIds(completedIds);

      // Fetch all active sessions
      const sessionsData = await APIService.getActiveSessions();
      
      // Separate completed and available sessions
      const now = new Date();
      const availableSessions = [];
      const completedSessionsList = [];
      
      sessionsData.forEach(session => {
        const endTime = new Date(session.end_time);
        const isExpired = now > endTime;
        const isCompleted = completedIds.includes(session.id);
        
        if (isCompleted) {
          completedSessionsList.push(session);
        } else if (!isExpired) {
          availableSessions.push(session);
        }
      });
      
      setSessions(availableSessions);
      setCompletedSessions(completedSessionsList);
      
    } catch (err) {
      console.error('Error fetching dashboard data:', err);
      setError('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('attendee_id');
    localStorage.removeItem('attendee_email');
    localStorage.removeItem('attendee_name');
    navigate('/');
  };

  const getSessionStatus = (session) => {
    const now = new Date();
    const startTime = new Date(session.start_time);
    const endTime = new Date(session.end_time);

    if (now < startTime) return { label: 'Upcoming', class: 'status-upcoming' };
    if (now > endTime) return { label: 'Completed', class: 'status-completed' };
    return { label: 'Active', class: 'status-active' };
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
      <div className="student-dashboard-page">
        <div className="container text-center py-5">
          <LoadingSpinner message="Loading dashboard..." />
        </div>
      </div>
    );
  }

  return (
    <div className="student-dashboard-page">
      <div className="container">
        {/* Header */}
        <div className="dashboard-header">
          <div className="welcome-section">
            <h1>Welcome back, {attendeeName}!</h1>
            <p className="text-muted">{attendeeEmail}</p>
          </div>
          <div className="header-actions">
            <button className="btn btn-outline-primary" onClick={() => navigate('/')}>
              <i className="bi bi-house me-2"></i>
              Home
            </button>
            <button className="btn btn-outline-secondary" onClick={handleLogout}>
              <i className="bi bi-box-arrow-right me-2"></i>
              Logout
            </button>
          </div>
        </div>

        {error && <Alert type="error" message={error} onClose={() => setError('')} />}

        {/* Stats Cards */}
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-icon">
              <i className="bi bi-clipboard-check"></i>
            </div>
            <div className="stat-content">
              <h3>{completedSessionIds.length}</h3>
              <p>Completed Sessions</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">
              <i className="bi bi-calendar-event"></i>
            </div>
            <div className="stat-content">
              <h3>{attendeeData?.class_session ? 1 : 0}</h3>
              <p>Current Session</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">
              <i className="bi bi-graph-up"></i>
            </div>
            <div className="stat-content">
              <h3>{sessions.length}</h3>
              <p>Available Sessions</p>
            </div>
          </div>
        </div>

        {/* Current Session */}
        {attendeeData?.class_session && (
          <div className="section">
            <h2 className="section-title">
              <i className="bi bi-bookmark-fill me-2"></i>
              My Current Session
            </h2>
            <div className="current-session-card">
              <div className="session-info">
                <h3>{attendeeData.session_title || `Session #${attendeeData.class_session}`}</h3>
                <div className="session-meta">
                  <span>
                    <i className="bi bi-person-circle me-1"></i>
                    Enrolled
                  </span>
                  <span className={`status-badge ${attendeeData.has_submitted ? 'status-completed' : 'status-active'}`}>
                    {attendeeData.has_submitted ? 'Quiz Completed' : 'In Progress'}
                  </span>
                </div>
              </div>
              {!attendeeData.has_submitted && (
                <div className="session-actions">
                  <button 
                    className="btn btn-primary"
                    onClick={() => navigate(`/student/quiz/${attendeeData.class_session}`)}
                  >
                    <i className="bi bi-play-circle me-2"></i>
                    Take Quiz
                  </button>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Available Sessions */}
        <div className="section">
          <h2 className="section-title">
            <i className="bi bi-calendar3 me-2"></i>
            Available Sessions
          </h2>
          
          {sessions.length === 0 ? (
            <div className="empty-state">
              <i className="bi bi-calendar-x"></i>
              <p>No other sessions available at the moment</p>
            </div>
          ) : (
            <div className="sessions-grid">
              {sessions.map((session) => {
                const status = getSessionStatus(session);
                
                return (
                  <div 
                    key={session.id} 
                    className="session-card"
                  >
                    <div className="session-header">
                      <h3>{session.title}</h3>
                      <span className={`status-badge ${status.class}`}>
                        {status.label}
                      </span>
                    </div>
                    
                    <div className="session-details">
                      <div className="detail-row">
                        <i className="bi bi-person-circle"></i>
                        <span>{session.teacher}</span>
                      </div>
                      <div className="detail-row">
                        <i className="bi bi-calendar"></i>
                        <span>{formatDate(session.start_time)}</span>
                      </div>
                      <div className="detail-row">
                        <i className="bi bi-key"></i>
                        <span>Code: {session.session_code}</span>
                      </div>
                    </div>
                    
                    <div className="session-footer">
                      <button 
                        className="btn btn-primary w-100"
                        onClick={() => navigate('/')}
                      >
                        <i className="bi bi-box-arrow-in-right me-2"></i>
                        Join with Code
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Completed Sessions History */}
        {completedSessions.length > 0 && (
          <div className="section">
            <h2 className="section-title">
              <i className="bi bi-check-circle me-2"></i>
              Completed Sessions History
            </h2>
            
            <div className="sessions-grid">
              {completedSessions.map((session) => (
                <div 
                  key={session.id} 
                  className="session-card completed"
                  style={{ opacity: 0.85, border: '2px solid #10b981' }}
                >
                  <div className="completed-badge" style={{
                    position: 'absolute',
                    top: '1rem',
                    right: '1rem',
                    backgroundColor: '#10b981',
                    color: 'white',
                    padding: '0.375rem 0.875rem',
                    borderRadius: '9999px',
                    fontSize: '0.8125rem',
                    fontWeight: '600'
                  }}>
                    <i className="bi bi-check-circle-fill me-1"></i>
                    Completed
                  </div>
                  
                  <div className="session-header">
                    <h3>{session.title}</h3>
                  </div>
                  
                  <div className="session-details">
                    <div className="detail-row">
                      <i className="bi bi-person-circle"></i>
                      <span>{session.teacher}</span>
                    </div>
                    <div className="detail-row">
                      <i className="bi bi-calendar"></i>
                      <span>{formatDate(session.start_time)}</span>
                    </div>
                    <div className="detail-row">
                      <i className="bi bi-award"></i>
                      <span>Quiz Submitted</span>
                    </div>
                  </div>
                  
                  <div className="session-footer">
                    <div className="text-center text-success py-2" style={{ fontWeight: '600' }}>
                      <i className="bi bi-lock-fill me-2"></i>
                      Session Completed
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

      </div>
    </div>
  );
};

export default StudentDashboard;
