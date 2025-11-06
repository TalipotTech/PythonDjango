/**
 * Admin Dashboard Component
 * Main dashboard showing statistics, recent activity, and quick actions
 */

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';
import '../../styles/AdminDashboard.css';

const AdminDashboard = () => {
  const navigate = useNavigate();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    // Check authentication
    if (!api.isAdminAuthenticated()) {
      navigate('/admin/login');
      return;
    }

    loadDashboardData();
  }, [navigate]);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      const data = await api.getDashboardStats();
      setStats(data);
    } catch (err) {
      console.error('Failed to load dashboard:', err);
      if (err.response?.status === 401) {
        navigate('/admin/login');
      } else {
        setError('Failed to load dashboard data. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    api.adminLogout();
    navigate('/admin/login');
  };

  if (loading) {
    return (
      <div className="admin-dashboard">
        <div className="loading-container">
          <i className="fas fa-spinner fa-spin"></i>
          <p>Loading dashboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="admin-dashboard">
        <div className="error-container">
          <i className="fas fa-exclamation-triangle"></i>
          <p>{error}</p>
          <button onClick={loadDashboardData} className="retry-button">
            <i className="fas fa-redo"></i>
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="admin-dashboard">
      {/* Header */}
      <div className="dashboard-header">
        <div className="header-left">
          <h1>
            <i className="fas fa-tachometer-alt"></i>
            Admin Dashboard
          </h1>
          <p>Welcome back! Here's what's happening today.</p>
        </div>
        <div className="header-right">
          <button onClick={loadDashboardData} className="refresh-button">
            <i className="fas fa-sync-alt"></i>
            Refresh
          </button>
          <button onClick={handleLogout} className="logout-button">
            <i className="fas fa-sign-out-alt"></i>
            Logout
          </button>
        </div>
      </div>

      {/* Statistics Cards */}
      <div className="stats-grid">
        {/* Sessions Stats */}
        <div className="stat-card sessions-card">
          <div className="stat-icon">
            <i className="fas fa-calendar-alt"></i>
          </div>
          <div className="stat-content">
            <h3>Sessions</h3>
            <div className="stat-number">{stats?.sessions?.total || 0}</div>
            <div className="stat-details">
              <span className="stat-detail active">
                <i className="fas fa-circle"></i>
                {stats?.sessions?.active || 0} Active
              </span>
              <span className="stat-detail upcoming">
                <i className="fas fa-clock"></i>
                {stats?.sessions?.upcoming || 0} Upcoming
              </span>
            </div>
          </div>
          <button 
            onClick={() => navigate('/admin/sessions')}
            className="card-action"
          >
            Manage <i className="fas fa-arrow-right"></i>
          </button>
        </div>

        {/* Students Stats */}
        <div className="stat-card students-card">
          <div className="stat-icon">
            <i className="fas fa-users"></i>
          </div>
          <div className="stat-content">
            <h3>Students</h3>
            <div className="stat-number">{stats?.attendees?.total || 0}</div>
            <div className="stat-details">
              <span className="stat-detail">
                <i className="fas fa-user-graduate"></i>
                Total Registered
              </span>
            </div>
          </div>
          <button 
            onClick={() => navigate('/admin/students')}
            className="card-action"
          >
            View All <i className="fas fa-arrow-right"></i>
          </button>
        </div>

        {/* Questions Stats */}
        <div className="stat-card questions-card">
          <div className="stat-icon">
            <i className="fas fa-question-circle"></i>
          </div>
          <div className="stat-content">
            <h3>Questions</h3>
            <div className="stat-number">{stats?.content?.questions || 0}</div>
            <div className="stat-details">
              <span className="stat-detail">
                <i className="fas fa-check-circle"></i>
                {stats?.content?.responses || 0} Responses
              </span>
            </div>
          </div>
          <button 
            onClick={() => navigate('/admin/questions')}
            className="card-action"
          >
            Manage <i className="fas fa-arrow-right"></i>
          </button>
        </div>

        {/* Feedback Stats */}
        <div className="stat-card feedback-card">
          <div className="stat-icon">
            <i className="fas fa-comment-dots"></i>
          </div>
          <div className="stat-content">
            <h3>Feedback</h3>
            <div className="stat-number">{stats?.content?.reviews || 0}</div>
            <div className="stat-details">
              <span className="stat-detail">
                <i className="fas fa-star"></i>
                Student Reviews
              </span>
            </div>
          </div>
          <button 
            onClick={() => navigate('/admin/feedback')}
            className="card-action"
          >
            View All <i className="fas fa-arrow-right"></i>
          </button>
        </div>
      </div>

      {/* Recent Activity Section */}
      <div className="activity-section">
        <div className="activity-column">
          <div className="activity-card">
            <div className="activity-header">
              <h2>
                <i className="fas fa-user-plus"></i>
                Recent Students
              </h2>
              <button 
                onClick={() => navigate('/admin/students')}
                className="view-all-link"
              >
                View All <i className="fas fa-arrow-right"></i>
              </button>
            </div>
            <div className="activity-list">
              {stats?.recent_activity?.attendees?.length > 0 ? (
                stats.recent_activity.attendees.map((student) => (
                  <div key={student.id} className="activity-item">
                    <div className="activity-icon student-icon">
                      <i className="fas fa-user"></i>
                    </div>
                    <div className="activity-info">
                      <h4>{student.name}</h4>
                      <p>{student.email}</p>
                      <span className="activity-time">
                        <i className="fas fa-calendar"></i>
                        {student.session_title || 'No session'}
                      </span>
                    </div>
                    <div className="activity-status">
                      {student.has_submitted ? (
                        <span className="badge badge-success">
                          <i className="fas fa-check"></i>
                          Completed
                        </span>
                      ) : (
                        <span className="badge badge-pending">
                          <i className="fas fa-clock"></i>
                          In Progress
                        </span>
                      )}
                    </div>
                  </div>
                ))
              ) : (
                <div className="empty-state">
                  <i className="fas fa-inbox"></i>
                  <p>No recent students</p>
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="activity-column">
          <div className="activity-card">
            <div className="activity-header">
              <h2>
                <i className="fas fa-comments"></i>
                Recent Feedback
              </h2>
              <button 
                onClick={() => navigate('/admin/feedback')}
                className="view-all-link"
              >
                View All <i className="fas fa-arrow-right"></i>
              </button>
            </div>
            <div className="activity-list">
              {stats?.recent_activity?.reviews?.length > 0 ? (
                stats.recent_activity.reviews.map((review) => (
                  <div key={review.id} className="activity-item">
                    <div className="activity-icon feedback-icon">
                      <i className="fas fa-comment"></i>
                    </div>
                    <div className="activity-info">
                      <h4>Student Feedback</h4>
                      <p className="feedback-content">
                        {review.content?.substring(0, 100)}
                        {review.content?.length > 100 ? '...' : ''}
                      </p>
                      <span className="activity-time">
                        <i className="fas fa-clock"></i>
                        {new Date(review.submitted_at).toLocaleDateString()}
                      </span>
                    </div>
                  </div>
                ))
              ) : (
                <div className="empty-state">
                  <i className="fas fa-inbox"></i>
                  <p>No recent feedback</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="quick-actions">
        <h2>
          <i className="fas fa-bolt"></i>
          Quick Actions
        </h2>
        <div className="actions-grid">
          <button 
            onClick={() => navigate('/admin/sessions')}
            className="action-button action-primary"
          >
            <i className="fas fa-plus-circle"></i>
            <span>Manage Sessions</span>
          </button>
          <button 
            onClick={() => navigate('/admin/questions')}
            className="action-button action-secondary"
          >
            <i className="fas fa-edit"></i>
            <span>Add Questions</span>
          </button>
          <button 
            onClick={() => navigate('/admin/students')}
            className="action-button action-tertiary"
          >
            <i className="fas fa-users"></i>
            <span>View All Students</span>
          </button>
          <button 
            onClick={() => navigate('/admin/feedback')}
            className="action-button action-info"
          >
            <i className="fas fa-star"></i>
            <span>View Feedback</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;
