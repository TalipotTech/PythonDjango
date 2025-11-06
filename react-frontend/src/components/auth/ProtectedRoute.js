/**
 * PROTECTED ROUTE COMPONENT
 * 
 * BEGINNER EXPLANATION:
 * This component protects pages that require login.
 * If user is not logged in, they get redirected to login page.
 * 
 * Think of it as a "security guard" for your pages.
 * 
 * Usage:
 * <ProtectedRoute>
 *   <YourProtectedComponent />
 * </ProtectedRoute>
 */

import React from 'react';
import { Navigate } from 'react-router-dom';
import api from '../../services/api';

function ProtectedRoute({ children }) {
  // Check if user is authenticated (has valid token)
  const isAuthenticated = api.isAuthenticated();

  // If not authenticated, redirect to login page
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  // If authenticated, show the protected component
  return children;
}

export default ProtectedRoute;
