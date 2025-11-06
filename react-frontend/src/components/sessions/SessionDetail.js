/**
 * SESSION DETAIL COMPONENT
 * 
 * BEGINNER EXPLANATION:
 * Shows detailed information about a single session.
 * Displays all questions and attendees for that session.
 * 
 * Uses useParams to get the session ID from the URL
 */

import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import api from '../../services/api';
import '../../styles/Sessions.css';

function SessionDetail() {
  const { id } = useParams(); // Get session ID from URL (/sessions/:id)
  const navigate = useNavigate();
  
  const [session, setSession] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchSessionDetail();
  }, [id]); // Re-fetch if ID changes

  /**
   * Fetch session details and questions
   */
  const fetchSessionDetail = async () => {
    try {
      // Fetch session info
      const sessionData = await api.getSessionById(id);
      setSession(sessionData);

      // Fetch questions for this session
      try {
        const questionsData = await api.getQuestions(id);
        setQuestions(questionsData.results || questionsData);
      } catch (qErr) {
        // Questions might require authentication, that's okay
        console.log('Could not load questions');
      }

    } catch (err) {
      setError('Failed to load session details');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Format date for display
   */
  const formatDateTime = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
      month: 'long',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
      <div className="container">
        <div className="loading">
          <div className="spinner"></div>
          <p>Loading session...</p>
        </div>
      </div>
    );
  }

  if (error || !session) {
    return (
      <div className="container">
        <div className="alert alert-error">{error || 'Session not found'}</div>
        <button onClick={() => navigate('/sessions')} className="btn btn-outline">
          ← Back to Sessions
        </button>
      </div>
    );
  }

  return (
    <div className="container">
      {/* Back Button */}
      <button onClick={() => navigate('/sessions')} className="btn btn-outline btn-sm mb-3">
        ← Back to Sessions
      </button>

      {/* Session Card */}
      <div className="session-detail-card">
        <div className="session-detail-header">
          <div>
            <h1>{session.title}</h1>
            <p className="session-teacher">by {session.teacher}</p>
          </div>
          {session.is_active ? (
            <span className="badge badge-success badge-lg">● Active Now</span>
          ) : (
            <span className="badge badge-secondary badge-lg">Upcoming</span>
          )}
        </div>

        <div className="session-detail-info">
          <div className="info-item">
            <strong>Session Code:</strong>
            <code className="session-code-large">{session.session_code}</code>
          </div>

          <div className="info-item">
            <strong>Start Time:</strong>
            <p>{formatDateTime(session.start_time)}</p>
          </div>

          <div className="info-item">
            <strong>End Time:</strong>
            <p>{formatDateTime(session.end_time)}</p>
          </div>

          <div className="info-item">
            <strong>Attendees:</strong>
            <p>👥 {session.attendee_count} registered</p>
          </div>
        </div>

        {/* Join Button */}
        <div className="session-actions-center">
          <Link 
            to={`/register/${session.session_code}`}
            className="btn btn-primary btn-lg"
          >
            Join This Session
          </Link>
        </div>
      </div>

      {/* Questions Section */}
      {questions.length > 0 && (
        <div className="questions-section">
          <h2>Quiz Questions ({questions.length})</h2>
          <div className="questions-list">
            {questions.map((question, index) => (
              <div key={question.id} className="question-card">
                <div className="question-header">
                  <span className="question-number">Q{index + 1}</span>
                  <span className="question-type-badge">
                    {question.question_type === 'multiple_choice' ? 'Multiple Choice' : 'Text Response'}
                  </span>
                </div>
                <p className="question-text">{question.text}</p>

                {/* Show options for multiple choice */}
                {question.question_type === 'multiple_choice' && (
                  <div className="question-options">
                    {[1, 2, 3, 4].map(num => {
                      const optionText = question[`option${num}`];
                      if (!optionText) return null;
                      return (
                        <div key={num} className="option-preview">
                          <span className="option-label">{String.fromCharCode(64 + num)}.</span>
                          <span>{optionText}</span>
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default SessionDetail;
