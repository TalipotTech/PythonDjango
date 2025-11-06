import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';
import '../../styles/StudentManagement.css';

const StudentManagement = () => {
  const navigate = useNavigate();
  const [students, setStudents] = useState([]);
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedSession, setSelectedSession] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [showDetailsModal, setShowDetailsModal] = useState(false);
  const [selectedStudent, setSelectedStudent] = useState(null);

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
      const [studentsData, sessionsData] = await Promise.all([
        api.getAllStudents(),
        api.getSessions()
      ]);
      
      setStudents(Array.isArray(studentsData) ? studentsData : (studentsData.results || []));
      setSessions(Array.isArray(sessionsData) ? sessionsData : (sessionsData.results || []));
      setError('');
    } catch (err) {
      setError('Failed to load data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id, name) => {
    if (window.confirm(`Are you sure you want to delete ${name}? This action cannot be undone.`)) {
      try {
        await api.deleteStudent(id);
        fetchData();
      } catch (err) {
        setError('Failed to delete student');
        console.error(err);
      }
    }
  };

  const handleViewDetails = (student) => {
    setSelectedStudent(student);
    setShowDetailsModal(true);
  };

  const handleLogout = () => {
    api.adminLogout();
    navigate('/admin/login');
  };

  const getSessionName = (sessionId) => {
    const session = sessions.find(s => s.id === sessionId);
    return session ? session.title : 'Unknown Session';
  };

  const filteredStudents = students.filter(student => {
    const matchesSession = selectedSession === 'all' || student.class_session === parseInt(selectedSession);
    const matchesSearch = student.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         student.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         student.phone.includes(searchTerm);
    return matchesSession && matchesSearch;
  });

  if (loading) {
    return (
      <div className="student-management">
        <div className="loading">Loading students...</div>
      </div>
    );
  }

  return (
    <div className="student-management">
      <div className="student-header">
        <div className="header-left">
          <h1>Student Management</h1>
          <button className="btn-back" onClick={() => navigate('/admin/dashboard')}>
            ← Back to Dashboard
          </button>
        </div>
        <div className="header-right">
          <button className="btn-logout" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </div>

      {error && <div className="error-message">{error}</div>}

      {/* Filters */}
      <div className="filters-section">
        <div className="filter-group">
          <label htmlFor="sessionFilter">Filter by Session:</label>
          <select
            id="sessionFilter"
            value={selectedSession}
            onChange={(e) => setSelectedSession(e.target.value)}
            className="filter-select"
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
          <label htmlFor="searchInput">Search:</label>
          <input
            id="searchInput"
            type="text"
            placeholder="Search by name, email, or phone..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
        </div>

        <div className="filter-stats">
          <span className="stat-badge">
            Total: {filteredStudents.length} student{filteredStudents.length !== 1 ? 's' : ''}
          </span>
        </div>
      </div>

      {/* Students Table */}
      {filteredStudents.length === 0 ? (
        <div className="no-data">
          <i className="fas fa-users"></i>
          <p>No students found matching your criteria.</p>
        </div>
      ) : (
        <div className="table-container">
          <table className="students-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Phone</th>
                <th>Session</th>
                <th>Status</th>
                <th>Registered</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredStudents.map(student => (
                <tr key={student.id}>
                  <td className="student-name">
                    <i className="fas fa-user-circle"></i>
                    {student.name}
                  </td>
                  <td>{student.email}</td>
                  <td>{student.phone}</td>
                  <td>
                    {student.attended_sessions && student.attended_sessions.length > 0 ? (
                      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.25rem' }}>
                        {student.attended_sessions.map((session, idx) => (
                          <span 
                            key={session.id}
                            style={{
                              padding: '0.25rem 0.5rem',
                              backgroundColor: '#e0e7ff',
                              borderRadius: '4px',
                              fontSize: '0.875rem',
                              color: '#4338ca'
                            }}
                          >
                            {session.title}
                          </span>
                        ))}
                      </div>
                    ) : (
                      <span style={{ color: '#9ca3af' }}>No sessions attended</span>
                    )}
                  </td>
                  <td>
                    {student.has_submitted ? (
                      <span className="badge badge-success">
                        <i className="fas fa-check-circle"></i> Completed
                      </span>
                    ) : student.quiz_started_at ? (
                      <span className="badge badge-warning">
                        <i className="fas fa-clock"></i> In Progress
                      </span>
                    ) : (
                      <span className="badge badge-info">
                        <i className="fas fa-user-plus"></i> Registered
                      </span>
                    )}
                  </td>
                  <td>{student.created_at ? new Date(student.created_at).toLocaleDateString() : 'N/A'}</td>
                  <td className="actions-cell">
                    <button 
                      className="btn-view"
                      onClick={() => handleViewDetails(student)}
                      title="View Details"
                    >
                      <i className="fas fa-eye"></i>
                    </button>
                    <button 
                      className="btn-delete-small"
                      onClick={() => handleDelete(student.id, student.name)}
                      title="Delete Student"
                    >
                      <i className="fas fa-trash"></i>
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Student Details Modal */}
      {showDetailsModal && selectedStudent && (
        <div className="modal-overlay" onClick={() => setShowDetailsModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Student Details</h2>
              <button className="modal-close" onClick={() => setShowDetailsModal(false)}>×</button>
            </div>
            <div className="student-details">
              <div className="detail-section">
                <h3>Personal Information</h3>
                <div className="detail-row">
                  <span className="detail-label">Name:</span>
                  <span className="detail-value">{selectedStudent.name}</span>
                </div>
                <div className="detail-row">
                  <span className="detail-label">Email:</span>
                  <span className="detail-value">{selectedStudent.email}</span>
                </div>
                <div className="detail-row">
                  <span className="detail-label">Phone:</span>
                  <span className="detail-value">{selectedStudent.phone}</span>
                </div>
                {selectedStudent.age && (
                  <div className="detail-row">
                    <span className="detail-label">Age:</span>
                    <span className="detail-value">{selectedStudent.age}</span>
                  </div>
                )}
                {selectedStudent.place && (
                  <div className="detail-row">
                    <span className="detail-label">Place:</span>
                    <span className="detail-value">{selectedStudent.place}</span>
                  </div>
                )}
              </div>

              <div className="detail-section">
                <h3>Session Information</h3>
                <div className="detail-row">
                  <span className="detail-label">Session:</span>
                  <span className="detail-value">{getSessionName(selectedStudent.class_session)}</span>
                </div>
                <div className="detail-row">
                  <span className="detail-label">Password:</span>
                  <span className="detail-value">{selectedStudent.plain_password || 'N/A'}</span>
                </div>
              </div>

              <div className="detail-section">
                <h3>Progress</h3>
                <div className="detail-row">
                  <span className="detail-label">Status:</span>
                  <span className="detail-value">
                    {selectedStudent.has_submitted ? (
                      <span className="badge badge-success">Completed Quiz</span>
                    ) : selectedStudent.quiz_started_at ? (
                      <span className="badge badge-warning">Quiz In Progress</span>
                    ) : (
                      <span className="badge badge-info">Not Started</span>
                    )}
                  </span>
                </div>
                <div className="detail-row">
                  <span className="detail-label">Registered:</span>
                  <span className="detail-value">
                    {selectedStudent.created_at ? new Date(selectedStudent.created_at).toLocaleString() : 'N/A'}
                  </span>
                </div>
                {selectedStudent.quiz_started_at && (
                  <div className="detail-row">
                    <span className="detail-label">Quiz Started:</span>
                    <span className="detail-value">
                      {new Date(selectedStudent.quiz_started_at).toLocaleString()}
                    </span>
                  </div>
                )}
              </div>
            </div>
            <div className="modal-actions">
              <button className="btn-close" onClick={() => setShowDetailsModal(false)}>
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default StudentManagement;
