import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

/**
 * ProtectedRoute Component
 * 
 * This component wraps routes that require authentication.
 * If user is not logged in, they are redirected to the login page.
 * 
 * Usage:
 * <ProtectedRoute>
 *   <YourProtectedPage />
 * </ProtectedRoute>
 */
const ProtectedRoute = ({ children, requireAdmin = false }) => {
  const { isAuthenticated, user, loading } = useAuth();
  const location = useLocation();

  // Show loading spinner while checking auth
  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    );
  }

  // If not authenticated, redirect to login
  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // If admin required but user is not admin
  if (requireAdmin && user?.role !== 'admin') {
    return <Navigate to="/student/dashboard" replace />;
  }

  // User is authenticated, render the protected content
  return children;
};

export default ProtectedRoute;
