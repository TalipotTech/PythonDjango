/**
 * QUIZ COMPONENT
 * 
 * BEGINNER EXPLANATION:
 * This component shows all quiz questions on one scrollable page with a timer.
 * It tracks progress and submits answers to the Django backend.
 * 
 * Flow:
 * 1. Load questions for the session
 * 2. Show all questions with scrolling
 * 3. Timer counts down from 5 minutes
 * 4. Auto-submit when timer ends
 * 5. Show completion message when done
 */

import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../../services/api';
import '../../styles/Quiz.css';

function Quiz() {
  const { sessionId } = useParams(); // Get session ID from URL
  const navigate = useNavigate();

  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState({});  // Store answers: {questionId: answer}
  const [feedback, setFeedback] = useState('');  // Store feedback/question
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [timeRemaining, setTimeRemaining] = useState(300); // 5 minutes in seconds
  const timerRef = useRef(null);

  // Get attendee info from localStorage
  const attendeeId = localStorage.getItem('attendee_id');
  const attendeeEmail = localStorage.getItem('attendee_email');

  useEffect(() => {
    if (!attendeeId) {
      navigate(`/register/${sessionId}`);
      return;
    }
    fetchQuestions();
  }, [sessionId]);

  // Timer countdown
  useEffect(() => {
    if (loading || submitting) return;

    timerRef.current = setInterval(() => {
      setTimeRemaining((prev) => {
        if (prev <= 1) {
          clearInterval(timerRef.current);
          handleSubmitQuiz(true); // Auto-submit when time runs out
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    };
  }, [loading, submitting]);

  /**
   * Fetch questions for this session
   */
  const fetchQuestions = async () => {
    try {
      const data = await api.getQuestions(sessionId);
      setQuestions(data.results || data);
      
      if ((data.results || data).length === 0) {
        setError('No questions available for this session yet');
      }
    } catch (err) {
      setError('Failed to load questions. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Handle answer selection/input
   */
  const handleAnswerChange = (questionId, answer) => {
    setAnswers({
      ...answers,
      [questionId]: answer
    });
  };

  /**
   * Format time remaining as MM:SS
   */
  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  /**
   * Submit all answers
   */
  const handleSubmitQuiz = async (autoSubmit = false) => {
    if (submitting) return;

    // Clear timer
    if (timerRef.current) {
      clearInterval(timerRef.current);
    }

    setError('');
    setSubmitting(true);

    try {
      // Submit all answers
      for (const question of questions) {
        const answer = answers[question.id];
        
        // Skip unanswered questions
        if (!answer) continue;

        // Prepare response data
        const responseData = {
          attendee: parseInt(attendeeId),
          question: question.id,
        };

        // Add answer based on question type
        if (question.question_type === 'multiple_choice') {
          responseData.selected_option = parseInt(answer);
        } else {
          responseData.text_response = answer;
        }

        // Submit answer to Django
        await api.submitResponse(responseData);
      }

      // Submit feedback if provided
      if (feedback.trim()) {
        try {
          await api.submitFeedback({
            attendee: parseInt(attendeeId),
            content: feedback,
            feedback_type: 'quiz'
          });
        } catch (feedbackErr) {
          console.error('Failed to submit feedback:', feedbackErr);
        }
      }
      
      await api.submitQuiz(attendeeId); // Mark as submitted
      
      const answeredCount = Object.keys(answers).length;
      
      // Redirect to Thank You page
      navigate('/thank-you', {
        state: {
          attendeeName: localStorage.getItem('attendee_name'),
          sessionTitle: questions[0]?.session_title || 'Quiz Session',
          answeredCount: answeredCount,
          totalQuestions: questions.length,
          autoSubmitted: autoSubmit
        }
      });

    } catch (err) {
      console.error('Submit error:', err);
      const errorMessage = err.response?.data?.detail 
        || err.response?.data?.message
        || err.response?.data?.error
        || err.message
        || 'Failed to submit quiz. Please try again.';
      
      setError(errorMessage);
      setSubmitting(false);
    }
  };

  // Loading state
  if (loading) {
    return (
      <div className="container">
        <div className="loading">
          <div className="spinner"></div>
          <p>Loading quiz...</p>
        </div>
      </div>
    );
  }

  // Error state
  if (error && questions.length === 0) {
    return (
      <div className="container">
        <div className="alert alert-error">{error}</div>
        <button onClick={() => navigate('/sessions')} className="btn btn-outline">
          ← Back to Sessions
        </button>
      </div>
    );
  }

  const answeredCount = Object.keys(answers).length;
  const progress = (answeredCount / questions.length) * 100;
  const isTimeLow = timeRemaining <= 60; // Last minute warning

  return (
    <div style={{ 
      backgroundColor: '#f5f7fa',
      minHeight: '100vh',
      paddingBottom: '140px' // Space for fixed footer
    }}>
      {/* Timer and Progress Header - Sticky */}
      <div style={{
        position: 'sticky',
        top: 0,
        backgroundColor: 'white',
        zIndex: 100,
        padding: '1.5rem 0',
        boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
        borderBottom: '2px solid #e5e7eb',
        marginBottom: '2rem'
      }}>
        <div style={{ maxWidth: '900px', margin: '0 auto', padding: '0 2rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
            <div>
              <h1 style={{ margin: 0, fontSize: '1.75rem', fontWeight: '600', color: '#1a202c' }}>
                📝 Quiz Assessment
              </h1>
              <p style={{ margin: '0.5rem 0 0 0', color: '#718096', fontSize: '0.95rem' }}>
                {answeredCount} of {questions.length} questions completed
              </p>
            </div>
          <div style={{ textAlign: 'right' }}>
            <div style={{
              fontSize: '2rem',
              fontWeight: 'bold',
              fontFamily: 'monospace',
              color: isTimeLow ? '#dc2626' : '#667eea',
              animation: isTimeLow ? 'pulse 1s infinite' : 'none'
            }}>
              ⏱️ {formatTime(timeRemaining)}
            </div>
            <p style={{ margin: '0.25rem 0 0 0', fontSize: '0.85rem', color: isTimeLow ? '#dc2626' : '#666' }}>
              {isTimeLow ? 'Hurry up!' : 'Time remaining'}
            </p>
          </div>
        </div>
        
        {/* Progress Bar */}
        <div className="quiz-progress">
          <div className="progress-bar" style={{ height: '8px', borderRadius: '4px' }}>
            <div 
              className="progress-fill" 
              style={{ 
                width: `${progress}%`,
                transition: 'width 0.3s ease',
                height: '100%',
                borderRadius: '4px'
              }}
            ></div>
          </div>
        </div>

        {error && <div className="alert alert-error" style={{ marginTop: '1rem' }}>{error}</div>}
      </div>

      {/* All Questions - Scrollable */}
      <div className="questions-container">
        {questions.map((question, index) => {
          const currentAnswer = answers[question.id];
          const isAnswered = currentAnswer !== undefined && currentAnswer !== '';

          return (
            <div 
              key={question.id} 
              className="question-card-large"
              style={{
                marginBottom: '2rem',
                border: isAnswered ? '2px solid #10b981' : '2px solid #e5e7eb',
                position: 'relative'
              }}
            >
              {isAnswered && (
                <div style={{
                  position: 'absolute',
                  top: '1rem',
                  right: '1rem',
                  background: '#10b981',
                  color: 'white',
                  padding: '0.5rem 1rem',
                  borderRadius: '20px',
                  fontSize: '0.85rem',
                  fontWeight: 'bold'
                }}>
                  ✓ Answered
                </div>
              )}

              <div className="question-header">
                <span className="question-number">Q{index + 1}</span>
                <span className="question-type-badge">
                  {question.question_type === 'multiple_choice' ? 
                    'Multiple Choice' : 'Text Response'}
                </span>
              </div>

              <h3 className="question-text" style={{ fontSize: '1.2rem', marginBottom: '1.5rem' }}>
                {question.text}
              </h3>

              {/* Multiple Choice Options */}
              {question.question_type === 'multiple_choice' ? (
                <div className="quiz-options">
                  {[1, 2, 3, 4].map((optionNum) => {
                    const optionText = question[`option${optionNum}`];
                    if (!optionText) return null;

                    return (
                      <label 
                        key={optionNum} 
                        className={`quiz-option ${currentAnswer === optionNum ? 'selected' : ''}`}
                      >
                        <input
                          type="radio"
                          name={`question-${question.id}`}
                          value={optionNum}
                          checked={currentAnswer === optionNum}
                          onChange={() => handleAnswerChange(question.id, optionNum)}
                          disabled={submitting}
                        />
                        <span className="option-letter">
                          {String.fromCharCode(64 + optionNum)}
                        </span>
                        <span className="option-text">{optionText}</span>
                      </label>
                    );
                  })}
                </div>
              ) : (
                /* Text Response Input */
                <div className="text-response-group">
                  <textarea
                    value={currentAnswer || ''}
                    onChange={(e) => handleAnswerChange(question.id, e.target.value)}
                    placeholder="Type your answer here..."
                    rows="6"
                    disabled={submitting}
                  />
                </div>
              )}
            </div>
          );
        })}

        {/* Feedback Section */}
        <div className="feedback-card" style={{ marginTop: '2rem', marginBottom: '2rem' }}>
          <h3 style={{ fontSize: '1.1rem', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span>💬</span> Feedback / Question (Optional)
          </h3>
          <p style={{ fontSize: '0.9rem', color: '#666', marginBottom: '1rem' }}>
            Submit a question or feedback about the quiz.
          </p>
          <div className="text-response-group">
            <textarea
              value={feedback}
              onChange={(e) => setFeedback(e.target.value)}
              placeholder="Ask the instructor or provide feedback..."
              rows="4"
              disabled={submitting}
              style={{ minHeight: '100px' }}
            />
          </div>
        </div>
      </div>

      {/* Submit Button - Fixed at Bottom */}
      <div style={{ 
        position: 'fixed',
        bottom: 0,
        left: 0,
        right: 0,
        backgroundColor: 'white',
        borderTop: '2px solid #e5e7eb',
        padding: '1.5rem',
        boxShadow: '0 -4px 20px rgba(0,0,0,0.1)',
        zIndex: 99,
        textAlign: 'center'
      }}>
        {answeredCount < questions.length && (
          <p style={{ margin: '0 0 1rem 0', color: '#f59e0b', fontSize: '0.95rem', fontWeight: '500' }}>
            ⚠️ You have {questions.length - answeredCount} unanswered question(s)
          </p>
        )}
        <button 
          onClick={() => handleSubmitQuiz(false)}
          className="btn btn-primary"
          disabled={submitting || answeredCount === 0}
          style={{
            fontSize: '1.2rem',
            padding: '1rem 3rem',
            boxShadow: '0 4px 20px rgba(102, 126, 234, 0.4)',
            minWidth: '300px'
          }}
        >
          {submitting ? '⏳ Submitting...' : `🎯 Submit Quiz (${answeredCount}/${questions.length})`}
        </button>
      </div>

      {/* Add padding at bottom to prevent content being hidden by fixed footer */}
      <div style={{ height: '120px' }}></div>

      {/* Timer CSS */}
      <style jsx>{`
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.5; }
        }
      `}</style>
    </div>
  );
}

export default Quiz;
