/**
 * MAIN APP COMPONENT
 * 
 * BEGINNER EXPLANATION:
 * This is the "main" file of your React app.
 * It defines all the routes (URLs) and which component to show for each route.
 * 
 * Think of it as a "map" of your application.
 * 
 * Key concepts:
 * - BrowserRouter: Enables navigation in React
 * - Routes: Container for all route definitions
 * - Route: Defines a URL path and what component to show
 * - ProtectedRoute: Wraps components that need authentication
 */

import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';

// Import pages
import HomePage from './pages/HomePage';
import StudentLogin from './pages/student/StudentLogin';
import SessionCodeRequest from './pages/student/SessionCodeRequest';
import VerifyCode from './pages/student/VerifyCode';
import RegisterStudent from './pages/student/RegisterStudent';
import SessionHome from './pages/student/SessionHome';
import StudentDashboard from './pages/student/StudentDashboard';
import ThankYou from './pages/student/ThankYou';
import Quiz from './components/quiz/Quiz';
import Feedback from './components/feedback/Feedback';

// Import admin components
import AdminLogin from './components/admin/AdminLogin';
import AdminDashboard from './components/admin/AdminDashboard';
import SessionManagement from './components/admin/SessionManagement';
import StudentManagement from './components/admin/StudentManagement';
import QuestionManagement from './components/admin/QuestionManagement';
import FeedbackManagement from './components/admin/FeedbackManagement';

// Import styles
import './styles/App.css';


function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="app-container">
          <Routes>
            {/* PUBLIC ROUTES */}
            <Route path="/" element={<HomePage />} />
            <Route path="/student/login" element={<StudentLogin />} />
            
            {/* STUDENT PUBLIC ROUTES (Pre-authentication) */}
            <Route path="/session-code-request/:id" element={<SessionCodeRequest />} />
            <Route path="/verify-code" element={<VerifyCode />} />
            <Route path="/register" element={<RegisterStudent />} />
            <Route path="/student/quiz/:sessionId" element={<Quiz />} />
            <Route path="/student/dashboard" element={<StudentDashboard />} />
            <Route path="/student/session/:id" element={<SessionHome />} />
            <Route path="/student/feedback" element={<Feedback />} />
            <Route path="/thank-you" element={<ThankYou />} />

            {/* ADMIN ROUTES */}
            <Route path="/admin/login" element={<AdminLogin />} />
            <Route path="/admin/dashboard" element={<AdminDashboard />} />
            <Route path="/admin/sessions" element={<SessionManagement />} />
            <Route path="/admin/students" element={<StudentManagement />} />
            <Route path="/admin/questions" element={<QuestionManagement />} />
            <Route path="/admin/feedback" element={<FeedbackManagement />} />

            {/* 404 Page */}
            <Route path="*" element={<NotFound />} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

// Simple 404 page
function NotFound() {
  return (
    <div className="container text-center mt-5">
      <h1 className="display-1">404</h1>
      <p className="lead">Page not found</p>
      <a href="/" className="btn btn-primary">Go Home</a>
    </div>
  );
}

export default App;

