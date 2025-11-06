/**
 * API Service - Handles all communication with Django backend
 * 
 * BEGINNER EXPLANATION:
 * This file is like a "middleman" between your React app and Django server.
 * It sends requests (like login, get data) and receives responses.
 * 
 * Key concepts:
 * - axios: A library to make HTTP requests (like fetch, but easier)
 * - JWT: JSON Web Token - a secure way to prove you're logged in
 * - localStorage: Browser storage to save login tokens
 */

import axios from 'axios';

// Get the API URL from environment variables (set in .env file)
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000/api';

/**
 * Create an axios instance with default settings
 * Think of this as creating a custom "request maker" with pre-configured settings
 */
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * REQUEST INTERCEPTOR
 * This runs BEFORE every request is sent
 * It automatically adds the JWT token to requests if user is logged in
 */
api.interceptors.request.use(
  (config) => {
    // Get the saved token from browser storage
    const token = localStorage.getItem('access_token');
    
    // If token exists, add it to the request header
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

/**
 * RESPONSE INTERCEPTOR
 * This runs AFTER every response is received
 * Handles errors gracefully
 */
api.interceptors.response.use(
  (response) => response, // If successful, just return the response
  async (error) => {
    const originalRequest = error.config;

    // For student endpoints, don't try to refresh token
    // Students don't use JWT authentication
    if (error.response?.status === 401) {
      // Only redirect to login for admin/authenticated endpoints
      const isAdminEndpoint = originalRequest.url?.includes('/admin') || 
                            originalRequest.url?.includes('/auth');
      
      if (isAdminEndpoint && !originalRequest._retry) {
        originalRequest._retry = true;

        try {
          // Try to refresh the token
          const refreshToken = localStorage.getItem('refresh_token');
          if (refreshToken) {
            const response = await axios.post(`${API_BASE_URL}/auth/token/refresh/`, {
              refresh: refreshToken,
            });

            const { access } = response.data;
            
            // Save the new token
            localStorage.setItem('access_token', access);

            // Retry the original request with new token
            originalRequest.headers.Authorization = `Bearer ${access}`;
            return api(originalRequest);
          }
        } catch (refreshError) {
          // If refresh fails, log user out
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          window.location.href = '/admin/login';
          return Promise.reject(refreshError);
        }
      }
    }

    return Promise.reject(error);
  }
);

/**
 * API SERVICE CLASS
 * Contains all methods to communicate with Django backend
 */
class APIService {
  
  // ==================== AUTHENTICATION ====================
  
  /**
   * Register a new user
   * @param {Object} userData - {username, email, password, password2, first_name, last_name}
   */
  async register(userData) {
    const response = await api.post('/auth/register/', userData);
    return response.data;
  }

  /**
   * Login user and save tokens
   * @param {string} username 
   * @param {string} password 
   */
  async login(username, password) {
    const response = await api.post('/auth/token/', { username, password });
    const { access, refresh } = response.data;
    
    // Save tokens to browser storage
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
    
    return response.data;
  }

  /**
   * Get current user profile
   */
  async getProfile() {
    const response = await api.get('/auth/profile/');
    return response.data;
  }

  /**
   * Logout user by removing tokens
   */
  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user_email'); // Remove any cached email
  }

  /**
   * Check if user is logged in
   */
  isAuthenticated() {
    return !!localStorage.getItem('access_token');
  }

  // ==================== SESSIONS ====================

  /**
   * Get all sessions with optional filtering
   * @param {Object} params - {teacher, search, ordering}
   */
  async getSessions(params = {}) {
    const response = await api.get('/sessions/', { params });
    return response.data;
  }

  /**
   * Get single session by ID
   * @param {number} id 
   */
  async getSessionById(id) {
    const response = await api.get(`/sessions/${id}/`);
    return response.data;
  }

  /**
   * Get currently active sessions
   */
  async getActiveSessions() {
    const response = await api.get('/sessions/active_sessions/');
    return response.data;
  }

  /**
   * Get upcoming sessions
   */
  async getUpcomingSessions() {
    const response = await api.get('/sessions/upcoming_sessions/');
    return response.data;
  }

  /**
   * Verify if a session code is valid
   * @param {string} sessionCode 
   * @param {string} email 
   * @param {number} expectedSessionId - Optional: validate code matches this session
   */
  async verifySessionCode(sessionCode, email, expectedSessionId = null) {
    const payload = {
      session_code: sessionCode,
      email: email,
    };
    
    // Include expected session ID if provided for validation
    if (expectedSessionId) {
      payload.expected_session_id = expectedSessionId;
    }
    
    const response = await api.post('/sessions/verify_code/', payload);
    return response.data;
  }

  /**
   * Request session code to be sent to email
   * @param {string} email 
   * @param {string} sessionCode 
   */
  async requestSessionCode(email, sessionCode) {
    const response = await api.post('/sessions/send_code/', {
      email,
      session_code: sessionCode,
    });
    return response.data;
  }

  /**
   * Student login with email and password
   * @param {string} email 
   * @param {string} password 
   */
  async studentLogin(email, password) {
    const response = await api.post('/student/login/', {
      email,
      password,
    });
    return response.data;
  }

  /**
   * Create new session (Admin only)
   * @param {Object} sessionData - {title, teacher, start_time, end_time}
   */
  async createSession(sessionData) {
    const response = await api.post('/sessions/', sessionData);
    return response.data;
  }

  /**
   * Update session (Admin only)
   * @param {number} id 
   * @param {Object} sessionData 
   */
  async updateSession(id, sessionData) {
    const response = await api.put(`/sessions/${id}/`, sessionData);
    return response.data;
  }

  /**
   * Delete session (Admin only)
   * @param {number} id 
   */
  async deleteSession(id) {
    const response = await api.delete(`/sessions/${id}/`);
    return response.data;
  }

  /**
   * Get all attendees for a session
   * @param {number} sessionId 
   */
  async getSessionAttendees(sessionId) {
    const response = await api.get(`/sessions/${sessionId}/attendees/`);
    return response.data;
  }

  /**
   * Get all questions for a session
   * @param {number} sessionId 
   */
  async getSessionQuestions(sessionId) {
    const response = await api.get(`/sessions/${sessionId}/questions/`);
    return response.data;
  }

  // ==================== ATTENDEES ====================

  /**
   * Register as attendee (No auth required)
   * @param {Object} attendeeData - {name, phone, email, session_code, password}
   */
  async registerAttendee(attendeeData) {
    const response = await api.post('/students/', attendeeData);
    return response.data;
  }

  /**
   * Get all attendees (Admin only)
   */
  async getAttendees(params = {}) {
    const response = await api.get('/students/', { params });
    return response.data;
  }

  /**
   * Get attendee by ID
   * @param {number} id 
   */
  async getAttendeeById(id) {
    const response = await api.get(`/students/${id}/`);
    return response.data;
  }

  /**
   * Get my registrations by email
   * @param {string} email 
   */
  async getMyRegistrations(email) {
    const response = await api.get('/attendees/my_registrations/', {
      params: { email },
    });
    return response.data;
  }

  /**
   * Mark attendee quiz as submitted
   * @param {number} attendeeId 
   */
  async submitQuiz(attendeeId) {
    const response = await api.post(`/students/${attendeeId}/submit_quiz/`);
    return response.data;
  }

  /**
   * Get completed session IDs for an attendee
   * @param {number} attendeeId 
   */
  async getCompletedSessions(attendeeId) {
    const response = await api.get(`/student/${attendeeId}/completed-sessions/`);
    return response.data;
  }

  /**
   * Update attendee information (used by students to join new sessions)
   * @param {number} id
   * @param {Object} data
   */
  async updateAttendee(id, data) {
    const response = await api.patch(`/students/${id}/`, data);
    return response.data;
  }

  // ==================== QUESTIONS ====================

  /**
   * Get all questions (Admin only)
   */
  async getAllQuestions() {
    const response = await api.get('/questions/');
    return response.data;
  }

  /**
   * Get questions for a session
   * @param {number} sessionId 
   */
  async getQuestions(sessionId) {
    const response = await api.get('/questions/', {
      params: { class_session: sessionId },
    });
    return response.data;
  }

  /**
   * Create new question (Admin only)
   * @param {Object} questionData 
   */
  async createQuestion(questionData) {
    const response = await api.post('/questions/', questionData);
    return response.data;
  }

  /**
   * Update question (Admin only)
   * @param {number} id 
   * @param {Object} questionData 
   */
  async updateQuestion(id, questionData) {
    const response = await api.put(`/questions/${id}/`, questionData);
    return response.data;
  }

  /**
   * Delete question (Admin only)
   * @param {number} id 
   */
  async deleteQuestion(id) {
    const response = await api.delete(`/questions/${id}/`);
    return response.data;
  }

  // ==================== RESPONSES ====================

  /**
   * Submit quiz response
   * @param {Object} responseData - {attendee, question, selected_option or text_response}
   */
  async submitResponse(responseData) {
    const response = await api.post('/responses/', responseData);
    return response.data;
  }

  /**
   * Get my responses
   * @param {string} email 
   */
  async getMyResponses(email) {
    const response = await api.get('/responses/my_responses/', {
      params: { email },
    });
    return response.data;
  }

  /**
   * Get all responses (filtered)
   * @param {Object} params 
   */
  async getResponses(params = {}) {
    const response = await api.get('/responses/', { params });
    return response.data;
  }

  /**
   * Get quiz progress for attendee in a session
   * @param {number} attendeeId 
   * @param {number} sessionId 
   */
  async getQuizProgress(attendeeId, sessionId) {
    try {
      // Get all questions for the session
      const questionsData = await this.getQuestions(sessionId);
      const questions = questionsData.results || questionsData;
      
      // Get responses for this attendee
      const responsesData = await this.getResponses({ attendee: attendeeId });
      const responses = responsesData.results || responsesData;
      
      // Calculate progress
      const totalQuestions = questions.length;
      const answeredQuestions = responses.filter(r => 
        questions.some(q => q.id === r.question)
      ).length;
      const pendingQuestions = totalQuestions - answeredQuestions;
      
      return {
        total_questions: totalQuestions,
        answered: answeredQuestions,
        pending: pendingQuestions,
        questions,
        responses
      };
    } catch (error) {
      console.error('Error getting quiz progress:', error);
      throw error;
    }
  }

  // ==================== REVIEWS/FEEDBACK ====================

  /**
   * Submit feedback/review
   * @param {Object} feedbackData - {attendee, content, feedback_type}
   */
  async submitFeedback(feedbackData) {
    const response = await api.post('/feedback/', feedbackData);
    return response.data;
  }

  /**
   * Get all reviews (Admin only)
   */
  async getReviews(params = {}) {
    const response = await api.get('/reviews/', { params });
    return response.data;
  }

  // ==================== QUIZ PROGRESS ====================

  /**
   * Get my quiz progress
   * @param {string} email 
   */
  async getMyProgress(email) {
    const response = await api.get('/progress/my_progress/', {
      params: { email },
    });
    return response.data;
  }

  /**
   * Get progress by ID
   * @param {number} id 
   */
  async getProgressById(id) {
    const response = await api.get(`/progress/${id}/`);
    return response.data;
  }

  /**
   * Update completion status
   * @param {number} progressId 
   */
  async updateProgressCompletion(progressId) {
    const response = await api.post(`/progress/${progressId}/update_completion/`);
    return response.data;
  }

  // ==================== ATTENDANCE ====================

  /**
   * Get my attendance history
   * @param {string} email 
   */
  async getMyAttendance(email) {
    const response = await api.get('/attendance/my_attendance/', {
      params: { email },
    });
    return response.data;
  }

  /**
   * Get session attendees
   * @param {number} sessionId 
   */
  async getSessionAttendanceList(sessionId) {
    const response = await api.get('/attendance/session_attendees/', {
      params: { session_id: sessionId },
    });
    return response.data;
  }

  // ==================== ADMIN/STATS ====================

  /**
   * Get dashboard statistics (Admin only)
   */
  async getDashboardStats() {
    const response = await api.get('/stats/dashboard/');
    return response.data;
  }

  // ==================== ADMIN AUTHENTICATION ====================

  /**
   * Admin login with username and password
   * Returns JWT access and refresh tokens
   * @param {Object} credentials - {username, password}
   */
  async adminLogin(credentials) {
    const response = await api.post('/auth/token/', credentials);
    const { access, refresh } = response.data;
    
    // Save tokens to localStorage
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
    localStorage.setItem('user_type', 'admin');
    
    return response.data;
  }

  /**
   * Admin logout
   * Clears all stored tokens
   */
  adminLogout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user_type');
  }

  /**
   * Get current admin profile
   */
  async getAdminProfile() {
    const response = await api.get('/auth/profile/');
    return response.data;
  }

  /**
   * Check if user is authenticated as admin
   */
  isAdminAuthenticated() {
    const token = localStorage.getItem('access_token');
    const userType = localStorage.getItem('user_type');
    return !!(token && userType === 'admin');
  }

  // ==================== ADMIN - STUDENT MANAGEMENT ====================

  /**
   * Get all students (Admin only)
   * @param {Object} params - {class_session, has_submitted, search}
   */
  async getAllStudents(params = {}) {
    const response = await api.get('/students/', { params });
    return response.data;
  }

  /**
   * Get student by ID (Admin only)
   * @param {number} id
   */
  async getStudentById(id) {
    const response = await api.get(`/students/${id}/`);
    return response.data;
  }

  /**
   * Update student (Admin only)
   * @param {number} id
   * @param {Object} data
   */
  async updateStudent(id, data) {
    const response = await api.patch(`/students/${id}/`, data);
    return response.data;
  }

  /**
   * Delete student (Admin only)
   * @param {number} id
   */
  async deleteStudent(id) {
    const response = await api.delete(`/students/${id}/`);
    return response.data;
  }

  // ==================== ADMIN - RESPONSE/FEEDBACK MANAGEMENT ====================

  /**
   * Get all responses (Admin only)
   * @param {Object} params - {attendee, question}
   */
  async getAllResponses(params = {}) {
    const response = await api.get('/responses/', { params });
    return response.data;
  }

  /**
   * Get all feedback/reviews (Admin only)
   * @param {Object} params - {attendee}
   */
  async getAllFeedback(params = {}) {
    const response = await api.get('/feedback/', { params });
    return response.data;
  }

  /**
   * Delete feedback (Admin only)
   * @param {number} id
   */
  async deleteFeedback(id) {
    const response = await api.delete(`/feedback/${id}/`);
    return response.data;
  }
}

// Export a single instance of the API service
export default new APIService();
