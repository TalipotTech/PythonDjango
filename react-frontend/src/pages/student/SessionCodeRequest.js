import React, { useState, useEffect } from 'react';
import { useParams, useLocation, useNavigate } from 'react-router-dom';
import APIService from '../../services/api';
import Alert from '../../components/Alert';
import LoadingSpinner from '../../components/LoadingSpinner';
import './SessionCodeRequest.css';

/**
 * SessionCodeRequest Component
 * 
 * Student enters email to request session code
 * Email will be sent with the session code
 */
const SessionCodeRequest = () => {
  const { id } = useParams();
  const location = useLocation();
  const navigate = useNavigate();
  
  const [session, setSession] = useState(location.state?.session || null);
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(!session);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  // Fetch session if not passed via state
  useEffect(() => {
    if (!session && id) {
      fetchSession();
    }
  }, [id, session]);

  const fetchSession = async () => {
    try {
      setLoading(true);
      const sessionData = await APIService.getSessionById(id);
      setSession(sessionData);
    } catch (err) {
      console.error('Error fetching session:', err);
      setError('Failed to load session details.');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // Request session code via API
      const response = await APIService.requestSessionCode(email, session.session_code);
      
      if (response.success) {
        setSuccess(true);
        
        // Store email for later use
        localStorage.setItem('temp_email', email);
        
        // After 2 seconds, navigate to code verification
        setTimeout(() => {
          navigate('/verify-code', { 
            state: { 
              email, 
              sessionId: id,
              session: session 
            } 
          });
        }, 2000);
      } else {
        setError(response.message || 'Failed to send session code.');
      }
      
    } catch (err) {
      console.error('Error requesting code:', err);
      setError(err.response?.data?.message || 'Failed to send session code. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (loading && !session) {
    return (
      <div className="session-code-request-page">
        <div className="container text-center py-5">
          <LoadingSpinner message="Loading session..." />
        </div>
      </div>
    );
  }

  if (!session) {
    return (
      <div className="session-code-request-page">
        <div className="container mt-5">
          <Alert type="error" message="Session not found. Please return to homepage." />
          <button className="btn btn-primary mt-3" onClick={() => navigate('/')}>
            Go to Homepage
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="session-code-request-page">
      <div className="container">
        <div className="row justify-content-center">
          <div className="col-md-8 col-lg-6">
            {/* Back Button */}
            <button className="btn btn-link mb-3" onClick={() => navigate(-1)}>
              <i className="bi bi-arrow-left me-2"></i>
              Back
            </button>

            {/* Session Info Card */}
            <div className="session-info-card mb-4">
              <h4 className="mb-3">{session.title}</h4>
              <div className="info-row">
                <i className="bi bi-person-circle"></i>
                <span>Instructor: {session.teacher}</span>
              </div>
              <div className="info-row">
                <i className="bi bi-calendar"></i>
                <span>Date: {new Date(session.start_time).toLocaleDateString()}</span>
              </div>
            </div>

            {/* Email Entry Form */}
            <div className="email-entry-card">
              <div className="text-center mb-4">
                <div className="icon-circle mb-3">
                  <i className="bi bi-envelope fs-1"></i>
                </div>
                <h3 className="mb-2">Request Session Code</h3>
                <p className="text-muted">
                  Enter your email address to receive your unique session code
                </p>
              </div>

              {error && <Alert type="error" message={error} onClose={() => setError('')} />}
              
              {success ? (
                <Alert 
                  type="success" 
                  message="Session code sent! Check your email and prepare to enter it on the next page."
                  dismissible={false}
                />
              ) : (
                <form onSubmit={handleSubmit}>
                  <div className="mb-4">
                    <label htmlFor="email" className="form-label">Email Address</label>
                    <input
                      type="email"
                      className="form-control form-control-lg"
                      id="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      placeholder="your.email@example.com"
                      required
                    />
                    <small className="form-text text-muted">
                      Use the email provided to your instructor
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
                        <i className="bi bi-send me-2"></i>
                        Send Session Code
                      </>
                    )}
                  </button>
                </form>
              )}

              <div className="text-center mt-4">
                <p className="text-muted mb-2">Already have a code?</p>
                <button 
                  className="btn btn-outline-secondary"
                  onClick={() => navigate('/verify-code')}
                >
                  Enter Session Code
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SessionCodeRequest;
