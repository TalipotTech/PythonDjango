import React, { createContext, useState, useContext, useEffect } from 'react';
import APIService from '../services/api';

// Create the Auth Context
const AuthContext = createContext(null);

// Custom hook to use auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};

// Auth Provider Component
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Check if user is logged in on mount
  useEffect(() => {
    checkAuthStatus();
  }, []);

  // Check authentication status
  const checkAuthStatus = async () => {
    try {
      const token = localStorage.getItem('access_token');
      if (token) {
        // Try to get user profile
        const profile = await APIService.getProfile();
        setUser(profile);
        setIsAuthenticated(true);
      }
    } catch (error) {
      console.error('Auth check failed:', error);
      // Token might be invalid, clear it
      logout();
    } finally {
      setLoading(false);
    }
  };

  // Login function
  const login = async (username, password) => {
    try {
      const response = await APIService.login(username, password);
      
      // Get user profile after login
      const profile = await APIService.getProfile();
      setUser(profile);
      setIsAuthenticated(true);

      return { success: true, data: response };
    } catch (error) {
      console.error('Login failed:', error);
      return {
        success: false,
        error: error.response?.data?.detail || 'Login failed. Please check your credentials.',
      };
    }
  };

  // Register function
  const register = async (userData) => {
    try {
      const response = await APIService.register(userData);
      return { success: true, data: response };
    } catch (error) {
      console.error('Registration failed:', error);
      return {
        success: false,
        error: error.response?.data || 'Registration failed. Please try again.',
      };
    }
  };

  // Logout function
  const logout = () => {
    APIService.logout();
    setUser(null);
    setIsAuthenticated(false);
  };

  // Student login with email and password
  const studentLogin = async (email, password) => {
    try {
      // For students, we might need a different endpoint or use email as username
      const response = await APIService.login(email, password);
      
      const profile = await APIService.getProfile();
      setUser({ ...profile, role: 'student', email });
      setIsAuthenticated(true);

      return { success: true, data: response };
    } catch (error) {
      console.error('Student login failed:', error);
      return {
        success: false,
        error: error.response?.data?.detail || 'Login failed. Please check your credentials.',
      };
    }
  };

  // Admin login
  const adminLogin = async (username, password) => {
    try {
      const response = await APIService.login(username, password);
      
      const profile = await APIService.getProfile();
      setUser({ ...profile, role: 'admin' });
      setIsAuthenticated(true);

      return { success: true, data: response };
    } catch (error) {
      console.error('Admin login failed:', error);
      return {
        success: false,
        error: error.response?.data?.detail || 'Invalid admin credentials.',
      };
    }
  };

  // Student registration
  const studentRegister = async (attendeeData) => {
    try {
      const response = await APIService.registerAttendee(attendeeData);
      
      // Save email for future use
      localStorage.setItem('user_email', attendeeData.email);
      
      return { success: true, data: response };
    } catch (error) {
      console.error('Student registration failed:', error);
      return {
        success: false,
        error: error.response?.data || 'Registration failed. Please try again.',
      };
    }
  };

  const value = {
    user,
    isAuthenticated,
    loading,
    login,
    logout,
    register,
    studentLogin,
    adminLogin,
    studentRegister,
    checkAuthStatus,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export default AuthContext;
