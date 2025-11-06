/**
 * QUIZ COMPONENT - CLEAN & PROFESSIONAL DESIGN
 * 
 * Features:
 * - 5-minute countdown timer
 * - All questions on one scrollable page
 * - Clean, spacious layout
 * - Professional styling
 */

import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../../services/api';
import '../../styles/Quiz.css';

function Quiz() {
  const { sessionId } = useParams();
  const navigate = useNavigate();

  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState({});
  const [feedback, setFeedback] = useState('');
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [timeRemaining, setTimeRemaining] = useState(300); // 5 minutes
  const timerRef = useRef(null);

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
          handleSubmitQuiz(true);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [loading, submitting]);

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

  const handleAnswerChange = (questionId, answer) => {
    setAnswers({
      ...answers,
      [questionId]: answer
    });
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const handleSubmitQuiz = async (autoSubmit = false) => {
    if (submitting) return;
    if (timerRef.current) clearInterval(timerRef.current);

    setError('');
    setSubmitting(true);

    try {
      for (const question of questions) {
        const answer = answers[question.id];
        if (!answer) continue;

        const responseData = {
          attendee: parseInt(attendeeId),
          question: question.id,
        };

        if (question.question_type === 'multiple_choice') {
          responseData.selected_option = parseInt(answer);
        } else {
          responseData.text_response = answer;
        }

        await api.submitResponse(responseData);
      }

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
      
      await api.submitQuiz(attendeeId);
      
      const answeredCount = Object.keys(answers).length;
      
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

  if (loading) {
    return (
      <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <div style={{ textAlign: 'center' }}>
          <div className="spinner"></div>
          <p style={{ marginTop: '1rem', color: '#718096' }}>Loading quiz...</p>
        </div>
      </div>
    );
  }

  if (error && questions.length === 0) {
    return (
      <div style={{ maxWidth: '600px', margin: '4rem auto', padding: '0 2rem' }}>
        <div style={{ padding: '1.5rem', backgroundColor: '#fee2e2', borderRadius: '8px', border: '1px solid #fecaca', color: '#991b1b' }}>
          {error}
        </div>
        <button onClick={() => navigate('/sessions')} style={{ marginTop: '1rem' }} className="btn btn-outline">
          ← Back to Sessions
        </button>
      </div>
    );
  }

  const answeredCount = Object.keys(answers).length;
  const progress = (answeredCount / questions.length) * 100;
  const isTimeLow = timeRemaining <= 60;

  return (
    <div style={{ backgroundColor: '#f8fafc', minHeight: '100vh', paddingBottom: '140px' }}>
      {/* Header - Sticky */}
      <div style={{
        position: 'sticky',
        top: 0,
        backgroundColor: 'white',
        zIndex: 100,
        padding: '1.5rem 0',
        boxShadow: '0 1px 3px rgba(0,0,0,0.08)',
        borderBottom: '1px solid #e2e8f0',
        marginBottom: '2.5rem'
      }}>
        <div style={{ maxWidth: '1000px', margin: '0 auto', padding: '0 2rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '2rem', marginBottom: '1.25rem' }}>
            <div style={{ flex: 1 }}>
              <h1 style={{ margin: 0, fontSize: '1.75rem', fontWeight: '600', color: '#1e293b', letterSpacing: '-0.025em' }}>
                📝 Quiz Assessment
              </h1>
              <p style={{ margin: '0.5rem 0 0 0', color: '#64748b', fontSize: '0.95rem' }}>
                Answer all questions to the best of your ability
              </p>
            </div>
            <div style={{ textAlign: 'right', minWidth: '150px' }}>
              <div style={{
                fontSize: '2.25rem',
                fontWeight: '700',
                fontFamily: 'ui-monospace, monospace',
                color: isTimeLow ? '#dc2626' : '#4f46e5',
                lineHeight: 1,
                animation: isTimeLow ? 'pulse 1s infinite' : 'none'
              }}>
                ⏱️ {formatTime(timeRemaining)}
              </div>
              <p style={{ margin: '0.5rem 0 0 0', fontSize: '0.8125rem', color: isTimeLow ? '#dc2626' : '#64748b', fontWeight: '500', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                {isTimeLow ? 'Hurry!' : 'Remaining'}
              </p>
            </div>
          </div>
          
          {/* Progress */}
          <div style={{ marginBottom: '0.75rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
              <span style={{ fontSize: '0.875rem', color: '#64748b', fontWeight: '500' }}>
                Progress: {answeredCount}/{questions.length}
              </span>
              <span style={{ fontSize: '0.875rem', color: '#4f46e5', fontWeight: '600' }}>
                {Math.round(progress)}%
              </span>
            </div>
            <div style={{ width: '100%', height: '8px', backgroundColor: '#e2e8f0', borderRadius: '4px', overflow: 'hidden' }}>
              <div style={{ 
                width: `${progress}%`,
                height: '100%',
                backgroundColor: '#4f46e5',
                transition: 'width 0.3s ease',
                borderRadius: '4px'
              }}></div>
            </div>
          </div>

          {error && (
            <div style={{ 
              marginTop: '1rem',
              padding: '0.875rem 1rem',
              backgroundColor: '#fee2e2',
              border: '1px solid #fecaca',
              borderRadius: '6px',
              color: '#991b1b',
              fontSize: '0.875rem',
              fontWeight: '500'
            }}>
              {error}
            </div>
          )}
        </div>
      </div>

      {/* Questions */}
      <div style={{ maxWidth: '1000px', margin: '0 auto', padding: '0 2rem' }}>
        {questions.map((question, index) => {
          const currentAnswer = answers[question.id];
          const isAnswered = currentAnswer !== undefined && currentAnswer !== '';

          return (
            <div 
              key={question.id} 
              style={{
                marginBottom: '2rem',
                padding: '2rem',
                backgroundColor: 'white',
                borderRadius: '12px',
                border: isAnswered ? '2px solid #10b981' : '2px solid #e2e8f0',
                boxShadow: '0 1px 3px rgba(0,0,0,0.05)',
                position: 'relative',
                transition: 'all 0.2s ease'
              }}
            >
              {isAnswered && (
                <div style={{
                  position: 'absolute',
                  top: '1.5rem',
                  right: '1.5rem',
                  backgroundColor: '#10b981',
                  color: 'white',
                  padding: '0.375rem 0.875rem',
                  borderRadius: '9999px',
                  fontSize: '0.8125rem',
                  fontWeight: '600',
                  letterSpacing: '0.025em'
                }}>
                  ✓ Answered
                </div>
              )}

              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1.25rem' }}>
                <span style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  width: '2.5rem',
                  height: '2.5rem',
                  backgroundColor: '#eef2ff',
                  color: '#4f46e5',
                  borderRadius: '50%',
                  fontWeight: '700',
                  fontSize: '0.875rem'
                }}>
                  Q{index + 1}
                </span>
                <span style={{
                  padding: '0.375rem 0.75rem',
                  backgroundColor: '#f8fafc',
                  color: '#64748b',
                  borderRadius: '6px',
                  fontSize: '0.75rem',
                  fontWeight: '600',
                  textTransform: 'uppercase',
                  letterSpacing: '0.05em'
                }}>
                  {question.question_type === 'multiple_choice' ? 'Multiple Choice' : 'Text Response'}
                </span>
              </div>

              <h3 style={{ 
                fontSize: '1.125rem', 
                fontWeight: '500', 
                color: '#1e293b', 
                marginBottom: '1.5rem',
                lineHeight: '1.6',
                paddingRight: isAnswered ? '100px' : '0'
              }}>
                {question.text}
              </h3>

              {question.question_type === 'multiple_choice' ? (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                  {[1, 2, 3, 4].map((optionNum) => {
                    const optionText = question[`option${optionNum}`];
                    if (!optionText) return null;

                    return (
                      <label 
                        key={optionNum} 
                        style={{
                          display: 'flex',
                          alignItems: 'center',
                          gap: '1rem',
                          padding: '1rem 1.25rem',
                          backgroundColor: currentAnswer === optionNum ? '#eef2ff' : '#f8fafc',
                          border: currentAnswer === optionNum ? '2px solid #4f46e5' : '2px solid #e2e8f0',
                          borderRadius: '8px',
                          cursor: 'pointer',
                          transition: 'all 0.2s ease'
                        }}
                        onMouseEnter={(e) => {
                          if (currentAnswer !== optionNum) {
                            e.currentTarget.style.borderColor = '#cbd5e1';
                            e.currentTarget.style.backgroundColor = '#f1f5f9';
                          }
                        }}
                        onMouseLeave={(e) => {
                          if (currentAnswer !== optionNum) {
                            e.currentTarget.style.borderColor = '#e2e8f0';
                            e.currentTarget.style.backgroundColor = '#f8fafc';
                          }
                        }}
                      >
                        <input
                          type="radio"
                          name={`question-${question.id}`}
                          value={optionNum}
                          checked={currentAnswer === optionNum}
                          onChange={() => handleAnswerChange(question.id, optionNum)}
                          disabled={submitting}
                          style={{ width: '1.25rem', height: '1.25rem', cursor: 'pointer' }}
                        />
                        <span style={{
                          display: 'inline-flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          width: '1.75rem',
                          height: '1.75rem',
                          backgroundColor: currentAnswer === optionNum ? '#4f46e5' : 'white',
                          color: currentAnswer === optionNum ? 'white' : '#64748b',
                          borderRadius: '4px',
                          fontWeight: '600',
                          fontSize: '0.875rem',
                          flexShrink: 0
                        }}>
                          {String.fromCharCode(64 + optionNum)}
                        </span>
                        <span style={{ flex: 1, color: '#334155', fontSize: '0.9375rem' }}>{optionText}</span>
                      </label>
                    );
                  })}
                </div>
              ) : (
                <textarea
                  value={currentAnswer || ''}
                  onChange={(e) => handleAnswerChange(question.id, e.target.value)}
                  placeholder="Type your answer here..."
                  rows="6"
                  disabled={submitting}
                  style={{
                    width: '100%',
                    padding: '1rem',
                    fontSize: '0.9375rem',
                    border: '2px solid #e2e8f0',
                    borderRadius: '8px',
                    fontFamily: 'inherit',
                    resize: 'vertical',
                    minHeight: '150px',
                    transition: 'border-color 0.2s ease'
                  }}
                  onFocus={(e) => e.target.style.borderColor = '#4f46e5'}
                  onBlur={(e) => e.target.style.borderColor = '#e2e8f0'}
                />
              )}
            </div>
          );
        })}

        {/* Feedback */}
        <div style={{ 
          marginTop: '2rem',
          marginBottom: '2rem',
          padding: '2rem',
          backgroundColor: 'white',
          borderRadius: '12px',
          border: '2px solid #e2e8f0',
          boxShadow: '0 1px 3px rgba(0,0,0,0.05)'
        }}>
          <h3 style={{ fontSize: '1.125rem', fontWeight: '600', color: '#1e293b', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            💬 Feedback (Optional)
          </h3>
          <p style={{ fontSize: '0.875rem', color: '#64748b', marginBottom: '1rem' }}>
            Share your thoughts or ask questions about this quiz.
          </p>
          <textarea
            value={feedback}
            onChange={(e) => setFeedback(e.target.value)}
            placeholder="Your feedback helps us improve..."
            rows="4"
            disabled={submitting}
            style={{
              width: '100%',
              padding: '1rem',
              fontSize: '0.9375rem',
              border: '2px solid #e2e8f0',
              borderRadius: '8px',
              fontFamily: 'inherit',
              resize: 'vertical',
              transition: 'border-color 0.2s ease'
            }}
            onFocus={(e) => e.target.style.borderColor = '#4f46e5'}
            onBlur={(e) => e.target.style.borderColor = '#e2e8f0'}
          />
        </div>
      </div>

      {/* Fixed Footer */}
      <div style={{ 
        position: 'fixed',
        bottom: 0,
        left: 0,
        right: 0,
        backgroundColor: 'white',
        borderTop: '2px solid #e2e8f0',
        padding: '0.75rem 2rem',
        boxShadow: '0 -2px 8px rgba(0,0,0,0.06)',
        zIndex: 99
      }}>
        <div style={{ maxWidth: '1000px', margin: '0 auto', textAlign: 'center' }}>
          {answeredCount < questions.length && (
            <p style={{ margin: '0 0 0.5rem 0', color: '#f59e0b', fontSize: '0.8125rem', fontWeight: '500' }}>
              ⚠️ {questions.length - answeredCount} unanswered
            </p>
          )}
          <button 
            onClick={() => handleSubmitQuiz(false)}
            disabled={submitting || answeredCount === 0}
            style={{
              padding: '0.625rem 2rem',
              fontSize: '0.9375rem',
              fontWeight: '600',
              color: 'white',
              backgroundColor: submitting || answeredCount === 0 ? '#cbd5e1' : '#4f46e5',
              border: 'none',
              borderRadius: '6px',
              cursor: submitting || answeredCount === 0 ? 'not-allowed' : 'pointer',
              boxShadow: submitting || answeredCount === 0 ? 'none' : '0 2px 8px rgba(79, 70, 229, 0.3)',
              transition: 'all 0.2s ease',
              minWidth: '200px'
            }}
            onMouseEnter={(e) => {
              if (!submitting && answeredCount > 0) {
                e.target.style.backgroundColor = '#4338ca';
                e.target.style.transform = 'translateY(-1px)';
                e.target.style.boxShadow = '0 4px 12px rgba(79, 70, 229, 0.4)';
              }
            }}
            onMouseLeave={(e) => {
              if (!submitting && answeredCount > 0) {
                e.target.style.backgroundColor = '#4f46e5';
                e.target.style.transform = 'translateY(0)';
                e.target.style.boxShadow = '0 2px 8px rgba(79, 70, 229, 0.3)';
              }
            }}
          >
            {submitting ? '⏳ Submitting...' : `Submit Quiz (${answeredCount}/${questions.length})`}
          </button>
        </div>
      </div>

      <style>{`
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.6; }
        }
      `}</style>
    </div>
  );
}

export default Quiz;
