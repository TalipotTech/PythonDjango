import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';
import '../../styles/FeedbackManagement.css';

const FeedbackManagement = () => {
  const navigate = useNavigate();
  const [feedback, setFeedback] = useState([]);
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedSession, setSelectedSession] = useState('all');
  const [selectedType, setSelectedType] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [showDetailModal, setShowDetailModal] = useState(false);
  const [selectedFeedback, setSelectedFeedback] = useState(null);

  useEffect(() => {
    if (!api.isAdminAuthenticated()) {
      navigate('/admin/login');
      return;
    }
    fetchData();
  }, [navigate]);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [feedbackData, sessionsData] = await Promise.all([
        api.getAllFeedback(),
        api.getSessions()
      ]);
      
      setFeedback(Array.isArray(feedbackData) ? feedbackData : (feedbackData.results || []));
      setSessions(Array.isArray(sessionsData) ? sessionsData : (sessionsData.results || []));
      setError('');
    } catch (err) {
      setError('Failed to load feedback data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this feedback?')) {
      return;
    }

    try {
      await api.deleteFeedback(id);
      setFeedback(feedback.filter(f => f.id !== id));
      setError('');
    } catch (err) {
      setError('Failed to delete feedback');
      console.error(err);
    }
  };

  const handleViewDetails = (feedbackItem) => {
    setSelectedFeedback(feedbackItem);
    setShowDetailModal(true);
  };

  const handleLogout = () => {
    api.clearAdminTokens();
    navigate('/admin/login');
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getSessionTitle = (sessionId) => {
    if (!sessionId) return 'No Session';
    const session = sessions.find(s => s.id === sessionId);
    return session ? session.title : 'Unknown Session';
  };

  const filteredFeedback = feedback.filter(item => {
    const sessionId = item.attendee?.class_session?.id || item.attendee?.class_session;
    const matchesSession = selectedSession === 'all' || 
                          sessionId === parseInt(selectedSession);
    const matchesType = selectedType === 'all' || item.feedback_type === selectedType;
    const matchesSearch = searchTerm === '' || 
                         item.content.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         item.attendee?.name?.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesSession && matchesType && matchesSearch;
  });

  return (
    <div className="feedback-management">
      <div className="management-header">
        <div className="header-left">
          <button onClick={() => navigate('/admin/dashboard')} className="btn-back">
            <i className="fas fa-arrow-left"></i> Back to Dashboard
          </button>
          <h1>Feedback Management</h1>
        </div>
        <button onClick={handleLogout} className="btn-logout">
          <i className="fas fa-sign-out-alt"></i> Logout
        </button>
      </div>

      {error && <div className="alert alert-danger">{error}</div>}

      <div className="filters-section">
        <div className="filter-group">
          <label>Filter by Session:</label>
          <select 
            value={selectedSession}
            onChange={(e) => setSelectedSession(e.target.value)}
            className="form-select"
          >
            <option value="all">All Sessions</option>
            {sessions.map(session => (
              <option key={session.id} value={session.id}>
                {session.title}
              </option>
            ))}
          </select>
        </div>

        <div className="filter-group">
          <label>Filter by Type:</label>
          <select 
            value={selectedType}
            onChange={(e) => setSelectedType(e.target.value)}
            className="form-select"
          >
            <option value="all">All Types</option>
            <option value="quiz">Quiz Feedback</option>
            <option value="review">General Review</option>
          </select>
        </div>

        <div className="filter-group flex-grow">
          <label>Search:</label>
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search by student name or content..."
            className="form-control"
          />
        </div>
      </div>

      <div className="feedback-stats">
        <div className="stat-card">
          <i className="fas fa-comments"></i>
          <div>
            <div className="stat-number">{filteredFeedback.length}</div>
            <div className="stat-label">Total Feedback</div>
          </div>
        </div>
        <div className="stat-card">
          <i className="fas fa-clipboard-check"></i>
          <div>
            <div className="stat-number">
              {filteredFeedback.filter(f => f.feedback_type === 'quiz').length}
            </div>
            <div className="stat-label">Quiz Feedback</div>
          </div>
        </div>
        <div className="stat-card">
          <i className="fas fa-star"></i>
          <div>
            <div className="stat-number">
              {filteredFeedback.filter(f => f.feedback_type === 'review').length}
            </div>
            <div className="stat-label">General Reviews</div>
          </div>
        </div>
      </div>

      {loading ? (
        <div className="loading">
          <i className="fas fa-spinner fa-spin"></i> Loading feedback...
        </div>
      ) : filteredFeedback.length === 0 ? (
        <div className="no-data">
          <i className="fas fa-inbox"></i>
          <p>No feedback found</p>
        </div>
      ) : (
        <div className="feedback-grid">
          {filteredFeedback.map(item => (
            <div key={item.id} className="feedback-card">
              <div className="feedback-header">
                <div className="student-info">
                  <i className="fas fa-user-circle"></i>
                  <div>
                    <div className="student-name">{item.attendee?.name || 'Unknown'}</div>
                    <div className="student-email">{item.attendee?.email || ''}</div>
                  </div>
                </div>
                <span className={`feedback-type-badge ${item.feedback_type}`}>
                  <i className={`fas ${item.feedback_type === 'quiz' ? 'fa-clipboard-check' : 'fa-star'}`}></i>
                  {item.feedback_type === 'quiz' ? 'Quiz' : 'Review'}
                </span>
              </div>

              <div className="feedback-content">
                <p>{item.content.length > 150 ? item.content.substring(0, 150) + '...' : item.content}</p>
              </div>

              <div className="feedback-meta">
                <div className="meta-item">
                  <i className="fas fa-chalkboard"></i>
                  <span>{item.session_title || getSessionTitle(item.attendee?.class_session?.id || item.attendee?.class_session)}</span>
                </div>
                <div className="meta-item">
                  <i className="fas fa-clock"></i>
                  <span>{formatDate(item.submitted_at)}</span>
                </div>
              </div>

              <div className="feedback-actions">
                <button 
                  onClick={() => handleViewDetails(item)}
                  className="btn-view"
                >
                  <i className="fas fa-eye"></i> View Details
                </button>
                <button 
                  onClick={() => handleDelete(item.id)}
                  className="btn-delete"
                >
                  <i className="fas fa-trash"></i> Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Detail Modal */}
      {showDetailModal && selectedFeedback && (
        <div className="modal-overlay" onClick={() => setShowDetailModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Feedback Details</h2>
              <button onClick={() => setShowDetailModal(false)} className="btn-close">
                <i className="fas fa-times"></i>
              </button>
            </div>
            <div className="modal-body">
              <div className="detail-section">
                <h3>Student Information</h3>
                <div className="detail-grid">
                  <div className="detail-item">
                    <label>Name:</label>
                    <span>{selectedFeedback.attendee?.name || 'N/A'}</span>
                  </div>
                  <div className="detail-item">
                    <label>Email:</label>
                    <span>{selectedFeedback.attendee?.email || 'N/A'}</span>
                  </div>
                  <div className="detail-item">
                    <label>Phone:</label>
                    <span>{selectedFeedback.attendee?.phone || 'N/A'}</span>
                  </div>
                  <div className="detail-item">
                    <label>Session:</label>
                    <span>{selectedFeedback.session_title || getSessionTitle(selectedFeedback.attendee?.class_session?.id || selectedFeedback.attendee?.class_session)}</span>
                  </div>
                </div>
              </div>

              <div className="detail-section">
                <h3>Feedback Information</h3>
                <div className="detail-grid">
                  <div className="detail-item">
                    <label>Type:</label>
                    <span className={`feedback-type-badge ${selectedFeedback.feedback_type}`}>
                      <i className={`fas ${selectedFeedback.feedback_type === 'quiz' ? 'fa-clipboard-check' : 'fa-star'}`}></i>
                      {selectedFeedback.feedback_type === 'quiz' ? 'Quiz Feedback' : 'General Review'}
                    </span>
                  </div>
                  <div className="detail-item">
                    <label>Submitted:</label>
                    <span>{formatDate(selectedFeedback.submitted_at)}</span>
                  </div>
                </div>
              </div>

              <div className="detail-section">
                <h3>Content</h3>
                <div className="feedback-full-content">
                  {selectedFeedback.content}
                </div>
              </div>
            </div>
            <div className="modal-footer">
              <button 
                onClick={() => {
                  setShowDetailModal(false);
                  handleDelete(selectedFeedback.id);
                }}
                className="btn-delete"
              >
                <i className="fas fa-trash"></i> Delete Feedback
              </button>
              <button onClick={() => setShowDetailModal(false)} className="btn-secondary">
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default FeedbackManagement;
