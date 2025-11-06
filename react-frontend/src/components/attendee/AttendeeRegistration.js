/**
 * ATTENDEE REGISTRATION COMPONENT
 * 
 * BEGINNER EXPLANATION:
 * This form allows users to register for a workshop session.
 * It first verifies the session code, then collects attendee information.
 * 
 * Flow:
 * 1. User enters session code (or comes from URL)
 * 2. System verifies code is valid
 * 3. User fills registration form
 * 4. System creates attendee record
 */

import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../../services/api';
import '../../styles/Registration.css';

function AttendeeRegistration() {
  const { sessionCode } = useParams(); // Get session code from URL if provided
  const navigate = useNavigate();

  // Step 1: Session code entry/verification
  const [step, setStep] = useState(sessionCode ? 2 : 1); // Skip to step 2 if code in URL
  const [codeInput, setCodeInput] = useState(sessionCode || '');
  const [session, setSession] = useState(null);

  // Step 2: Registration form
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    session_code: sessionCode || '',
  });

  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  /**
   * Verify session code when component loads (if code in URL)
   */
  useEffect(() => {
    if (sessionCode) {
      verifyCode(sessionCode);
    }
  }, [sessionCode]);

  /**
   * Verify session code
   */
  const verifyCode = async (code) => {
    setError('');
    setLoading(true);

    try {
      const result = await api.verifySessionCode(code);
      
      if (result.valid) {
        setSession(result.session);
        setFormData({ ...formData, session_code: code });
        setStep(2); // Move to registration form
      } else {
        setError(result.message || 'Invalid session code');
      }
    } catch (err) {
      setError('Failed to verify code. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  /**
   * Handle session code form submission
   */
  const handleCodeSubmit = (e) => {
    e.preventDefault();
    verifyCode(codeInput);
  };

  /**
   * Handle registration form input changes
   */
  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  /**
   * Handle registration form submission
   */
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    // Validate phone number (10 digits)
    if (formData.phone && !/^\d{10}$/.test(formData.phone)) {
      setError('Phone number must be exactly 10 digits');
      setLoading(false);
      return;
    }

    try {
      const result = await api.registerAttendee(formData);
      
      setSuccess(true);
      
      // Save attendee ID and email for later use
      localStorage.setItem('attendee_id', result.id);
      localStorage.setItem('attendee_email', result.email);

      // Redirect to quiz after 2 seconds
      setTimeout(() => {
        navigate(`/quiz/${result.class_session}`);
      }, 2000);

    } catch (err) {
      const errors = err.response?.data;
      if (errors) {
        const errorMessage = errors.session_code?.[0] ||
                            errors.email?.[0] ||
                            errors.phone?.[0] ||
                            errors.name?.[0] ||
                            'Registration failed. Please check your information.';
        setError(errorMessage);
      } else {
        setError('Registration failed. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  // Success message
  if (success) {
    return (
      <div className="container">
        <div className="registration-card">
          <div className="alert alert-success">
            <h2>✓ Registration Successful!</h2>
            <p>Welcome to {session?.title}!</p>
            <p>Redirecting to quiz...</p>
          </div>
        </div>
      </div>
    );
  }

  // Step 1: Session Code Entry
  if (step === 1) {
    return (
      <div className="container">
        <div className="registration-card">
          <h2>Join Workshop Session</h2>
          <p className="subtitle">Enter your session code to continue</p>

          {error && <div className="alert alert-error">{error}</div>}

          <form onSubmit={handleCodeSubmit}>
            <div className="form-group">
              <label htmlFor="sessionCode">Session Code</label>
              <input
                type="text"
                id="sessionCode"
                value={codeInput}
                onChange={(e) => setCodeInput(e.target.value.toUpperCase())}
                placeholder="Enter 8-character code"
                maxLength="10"
                required
                disabled={loading}
                style={{ textTransform: 'uppercase' }}
              />
              <small>Ask your instructor for the session code</small>
            </div>

            <button 
              type="submit" 
              className="btn btn-primary btn-block"
              disabled={loading || !codeInput}
            >
              {loading ? 'Verifying...' : 'Verify Code'}
            </button>
          </form>

          <p className="auth-footer">
            Already registered? <a href="/login">Login here</a>
          </p>
        </div>
      </div>
    );
  }

  // Step 2: Registration Form
  return (
    <div className="container">
      <div className="registration-card">
        <div className="session-info-banner">
          <h3>{session?.title}</h3>
          <p>Teacher: {session?.teacher}</p>
          <code>{session?.session_code}</code>
        </div>

        <h2>Complete Registration</h2>
        <p className="subtitle">Please provide your information</p>

        {error && <div className="alert alert-error">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="name">Full Name *</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              placeholder="John Doe"
              required
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="email">Email Address *</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="john.doe@example.com"
              required
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="phone">Phone Number (10 digits)</label>
            <input
              type="tel"
              id="phone"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
              placeholder="1234567890"
              pattern="[0-9]{10}"
              disabled={loading}
            />
            <small>Optional: 10 digits, no spaces or dashes</small>
          </div>

          <button 
            type="submit" 
            className="btn btn-primary btn-block"
            disabled={loading}
          >
            {loading ? 'Registering...' : 'Register & Start Quiz'}
          </button>
        </form>

        <button 
          onClick={() => setStep(1)} 
          className="btn btn-outline btn-sm mt-3"
          disabled={loading}
        >
          ← Change Session Code
        </button>
      </div>
    </div>
  );
}

export default AttendeeRegistration;
