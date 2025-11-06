import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';
import '../../styles/SessionManagement.css';

const SessionManagement = () => {
  const navigate = useNavigate();
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editingSession, setEditingSession] = useState(null);
  const [formData, setFormData] = useState({
    title: '',
    teacher: '',
    session_code: '',
    start_time: '',
    end_time: ''
  });

  useEffect(() => {
    if (!api.isAdminAuthenticated()) {
      navigate('/admin/login');
      return;
    }
    fetchSessions();
  }, [navigate]);

  const fetchSessions = async () => {
    try {
      setLoading(true);
      const data = await api.getSessions();
      // Handle both array and paginated response formats
      setSessions(Array.isArray(data) ? data : (data.results || []));
      setError('');
    } catch (err) {
      setError('Failed to load sessions');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Format the data for the API
      const apiData = {
        title: formData.title,
        teacher: formData.teacher,
        start_time: new Date(formData.start_time).toISOString(),
        end_time: new Date(formData.end_time).toISOString()
      };
      
      // Only include session_code if it's provided (not editing)
      if (formData.session_code && !editingSession) {
        apiData.session_code = formData.session_code;
      }
      
      if (editingSession) {
        await api.updateSession(editingSession.id, apiData);
      } else {
        await api.createSession(apiData);
      }
      setShowModal(false);
      setEditingSession(null);
      resetForm();
      fetchSessions();
    } catch (err) {
      setError(editingSession ? 'Failed to update session' : 'Failed to create session');
      console.error(err);
    }
  };

  const handleEdit = (session) => {
    setEditingSession(session);
    
    // Parse start_time and end_time to separate date and time for form fields
    const startDate = new Date(session.start_time);
    const endDate = new Date(session.end_time);
    
    setFormData({
      title: session.title,
      teacher: session.teacher,
      session_code: session.session_code,
      start_time: session.start_time,
      end_time: session.end_time
    });
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this session? This will also delete all associated data.')) {
      try {
        await api.deleteSession(id);
        fetchSessions();
      } catch (err) {
        setError('Failed to delete session');
        console.error(err);
      }
    }
  };

  const handleAddNew = () => {
    resetForm();
    setEditingSession(null);
    setShowModal(true);
  };

  const resetForm = () => {
    setFormData({
      title: '',
      teacher: '',
      session_code: '',
      start_time: '',
      end_time: ''
    });
  };

  const handleLogout = () => {
    api.adminLogout();
    navigate('/admin/login');
  };

  const getStatusBadge = (session) => {
    if (session.is_active) {
      return <span className="badge badge-active">Active</span>;
    }
    const sessionStartDate = new Date(session.start_time);
    const today = new Date();
    if (sessionStartDate > today) {
      return <span className="badge badge-upcoming">Upcoming</span>;
    }
    return <span className="badge badge-completed">Completed</span>;
  };

  if (loading) {
    return (
      <div className="session-management">
        <div className="loading">Loading sessions...</div>
      </div>
    );
  }

  return (
    <div className="session-management">
      <div className="session-header">
        <div className="header-left">
          <h1>Session Management</h1>
          <button className="btn-back" onClick={() => navigate('/admin/dashboard')}>
            ← Back to Dashboard
          </button>
        </div>
        <div className="header-right">
          <button className="btn-primary" onClick={handleAddNew}>
            + Create New Session
          </button>
          <button className="btn-logout" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </div>

      {error && <div className="error-message">{error}</div>}

      <div className="sessions-grid">
        {sessions.length === 0 ? (
          <div className="no-data">
            <p>No sessions found. Create your first session to get started!</p>
          </div>
        ) : (
          sessions.map(session => (
            <div key={session.id} className="session-card">
              <div className="session-card-header">
                <h3>{session.title}</h3>
                {getStatusBadge(session)}
              </div>
              <div className="session-card-body">
                <div className="session-info">
                  <div className="info-row">
                    <span className="info-label">Teacher:</span>
                    <span className="info-value">{session.teacher}</span>
                  </div>
                  <div className="info-row">
                    <span className="info-label">Session Code:</span>
                    <span className="info-value">{session.session_code}</span>
                  </div>
                  <div className="info-row">
                    <span className="info-label">Start Time:</span>
                    <span className="info-value">{new Date(session.start_time).toLocaleString()}</span>
                  </div>
                  <div className="info-row">
                    <span className="info-label">End Time:</span>
                    <span className="info-value">{new Date(session.end_time).toLocaleString()}</span>
                  </div>
                  <div className="info-row">
                    <span className="info-label">Students:</span>
                    <span className="info-value">{session.attendee_count || 0}</span>
                  </div>
                </div>
              </div>
              <div className="session-card-actions">
                <button className="btn-edit" onClick={() => handleEdit(session)}>
                  Edit
                </button>
                <button className="btn-delete" onClick={() => handleDelete(session.id)}>
                  Delete
                </button>
              </div>
            </div>
          ))
        )}
      </div>

      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>{editingSession ? 'Edit Session' : 'Create New Session'}</h2>
              <button className="modal-close" onClick={() => setShowModal(false)}>×</button>
            </div>
            <form onSubmit={handleSubmit} className="session-form">
              <div className="form-group">
                <label htmlFor="title">Session Title *</label>
                <input
                  type="text"
                  id="title"
                  name="title"
                  value={formData.title}
                  onChange={handleInputChange}
                  placeholder="e.g., React Workshop Fall 2025"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="teacher">Teacher Name *</label>
                <input
                  type="text"
                  id="teacher"
                  name="teacher"
                  value={formData.teacher}
                  onChange={handleInputChange}
                  placeholder="e.g., Dr. Smith"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="session_code">Session Code {editingSession ? '' : '(Optional - Auto-generated if empty)'}</label>
                <input
                  type="text"
                  id="session_code"
                  name="session_code"
                  value={formData.session_code}
                  onChange={handleInputChange}
                  placeholder="e.g., REACT2025"
                  disabled={!!editingSession}
                />
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="start_time">Start Date & Time *</label>
                  <input
                    type="datetime-local"
                    id="start_time"
                    name="start_time"
                    value={formData.start_time ? new Date(formData.start_time).toISOString().slice(0, 16) : ''}
                    onChange={handleInputChange}
                    required
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="end_time">End Date & Time *</label>
                  <input
                    type="datetime-local"
                    id="end_time"
                    name="end_time"
                    value={formData.end_time ? new Date(formData.end_time).toISOString().slice(0, 16) : ''}
                    onChange={handleInputChange}
                    required
                  />
                </div>
              </div>

              <div className="form-actions">
                <button type="button" className="btn-cancel" onClick={() => setShowModal(false)}>
                  Cancel
                </button>
                <button type="submit" className="btn-submit">
                  {editingSession ? 'Update Session' : 'Create Session'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default SessionManagement;
