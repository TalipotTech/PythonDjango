/**
 * INDEX.JS - Entry Point
 * 
 * BEGINNER EXPLANATION:
 * This is the first JavaScript file that runs in your React app.
 * It tells React to render your App component into the HTML page.
 * 
 * You rarely need to modify this file.
 */

import React from 'react';
import ReactDOM from 'react-dom/client';
import './styles/index.css';
import App from './App';

// Get the root element from HTML
const root = ReactDOM.createRoot(document.getElementById('root'));

// Render the App component
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
