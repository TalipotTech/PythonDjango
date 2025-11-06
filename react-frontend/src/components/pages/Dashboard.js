/**
 * DASHBOARD COMPONENT
 * 
 * BEGINNER EXPLANATION:
 * User dashboard showing their registered sessions and progress.
 * Requires authentication to access.
 */

import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../../services/api';
import '../../styles/Dashboard.css';

function Dashboard() {
  const [user, setUser] = useState(null);
  const [registrations, setRegistrations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchUserData();
  }, []);

  const fetchUserData = async () => {
    try {
      const userData = await api.getProfile();
      setUser(userData);

      // Fetch user's registrations
      const regs = await api.getMyRegistrations(userData.email);
      setRegistrations(regs);
    } catch (err) {
      console.error('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="container">
        <div className="loading">
          <div className="spinner"></div>
          <p>Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      <div className="dashboard">
        <div className="dashboard-header">
          <div>
            <h1>Welcome back, {user?.first_name || user?.username}!</h1>
            <p className="text-muted">{user?.email}</p>
          </div>
          <Link to="/sessions" className="btn btn-primary">
            Browse More Sessions
          </Link>
        </div>

        <div className="dashboard-stats">
          <div className="stat-card">
            <h3>{registrations.length}</h3>
            <p>Registered Sessions</p>
          </div>
          <div className="stat-card">
            <h3>{registrations.filter(r => r.has_submitted).length}</h3>
            <p>Completed Quizzes</p>
          </div>
          <div className="stat-card">
            <h3>{registrations.filter(r => !r.has_submitted).length}</h3>
            <p>Pending Quizzes</p>
          </div>
        </div>

        <div className="dashboard-sessions">
          <h2>My Sessions</h2>
          
          {registrations.length === 0 ? (
            <div className="empty-state">
              <p>You haven't registered for any sessions yet.</p>
              <Link to="/sessions" className="btn btn-primary">
                Browse Sessions
              </Link>
            </div>
          ) : (
            <div className="sessions-list">
              {registrations.map((reg) => (
                <div key={reg.id} className="registration-card">
                  <div className="registration-info">
                    <h3>{reg.session_title}</h3>
                    <p>Session Code: <code>{reg.session_code}</code></p>
                    <p>Registered on: {new Date(reg.created_at).toLocaleDateString()}</p>
                  </div>
                  <div className="registration-status">
                    {reg.has_submitted ? (
                      <span className="badge badge-success">✓ Completed</span>
                    ) : (
                      <>
                        <span className="badge badge-warning">Pending</span>
                        <Link 
                          to={`/quiz/${reg.class_session}`}
                          className="btn btn-primary btn-sm"
                        >
                          Continue Quiz
                        </Link>
                      </>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
