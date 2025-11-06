import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import APIService from '../../services/api';
import Alert from '../../components/Alert';
import LoadingSpinner from '../../components/LoadingSpinner';
import './RegisterStudent.css';

/**
 * RegisterStudent Component
 * 
 * Student registration form after code verification
 * Collects: name, phone, password
 */
const RegisterStudent = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { register } = useAuth();
  
  const session = location.state?.session;
  const sessionCode = location.state?.sessionCode;
  const email = location.state?.email || localStorage.getItem('temp_email') || '';

  const [formData, setFormData] = useState({
    name: '',
    phone: '',
    password: ''  // Optional password field
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Redirect if no session data
  React.useEffect(() => {
    if (!session || !sessionCode) {
      navigate('/');
    }
  }, [session, sessionCode, navigate]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    
    // For phone number, only allow digits and limit to 10 digits
    if (name === 'phone') {
      const digits = value.replace(/\D/g, ''); // Remove non-digits
      if (digits.length <= 10) {
        setFormData({
          ...formData,
          [name]: digits
        });
      }
    } else {
      setFormData({
        ...formData,
        [name]: value
      });
    }
  };

  const validateForm = () => {
    if (!formData.name.trim()) {
      setError('Please enter your full name');
      return false;
    }
    
    if (!formData.phone.trim()) {
      setError('Please enter your phone number');
      return false;
    }
    
    // Validate phone number: must be exactly 10 digits
    const phoneDigits = formData.phone.replace(/\D/g, '');
    if (phoneDigits.length !== 10) {
      setError('Phone number must be exactly 10 digits');
      return false;
    }
    
    // Validate phone number format: should start with 6-9
    if (!phoneDigits.match(/^[6-9]\d{9}$/)) {
      setError('Please enter a valid Indian phone number (starting with 6-9)');
      return false;
    }
    
    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!validateForm()) {
      return;
    }

    setLoading(true);

    try {
      // Phone number is already 10 digits from validation
      const phone10Digits = formData.phone;
      
      // Prepare registration data
      const registrationData = {
        email,
        name: formData.name,
        phone: phone10Digits,
        session_code: sessionCode
      };
      
      // Only include password if user entered one
      if (formData.password && formData.password.trim()) {
        registrationData.password = formData.password;
      }
      
      // Register student using the API directly to get attendee_id
      const response = await APIService.registerAttendee(registrationData);

      console.log('Registration response:', response);

      // Store attendee information in localStorage for quiz access
      if (response.id) {
        localStorage.setItem('attendee_id', response.id);
        localStorage.setItem('attendee_email', email);
        localStorage.setItem('attendee_name', formData.name);
        console.log('Stored attendee_id:', response.id);
      } else {
        console.error('No attendee ID in response:', response);
      }

      // Success - navigate to SessionHome dashboard
      navigate(`/student/session/${session.id}`, {
        state: {
          session,
          message: 'Registration successful! Welcome to your session.'
        }
      });
    } catch (err) {
      console.error('Registration error:', err);
      console.error('Error response:', err.response?.data);
      setError(err.response?.data?.message || err.response?.data?.detail || 'Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (!session) {
    return <LoadingSpinner message="Loading..." />;
  }

  return (
    <div className="register-student-page">
      <div className="container">
        <div className="row justify-content-center">
          <div className="col-md-8 col-lg-6">
            {/* Back Button */}
            <button className="btn btn-link mb-3" onClick={() => navigate(-1)}>
              <i className="bi bi-arrow-left me-2"></i>
              Back
            </button>

            <div className="register-card">
              {/* Header */}
              <div className="text-center mb-4">
                <div className="icon-circle mb-3">
                  <i className="bi bi-person-plus fs-1"></i>
                </div>
                <h3 className="mb-2">Student Registration</h3>
                <div className="session-info">
                  <h5>{session.title}</h5>
                  <p className="text-muted mb-0">
                    <i className="bi bi-person-circle me-2"></i>
                    {session.teacher}
                  </p>
                </div>
              </div>

              {error && <Alert type="error" message={error} onClose={() => setError('')} />}

              <form onSubmit={handleSubmit}>
                {/* Email (Read-only) */}
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
                    readOnly
                    style={{ backgroundColor: '#f8f9fa' }}
                  />
                </div>

                {/* Full Name */}
                <div className="mb-3">
                  <label htmlFor="name" className="form-label">
                    <i className="bi bi-person me-2"></i>
                    Full Name *
                  </label>
                  <input
                    type="text"
                    className="form-control"
                    id="name"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    placeholder="John Doe"
                    required
                  />
                </div>

                {/* Phone Number */}
                <div className="mb-3">
                  <label htmlFor="phone" className="form-label">
                    <i className="bi bi-telephone me-2"></i>
                    Phone Number *
                  </label>
                  <input
                    type="tel"
                    className="form-control"
                    id="phone"
                    name="phone"
                    value={formData.phone}
                    onChange={handleChange}
                    placeholder="9876543210"
                    required
                    maxLength="10"
                    pattern="[6-9][0-9]{9}"
                  />
                  <small className="form-text text-muted">
                    Enter exactly 10 digits (e.g., 9876543210)
                  </small>
                </div>

                {/* Password (Optional) */}
                <div className="mb-4">
                  <label htmlFor="password" className="form-label">
                    <i className="bi bi-lock me-2"></i>
                    Password <span className="badge bg-secondary">Optional</span>
                  </label>
                  <input
                    type="password"
                    className="form-control"
                    id="password"
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    placeholder="Create a password (optional)"
                  />
                  <small className="form-text text-muted">
                    Set a password for extra security, or leave blank to login with email only
                  </small>
                </div>

                {/* Submit Button */}
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
                      Complete Registration
                    </>
                  )}
                </button>
              </form>

              {/* Login Link */}
              <div className="text-center mt-3">
                <p className="text-muted">
                  Already have an account?{' '}
                  <button
                    className="btn btn-link p-0"
                    onClick={() => navigate('/student/login', {
                      state: {
                        session,
                        sessionCode,
                        returnTo: `/student/session/${session.id}`
                      }
                    })}
                  >
                    Login here
                  </button>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RegisterStudent;
