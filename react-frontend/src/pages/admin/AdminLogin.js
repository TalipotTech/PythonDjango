import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import Alert from '../../components/Alert';
import LoadingSpinner from '../../components/LoadingSpinner';
import './AdminLogin.css';

/**
 * AdminLogin Component
 * 
 * Allows administrators to login and access the admin dashboard
 */
const AdminLogin = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  const { adminLogin } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const result = await adminLogin(username, password);
      
      if (result.success) {
        // Redirect to admin dashboard
        navigate('/admin/dashboard');
      } else {
        setError(result.error);
      }
    } catch (err) {
      setError('Login failed. Please check your credentials.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="admin-login-page">
      <div className="container">
        <div className="row justify-content-center">
          <div className="col-md-6 col-lg-5">
            <div className="admin-login-card">
              <div className="text-center mb-4">
                <div className="admin-icon mb-3">
                  <i className="bi bi-shield-lock fs-1"></i>
                </div>
                <h2 className="mb-2">Admin Login</h2>
                <p className="text-muted">Access the administrative dashboard</p>
              </div>

              {error && <Alert type="error" message={error} onClose={() => setError('')} />}

              <form onSubmit={handleSubmit}>
                <div className="mb-3">
                  <label htmlFor="username" className="form-label">Username</label>
                  <input
                    type="text"
                    className="form-control"
                    id="username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                    placeholder="Enter admin username"
                  />
                </div>

                <div className="mb-3">
                  <label htmlFor="password" className="form-label">Password</label>
                  <input
                    type="password"
                    className="form-control"
                    id="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    placeholder="Enter admin password"
                  />
                </div>

                <button 
                  type="submit" 
                  className="btn btn-admin w-100"
                  disabled={loading}
                >
                  {loading ? <LoadingSpinner size="sm" message="" /> : 'Login as Admin'}
                </button>
              </form>

              <div className="text-center mt-4">
                <Link to="/" className="text-muted">Back to Home</Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminLogin;
