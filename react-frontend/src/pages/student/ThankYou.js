import React, { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import './ThankYou.css';

/**
 * ThankYou Component
 * 
 * Beautiful success page shown after quiz completion
 * Matches Django's thank_you.html design
 */
const ThankYou = () => {
  const navigate = useNavigate();
  const location = useLocation();
  
  const [studentName, setStudentName] = useState('');
  const [sessionTitle, setSessionTitle] = useState('');
  const [answeredCount, setAnsweredCount] = useState(0);

  useEffect(() => {
    // Get data from localStorage or location state
    const name = localStorage.getItem('attendee_name') || location.state?.attendeeName || 'Student';
    const session = location.state?.sessionTitle || 'Quiz Session';
    const count = location.state?.answeredCount || 0;

    setStudentName(name);
    setSessionTitle(session);
    setAnsweredCount(count);
  }, [location.state]);

  return (
    <div className="thankyou-container">
      {/* Success Animation */}
      <div className="success-animation">
        <div className="checkmark-circle">
          <div className="checkmark-icon">✓</div>
        </div>
      </div>

      {/* Main Content */}
      <div className="thankyou-content">
        <h1 className="thankyou-title">Submission Successful!</h1>
        <p className="thankyou-message">
          🎉 Your quiz has been submitted successfully. Great job completing the assessment!
        </p>

        {/* Submission Details */}
        <div className="submission-details">
          <div className="detail-row">
            <span className="detail-icon">👤</span>
            <div className="detail-info">
              <strong>{studentName}</strong>
              <span className="detail-label">Student Name</span>
            </div>
          </div>
          
          <div className="detail-row">
            <span className="detail-icon">📚</span>
            <div className="detail-info">
              <strong>{sessionTitle}</strong>
              <span className="detail-label">Class Session</span>
            </div>
          </div>
          
          {answeredCount > 0 && (
            <div className="detail-row">
              <span className="detail-icon">✅</span>
              <div className="detail-info">
                <strong>{answeredCount} Question{answeredCount !== 1 ? 's' : ''}</strong>
                <span className="detail-label">Answered</span>
              </div>
            </div>
          )}
        </div>

        {/* Next Steps */}
        <div className="next-steps">
          <h2>📋 What's Next?</h2>
          <div className="steps-grid">
            <div 
              className="step-card interactive"
              onClick={() => navigate('/student/dashboard')}
            >
              <div className="step-icon">📊</div>
              <h3>View Your Results</h3>
              <p>Check your performance and see your score</p>
              <span className="card-action">View Dashboard →</span>
            </div>
            
            <div 
              className="step-card interactive"
              onClick={() => navigate('/student/feedback')}
            >
              <div className="step-icon">💬</div>
              <h3>Share Feedback</h3>
              <p>Tell us about your quiz experience</p>
              <span className="card-action">Leave Feedback →</span>
            </div>
            
            <div 
              className="step-card interactive"
              onClick={() => navigate('/')}
            >
              <div className="step-icon">🎓</div>
              <h3>Continue Learning</h3>
              <p>Explore more courses and sessions</p>
              <span className="card-action">Go to Home →</span>
            </div>
          </div>
        </div>

        {/* Appreciation Message */}
        <div className="appreciation-message">
          <div className="appreciation-icon">💙</div>
          <p>Thank you for your participation and dedication to learning. Your effort makes a difference!</p>
        </div>
      </div>
    </div>
  );
};

export default ThankYou;
