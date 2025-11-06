/**
 * FEEDBACK COMPONENT
 * 
 * BEGINNER EXPLANATION:
 * Simple form to collect feedback after quiz completion.
 * No authentication required for submitting feedback.
 */

import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../../services/api';
import '../../styles/Feedback.css';

function Feedback() {
  const { sessionId } = useParams();
  const navigate = useNavigate();

  const [content, setContent] = useState('');
  const [feedbackType, setFeedbackType] = useState('review');
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const attendeeId = localStorage.getItem('attendee_id');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSubmitting(true);

    if (!attendeeId) {
      setError('Attendee information not found. Please register first.');
      setSubmitting(false);
      return;
    }

    try {
      await api.submitFeedback({
        attendee: parseInt(attendeeId),
        content: content,
        feedback_type: feedbackType,
      });

      setSuccess(true);
      
      // Redirect after 2 seconds
      setTimeout(() => {
        navigate('/student/dashboard');
      }, 2000);

    } catch (err) {
      setError('Failed to submit feedback. Please try again.');
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  if (success) {
    return (
      <div className="container">
        <div className="feedback-card">
          <div className="alert alert-success">
            <h2>✓ Thank You for Your Feedback!</h2>
            <p>Your feedback has been submitted successfully.</p>
            <p>Redirecting...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      <div className="feedback-card">
        <h2>Share Your Feedback</h2>
        <p className="subtitle">
          Help us improve by sharing your thoughts about the workshop
        </p>

        {error && <div className="alert alert-error">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="feedbackType">Feedback Type</label>
            <select
              id="feedbackType"
              value={feedbackType}
              onChange={(e) => setFeedbackType(e.target.value)}
              disabled={submitting}
            >
              <option value="review">General Review</option>
              <option value="quiz">Quiz Feedback</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="content">Your Feedback *</label>
            <textarea
              id="content"
              value={content}
              onChange={(e) => setContent(e.target.value)}
              placeholder="Share your thoughts about the workshop, quiz questions, or any suggestions for improvement..."
              rows="8"
              required
              disabled={submitting}
            />
          </div>

          <div className="form-actions">
            <button 
              type="submit" 
              className="btn btn-primary"
              disabled={!content || submitting}
            >
              {submitting ? 'Submitting...' : 'Submit Feedback'}
            </button>
            <button 
              type="button"
              onClick={() => navigate('/student/dashboard')}
              className="btn btn-outline"
              disabled={submitting}
            >
              Skip for Now
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default Feedback;
