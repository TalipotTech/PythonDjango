import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import APIService from '../../services/api';
import Alert from '../../components/Alert';
import LoadingSpinner from '../../components/LoadingSpinner';
import './SessionHome.css';

/**
 * SessionHome Component
 * 
 * Main dashboard for a specific session showing:
 * - Session details and status
 * - Countdown timer (if not started)
 * - Quiz timer (if active)
 * - Progress statistics
 * - Start/Resume/View Results buttons
 */
const SessionHome = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const location = useLocation();

  const [session, setSession] = useState(location.state?.session || null);
  const [progress, setProgress] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [message, setMessage] = useState(location.state?.message || '');
  const [sessionStatus, setSessionStatus] = useState('loading'); // 'waiting', 'active', 'expired'
  const [countdown, setCountdown] = useState('');
  const [timeRemaining, setTimeRemaining] = useState('');

  // Get attendee info from localStorage
  const attendeeId = localStorage.getItem('attendee_id');
  const attendeeName = localStorage.getItem('attendee_name');

  useEffect(() => {
    if (!attendeeId) {
      navigate('/');
      return;
    }
    fetchSessionData();
  }, [id]);

  useEffect(() => {
    if (session) {
      updateSessionStatus();
      const interval = setInterval(updateSessionStatus, 1000);
      return () => clearInterval(interval);
    }
  }, [session]);

  const fetchSessionData = async () => {
    setLoading(true);
    setError('');

    try {
      // Fetch session details if not passed via state
      if (!session) {
        const sessionData = await APIService.getSessionById(id);
        setSession(sessionData);
      }

      // Fetch quiz progress
      if (attendeeId) {
        const progressData = await APIService.getQuizProgress(attendeeId, id);
        setProgress(progressData);
      }
    } catch (err) {
      console.error('Error fetching session data:', err);
      setError('Failed to load session details. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const updateSessionStatus = () => {
    if (!session) return;

    const now = new Date();
    const startTime = new Date(session.start_time);
    const endTime = new Date(session.end_time);

    if (now < startTime) {
      // Quiz hasn't started - show countdown
      setSessionStatus('waiting');
      setCountdown(calculateCountdown(now, startTime));
    } else if (now >= startTime && now <= endTime) {
      // Quiz is active - show time remaining
      setSessionStatus('active');
      setTimeRemaining(calculateCountdown(now, endTime));
    } else {
      // Quiz has expired
      setSessionStatus('expired');
    }
  };

  const calculateCountdown = (from, to) => {
    const diff = to - from;
    if (diff <= 0) return 'Starting now...';

    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((diff % (1000 * 60)) / 1000);

    if (days > 0) {
      return `${days}d ${hours}h ${minutes}m ${seconds}s`;
    } else if (hours > 0) {
      return `${hours}h ${minutes}m ${seconds}s`;
    } else if (minutes > 0) {
      return `${minutes}m ${seconds}s`;
    } else {
      return `${seconds}s`;
    }
  };

  const handleStartQuiz = () => {
    navigate(`/student/quiz/${id}`, {
      state: { session, startNew: true }
    });
  };

  const handleResumeQuiz = () => {
    navigate(`/student/quiz/${id}`, {
      state: { session, resume: true }
    });
  };

  const handleViewResults = () => {
    navigate('/student/dashboard', {
      state: { highlightSession: id }
    });
  };

  const handleLogout = () => {
    localStorage.removeItem('attendee_id');
    localStorage.removeItem('attendee_email');
    localStorage.removeItem('attendee_name');
    navigate('/');
  };

  if (loading) {
    return (
      <div className="session-home-page">
        <div className="container text-center py-5">
          <LoadingSpinner message="Loading session..." />
        </div>
      </div>
    );
  }

  if (error || !session) {
    return (
      <div className="session-home-page">
        <div className="container py-5">
          <Alert type="error" message={error || 'Session not found'} />
          <button className="btn btn-primary mt-3" onClick={() => navigate('/')}>
            Back to Home
          </button>
        </div>
      </div>
    );
  }

  const progressStats = progress ? {
    total: progress.total_questions || 0,
    answered: progress.answered || 0,
    pending: progress.pending || 0,
    percentage: progress.total_questions > 0 ? (progress.answered / progress.total_questions) * 100 : 0
  } : { total: 0, answered: 0, pending: 0, percentage: 0 };
  
  const isFullyCompleted = progressStats.answered === progressStats.total && progressStats.total > 0;

  return (
    <div className="session-home-page">
      <div className="container py-4">
        {/* Header */}
        <div className="session-header">
          <div className="d-flex justify-content-between align-items-start mb-4">
            <div>
              <h2 className="mb-2">{session.title}</h2>
              <p className="text-muted mb-0">
                <i className="bi bi-person-circle me-2"></i>
                {session.teacher}
              </p>
            </div>
            <button className="btn btn-outline-danger" onClick={handleLogout}>
              <i className="bi bi-box-arrow-right me-2"></i>
              Logout
            </button>
          </div>

          {message && <Alert type="success" message={message} onClose={() => setMessage('')} />}
        </div>

        <div className="row g-4">
          {/* Left Column - Session Status */}
          <div className="col-lg-8">
            {/* Session Status Card */}
            <div className="status-card">
              {sessionStatus === 'waiting' && (
                <>
                  <div className="status-icon waiting">
                    <i className="bi bi-hourglass-split fs-1"></i>
                  </div>
                  <h3 className="mb-3">Quiz Starts In</h3>
                  <div className="countdown-display">
                    {countdown}
                  </div>
                  <p className="text-muted mt-3">
                    <i className="bi bi-calendar-event me-2"></i>
                    Starts: {new Date(session.start_time).toLocaleString()}
                  </p>
                </>
              )}

              {sessionStatus === 'active' && (
                <>
                  <div className="status-icon active">
                    <i className="bi bi-play-circle fs-1"></i>
                  </div>
                  <h3 className="mb-3">Quiz is Live!</h3>
                  <div className="time-remaining-display">
                    <i className="bi bi-clock me-2"></i>
                    Time Remaining: {timeRemaining}
                  </div>
                  <p className="text-muted mt-3">
                    <i className="bi bi-calendar-x me-2"></i>
                    Ends: {new Date(session.end_time).toLocaleString()}
                  </p>

                  {/* Action Buttons */}
                  <div className="action-buttons mt-4">
                    {progressStats.answered === 0 ? (
                      <button 
                        className="btn btn-success btn-lg"
                        onClick={handleStartQuiz}
                      >
                        <i className="bi bi-play-fill me-2"></i>
                        Start Quiz
                      </button>
                    ) : isFullyCompleted ? (
                      <div className="completed-badge">
                        <i className="bi bi-check-circle-fill me-2"></i>
                        Quiz Completed!
                      </div>
                    ) : (
                      <button 
                        className="btn btn-primary btn-lg"
                        onClick={handleResumeQuiz}
                      >
                        <i className="bi bi-arrow-clockwise me-2"></i>
                        Resume Quiz
                      </button>
                    )}
                  </div>
                </>
              )}

              {sessionStatus === 'expired' && (
                <>
                  <div className="status-icon expired">
                    <i className="bi bi-clock-history fs-1"></i>
                  </div>
                  <h3 className="mb-3">Quiz Ended</h3>
                  <p className="text-muted">
                    <i className="bi bi-calendar-x me-2"></i>
                    Ended: {new Date(session.end_time).toLocaleString()}
                  </p>
                  <button 
                    className="btn btn-primary btn-lg mt-4"
                    onClick={handleViewResults}
                  >
                    <i className="bi bi-file-earmark-text me-2"></i>
                    View Results
                  </button>
                </>
              )}
            </div>
          </div>

          {/* Right Column - Progress Panel */}
          <div className="col-lg-4">
            <div className="progress-panel">
              <h5 className="mb-3">
                <i className="bi bi-bar-chart-line me-2"></i>
                Your Progress
              </h5>

              {/* Progress Stats */}
              <div className="progress-stats">
                <div className="stat-item">
                  <div className="stat-icon">
                    <i className="bi bi-question-circle"></i>
                  </div>
                  <div className="stat-info">
                    <div className="stat-value">{progressStats.total}</div>
                    <div className="stat-label">Total Questions</div>
                  </div>
                </div>

                <div className="stat-item">
                  <div className="stat-icon success">
                    <i className="bi bi-check-circle"></i>
                  </div>
                  <div className="stat-info">
                    <div className="stat-value">{progressStats.answered}</div>
                    <div className="stat-label">Answered</div>
                  </div>
                </div>

                <div className="stat-item">
                  <div className="stat-icon warning">
                    <i className="bi bi-dash-circle"></i>
                  </div>
                  <div className="stat-info">
                    <div className="stat-value">{progressStats.pending}</div>
                    <div className="stat-label">Pending</div>
                  </div>
                </div>
              </div>

              {/* Progress Bar */}
              <div className="progress-bar-container mt-4">
                <div className="d-flex justify-content-between mb-2">
                  <span className="small">Completion</span>
                  <span className="small fw-bold">{progressStats.percentage.toFixed(0)}%</span>
                </div>
                <div className="progress" style={{ height: '12px' }}>
                  <div 
                    className="progress-bar" 
                    role="progressbar" 
                    style={{ width: `${progressStats.percentage}%` }}
                    aria-valuenow={progressStats.percentage}
                    aria-valuemin="0" 
                    aria-valuemax="100"
                  ></div>
                </div>
              </div>

              {/* Additional Info */}
              {progress?.last_answered_at && (
                <div className="last-activity mt-4">
                  <small className="text-muted">
                    <i className="bi bi-clock-history me-2"></i>
                    Last activity: {new Date(progress.last_answered_at).toLocaleString()}
                  </small>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SessionHome;
