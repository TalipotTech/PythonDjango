import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import APIService from '../../services/api';
import Alert from '../../components/Alert';
import LoadingSpinner from '../../components/LoadingSpinner';
import './VerifyCode.css';

/**
 * VerifyCode Component
 * 
 * Student enters and verifies session code
 * Then identifies as new or returning user
 */
const VerifyCode = () => {
  const location = useLocation();
  const navigate = useNavigate();
  
  const [sessionCode, setSessionCode] = useState(location.state?.sessionCode || '');
  const [email, setEmail] = useState(location.state?.email || localStorage.getItem('temp_email') || '');
  const [session] = useState(location.state?.session || null); // Session from selected flow
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleVerifyCode = async (e) => {
    e.preventDefault();
    setError('');
    
    // Validate email is provided
    if (!email) {
      setError('Email address is required to verify the session code.');
      return;
    }
    
    setLoading(true);

    try {
      // Verify session code with API - pass expected session ID if available
      const response = await APIService.verifySessionCode(
        sessionCode, 
        email,
        session?.id  // Pass the session ID to validate against
      );
      
      if (response.valid) {
        // Automatically redirect based on user status
        if (response.is_new_user) {
          // New user - go to registration
          navigate('/register', {
            state: {
              session: response.session,
              sessionCode,
              email
            }
          });
        } else {
          // Existing user - go to login
          navigate('/student/login', {
            state: {
              session: response.session,
              sessionCode,
              email
            }
          });
        }
      } else {
        setError(response.message || 'Invalid session code. Please check and try again.');
      }
    } catch (err) {
      console.error('Error verifying code:', err);
      setError(err.response?.data?.message || 'Invalid session code. Please check and try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="verify-code-page">
      <div className="container">
        <div className="row justify-content-center">
          <div className="col-md-8 col-lg-6">
            {/* Back Button */}
            <button className="btn btn-link mb-3" onClick={() => navigate('/')}>
              <i className="bi bi-arrow-left me-2"></i>
              Back to Home
            </button>

            <div className="verify-code-card">
              {/* Show session info if available */}
              {session && (
                <div className="alert alert-info mb-4">
                  <h6 className="mb-1">
                    <i className="bi bi-info-circle me-2"></i>
                    Verifying for session:
                  </h6>
                  <strong>{session.title}</strong>
                  <div className="small text-muted">by {session.teacher}</div>
                </div>
              )}

              {/* Code Verification Section */}
              <div className="text-center mb-4">
                <div className="icon-circle mb-3">
                  <i className="bi bi-shield-lock fs-1"></i>
                </div>
                <h3 className="mb-2">Verify Session Code</h3>
                <p className="text-muted">
                  {session 
                    ? `Enter the code for ${session.title}`
                    : 'Enter the 8-character code you received via email'
                  }
                </p>
              </div>

              {error && <Alert type="error" message={error} onClose={() => setError('')} />}

              <form onSubmit={handleVerifyCode}>
                <div className="mb-3">
                  <label htmlFor="sessionCode" className="form-label">Session Code</label>
                  <input
                    type="text"
                    className="form-control form-control-lg text-center text-uppercase code-input"
                    id="sessionCode"
                    value={sessionCode}
                    onChange={(e) => setSessionCode(e.target.value.toUpperCase())}
                    placeholder="ABC12345"
                    required
                    maxLength="8"
                    style={{ letterSpacing: '4px', fontSize: '1.5rem' }}
                  />
                  <small className="form-text text-muted">
                    Example: ABC12345
                  </small>
                </div>

                <div className="mb-3">
                  <label htmlFor="email" className="form-label">Email Address</label>
                  <input
                    type="email"
                    className="form-control"
                    id="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="your.email@example.com"
                    required
                  />
                  <small className="form-text text-muted">
                    Use the same email you entered to request the code
                  </small>
                </div>

                <button 
                  type="submit" 
                  className="btn btn-primary btn-lg w-100"
                  disabled={loading}
                >
                  {loading ? (
                    <LoadingSpinner size="sm" message="" />
                  ) : (
                    <>
                      <i className="bi bi-check-circle me-2"></i>
                      Verify Code
                    </>
                  )}
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default VerifyCode;
