import React, { useState } from 'react';
import { useNavigate, useLocation, Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import APIService from '../../services/api';
import Alert from '../../components/Alert';
import LoadingSpinner from '../../components/LoadingSpinner';
import './StudentLogin.css';

/**
 * StudentLogin Component
 * 
 * Allows students to login with email and password
 * Can receive session context from verification flow
 */
const StudentLogin = () => {
  const location = useLocation();
  const session = location.state?.session;
  const sessionCode = location.state?.sessionCode;
  const returnTo = location.state?.returnTo;
  const prefilledEmail = location.state?.email || '';

  const [email, setEmail] = useState(prefilledEmail);
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  const { studentLogin } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // Use the new student login API
      const response = await APIService.studentLogin(email, password);
      
      if (response.success) {
        // Store attendee information in localStorage
        localStorage.setItem('attendee_id', response.attendee.id);
        localStorage.setItem('attendee_email', response.attendee.email);
        localStorage.setItem('attendee_name', response.attendee.name);
        
        console.log('Login successful, attendee_id:', response.attendee.id);
        
        // If coming from verification flow with session, go to quiz
        if (session && session.id) {
          navigate(`/student/quiz/${session.id}`, { state: { session } });
        }
        // If returnTo is specified, use it
        else if (returnTo) {
          navigate(returnTo, { state: { session } });
        }
        // If attendee has a session, go to that session's quiz
        else if (response.attendee.session_id) {
          navigate(`/student/quiz/${response.attendee.session_id}`);
        }
        // Otherwise go to home
        else {
          navigate('/');
        }
      } else {
        setError(response.message || 'Invalid email or password.');
      }
    } catch (err) {
      console.error('Login error:', err);
      setError(err.response?.data?.message || 'Login failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="container">
        <div className="row justify-content-center">
          <div className="col-md-6 col-lg-5">
            {/* Back Button */}
            <button className="btn btn-link mb-3" onClick={() => navigate(-1)}>
              <i className="bi bi-arrow-left me-2"></i>
              Back
            </button>

            <div className="login-card">
              <div className="text-center mb-4">
                <div className="icon-circle mb-3">
                  <i className="bi bi-person-circle fs-1"></i>
                </div>
                <h2 className="mb-2">Student Login</h2>
                {session ? (
                  <div className="session-info">
                    <h5>{session.title}</h5>
                    <p className="text-muted mb-0">Login to continue</p>
                  </div>
                ) : (
                  <p className="text-muted">Enter your credentials to access the quiz</p>
                )}
              </div>

              {error && <Alert type="error" message={error} onClose={() => setError('')} />}

              <form onSubmit={handleSubmit}>
                <div className="mb-3">
                  <label htmlFor="email" className="form-label">
                    <i className="bi bi-envelope me-2"></i>
                    Email Address
                  </label>
                  <input
                    type="email"
                    className="form-control"
                    id="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    placeholder="your.email@example.com"
                  />
                </div>

                <div className="mb-3">
                  <label htmlFor="password" className="form-label">
                    <i className="bi bi-lock me-2"></i>
                    Password <span className="badge bg-secondary">Optional</span>
                  </label>
                  <input
                    type="password"
                    className="form-control"
                    id="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Enter password if you set one"
                  />
                  <small className="form-text text-muted">
                    Leave blank if you didn't set a password during registration
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
                      <i className="bi bi-box-arrow-in-right me-2"></i>
                      Login
                    </>
                  )}
                </button>
              </form>

              <div className="text-center mt-4">
                <p className="text-muted">
                  Don't have an account?{' '}
                  {session && sessionCode ? (
                    <button
                      className="btn btn-link p-0"
                      onClick={() => navigate('/student/register', {
                        state: { session, sessionCode, email }
                      })}
                    >
                      Register here
                    </button>
                  ) : (
                    <Link to="/">Get session code</Link>
                  )}
                </p>
                <Link to="/" className="text-muted">
                  <i className="bi bi-house me-2"></i>
                  Back to Home
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StudentLogin;
