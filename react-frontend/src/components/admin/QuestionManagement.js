import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';
import '../../styles/QuestionManagement.css';

const QuestionManagement = () => {
  const navigate = useNavigate();
  const [questions, setQuestions] = useState([]);
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedSession, setSelectedSession] = useState('all');
  const [showModal, setShowModal] = useState(false);
  const [editingQuestion, setEditingQuestion] = useState(null);
  const [formData, setFormData] = useState({
    text: '',
    question_type: 'multiple_choice',
    option1: '',
    option2: '',
    option3: '',
    option4: '',
    correct_option: '',
    class_session: ''
  });

  useEffect(() => {
    if (!api.isAdminAuthenticated()) {
      navigate('/admin/login');
      return;
    }
    fetchData();
  }, [navigate]);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [questionsData, sessionsData] = await Promise.all([
        api.getAllQuestions(),
        api.getSessions()
      ]);
      
      setQuestions(Array.isArray(questionsData) ? questionsData : (questionsData.results || []));
      setSessions(Array.isArray(sessionsData) ? sessionsData : (sessionsData.results || []));
      setError('');
    } catch (err) {
      setError('Failed to load data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validation
    if (!formData.class_session) {
      setError('Please select a session');
      return;
    }

    try {
      const submitData = {
        text: formData.text,
        question_type: formData.question_type,
        class_session: parseInt(formData.class_session)
      };

      // Add MCQ fields if question type is multiple choice
      if (formData.question_type === 'multiple_choice') {
        if (!formData.option1 || !formData.option2 || !formData.correct_option) {
          setError('Please provide at least 2 options and select the correct answer');
          return;
        }
        submitData.option1 = formData.option1;
        submitData.option2 = formData.option2;
        submitData.option3 = formData.option3 || null;
        submitData.option4 = formData.option4 || null;
        submitData.correct_option = parseInt(formData.correct_option);
      }

      if (editingQuestion) {
        await api.updateQuestion(editingQuestion.id, submitData);
      } else {
        await api.createQuestion(submitData);
      }
      
      setShowModal(false);
      setEditingQuestion(null);
      resetForm();
      fetchData();
    } catch (err) {
      setError(editingQuestion ? 'Failed to update question' : 'Failed to create question');
      console.error(err);
    }
  };

  const handleEdit = (question) => {
    setEditingQuestion(question);
    setFormData({
      text: question.text,
      question_type: question.question_type,
      option1: question.option1 || '',
      option2: question.option2 || '',
      option3: question.option3 || '',
      option4: question.option4 || '',
      correct_option: question.correct_option || '',
      class_session: question.class_session
    });
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this question? This will also delete all student responses to this question.')) {
      try {
        await api.deleteQuestion(id);
        fetchData();
      } catch (err) {
        setError('Failed to delete question');
        console.error(err);
      }
    }
  };

  const handleAddNew = () => {
    resetForm();
    setEditingQuestion(null);
    setShowModal(true);
  };

  const resetForm = () => {
    setFormData({
      text: '',
      question_type: 'multiple_choice',
      option1: '',
      option2: '',
      option3: '',
      option4: '',
      correct_option: '',
      class_session: ''
    });
  };

  const handleLogout = () => {
    api.adminLogout();
    navigate('/admin/login');
  };

  const getSessionName = (sessionId) => {
    const session = sessions.find(s => s.id === sessionId);
    return session ? session.title : 'Unknown Session';
  };

  const filteredQuestions = selectedSession === 'all' 
    ? questions 
    : questions.filter(q => q.class_session === parseInt(selectedSession));

  if (loading) {
    return (
      <div className="question-management">
        <div className="loading">Loading questions...</div>
      </div>
    );
  }

  return (
    <div className="question-management">
      <div className="question-header">
        <div className="header-left">
          <h1>Question Management</h1>
          <button className="btn-back" onClick={() => navigate('/admin/dashboard')}>
            ← Back to Dashboard
          </button>
        </div>
        <div className="header-right">
          <button className="btn-primary" onClick={handleAddNew}>
            + Add New Question
          </button>
          <button className="btn-logout" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </div>

      {error && <div className="error-message">{error}</div>}

      {/* Filter Section */}
      <div className="filters-section">
        <div className="filter-group">
          <label htmlFor="sessionFilter">Filter by Session:</label>
          <select
            id="sessionFilter"
            value={selectedSession}
            onChange={(e) => setSelectedSession(e.target.value)}
            className="filter-select"
          >
            <option value="all">All Sessions</option>
            {sessions.map(session => (
              <option key={session.id} value={session.id}>
                {session.title}
              </option>
            ))}
          </select>
        </div>
        <div className="filter-stats">
          <span className="stat-badge">
            Total: {filteredQuestions.length} question{filteredQuestions.length !== 1 ? 's' : ''}
          </span>
        </div>
      </div>

      {/* Questions List */}
      {filteredQuestions.length === 0 ? (
        <div className="no-data">
          <i className="fas fa-question-circle"></i>
          <p>No questions found. Create your first question to get started!</p>
        </div>
      ) : (
        <div className="questions-grid">
          {filteredQuestions.map(question => (
            <div key={question.id} className="question-card">
              <div className="question-card-header">
                <span className={`question-type-badge ${question.question_type}`}>
                  {question.question_type === 'multiple_choice' ? (
                    <><i className="fas fa-list-ul"></i> Multiple Choice</>
                  ) : (
                    <><i className="fas fa-align-left"></i> Text Response</>
                  )}
                </span>
                <span className="session-badge">{getSessionName(question.class_session)}</span>
              </div>
              
              <div className="question-card-body">
                <h3 className="question-text">{question.text}</h3>
                
                {question.question_type === 'multiple_choice' && (
                  <div className="options-list">
                    {[1, 2, 3, 4].map(num => {
                      const option = question[`option${num}`];
                      if (!option) return null;
                      const isCorrect = question.correct_option === num;
                      return (
                        <div key={num} className={`option-item ${isCorrect ? 'correct' : ''}`}>
                          <span className="option-number">{num}</span>
                          <span className="option-text">{option}</span>
                          {isCorrect && <i className="fas fa-check-circle correct-icon"></i>}
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>

              <div className="question-card-actions">
                <button className="btn-edit" onClick={() => handleEdit(question)}>
                  <i className="fas fa-edit"></i> Edit
                </button>
                <button className="btn-delete" onClick={() => handleDelete(question.id)}>
                  <i className="fas fa-trash"></i> Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Add/Edit Question Modal */}
      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>{editingQuestion ? 'Edit Question' : 'Create New Question'}</h2>
              <button className="modal-close" onClick={() => setShowModal(false)}>×</button>
            </div>
            
            <form onSubmit={handleSubmit} className="question-form">
              <div className="form-group">
                <label htmlFor="class_session">Session *</label>
                <select
                  id="class_session"
                  name="class_session"
                  value={formData.class_session}
                  onChange={handleInputChange}
                  required
                >
                  <option value="">Select a session</option>
                  {sessions.map(session => (
                    <option key={session.id} value={session.id}>
                      {session.title}
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="question_type">Question Type *</label>
                <select
                  id="question_type"
                  name="question_type"
                  value={formData.question_type}
                  onChange={handleInputChange}
                  required
                >
                  <option value="multiple_choice">Multiple Choice</option>
                  <option value="text_response">Text Response</option>
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="text">Question Text *</label>
                <textarea
                  id="text"
                  name="text"
                  value={formData.text}
                  onChange={handleInputChange}
                  placeholder="Enter your question here..."
                  rows="3"
                  required
                />
              </div>

              {formData.question_type === 'multiple_choice' && (
                <>
                  <div className="options-section">
                    <h3>Answer Options</h3>
                    
                    <div className="form-group">
                      <label htmlFor="option1">Option 1 *</label>
                      <input
                        type="text"
                        id="option1"
                        name="option1"
                        value={formData.option1}
                        onChange={handleInputChange}
                        placeholder="Enter option 1"
                        required={formData.question_type === 'multiple_choice'}
                      />
                    </div>

                    <div className="form-group">
                      <label htmlFor="option2">Option 2 *</label>
                      <input
                        type="text"
                        id="option2"
                        name="option2"
                        value={formData.option2}
                        onChange={handleInputChange}
                        placeholder="Enter option 2"
                        required={formData.question_type === 'multiple_choice'}
                      />
                    </div>

                    <div className="form-group">
                      <label htmlFor="option3">Option 3 (Optional)</label>
                      <input
                        type="text"
                        id="option3"
                        name="option3"
                        value={formData.option3}
                        onChange={handleInputChange}
                        placeholder="Enter option 3"
                      />
                    </div>

                    <div className="form-group">
                      <label htmlFor="option4">Option 4 (Optional)</label>
                      <input
                        type="text"
                        id="option4"
                        name="option4"
                        value={formData.option4}
                        onChange={handleInputChange}
                        placeholder="Enter option 4"
                      />
                    </div>

                    <div className="form-group">
                      <label htmlFor="correct_option">Correct Answer *</label>
                      <select
                        id="correct_option"
                        name="correct_option"
                        value={formData.correct_option}
                        onChange={handleInputChange}
                        required={formData.question_type === 'multiple_choice'}
                      >
                        <option value="">Select correct option</option>
                        <option value="1">Option 1</option>
                        <option value="2">Option 2</option>
                        {formData.option3 && <option value="3">Option 3</option>}
                        {formData.option4 && <option value="4">Option 4</option>}
                      </select>
                    </div>
                  </div>
                </>
              )}

              <div className="form-actions">
                <button type="button" className="btn-cancel" onClick={() => setShowModal(false)}>
                  Cancel
                </button>
                <button type="submit" className="btn-submit">
                  {editingQuestion ? 'Update Question' : 'Create Question'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default QuestionManagement;
