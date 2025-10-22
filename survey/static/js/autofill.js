// Auto-fill participant details when email or phone is entered
document.addEventListener('DOMContentLoaded', function() {
    const emailInput = document.getElementById('id_email');
    const phoneInput = document.getElementById('id_phone');
    const nameInput = document.getElementById('id_name');
    const ageInput = document.getElementById('id_age');
    const placeInput = document.getElementById('id_place');
    
    let debounceTimer;
    
    function checkParticipant(field, value) {
        if (!value || value.length < 3) return;
        
        // Clear previous timer
        clearTimeout(debounceTimer);
        
        // Debounce - wait 500ms after user stops typing
        debounceTimer = setTimeout(() => {
            const data = {};
            data[field] = value;
            
            fetch('/api/check-participant/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                if (data.exists) {
                    // Auto-fill the form
                    if (nameInput && data.data.name) nameInput.value = data.data.name;
                    if (emailInput && data.data.email) emailInput.value = data.data.email;
                    if (phoneInput && data.data.phone) phoneInput.value = data.data.phone;
                    if (ageInput && data.data.age) ageInput.value = data.data.age;
                    if (placeInput && data.data.place) placeInput.value = data.data.place;
                    
                    // Highlight auto-filled fields
                    [nameInput, emailInput, phoneInput, ageInput, placeInput].forEach(input => {
                        if (input && input.value) {
                            input.style.background = '#e8f5e9';
                            input.style.borderColor = '#4caf50';
                        }
                    });
                    
                    // Show success message
                    showMessage('✓ Welcome back! Your details have been filled automatically.', 'success');
                } else if (data.message) {
                    // Show info message for new users
                    showMessage(data.message, 'info');
                }
            })
            .catch(error => {
                console.error('Auto-fill error:', error);
            });
        }, 500);
    }
    
    // Check on input (as user types)
    if (emailInput) {
        emailInput.addEventListener('input', function() {
            // Only check if email looks valid
            if (this.value.includes('@')) {
                checkParticipant('email', this.value);
            }
        });
    }
    
    if (phoneInput) {
        phoneInput.addEventListener('input', function() {
            // Only check if phone is 10 digits
            if (this.value.length === 10) {
                checkParticipant('phone', this.value);
            }
        });
    }
    
    // Helper function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    // Helper function to show toast messages
    function showMessage(message, type) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `autofill-alert alert-${type}`;
        alertDiv.innerHTML = `
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <span style="font-size: 1.5rem;">${type === 'success' ? '✓' : 'ℹ'}</span>
                <span>${message}</span>
            </div>
        `;
        
        alertDiv.style.cssText = `
            position: fixed;
            top: 80px;
            right: 20px;
            z-index: 9999;
            padding: 1rem 1.5rem;
            border-radius: 12px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.2);
            max-width: 400px;
            font-weight: 600;
            animation: slideInRight 0.4s ease-out;
        `;
        
        if (type === 'success') {
            alertDiv.style.background = 'linear-gradient(135deg, #10b981, #059669)';
            alertDiv.style.color = 'white';
            alertDiv.style.border = '2px solid #059669';
        } else {
            alertDiv.style.background = '#dbeafe';
            alertDiv.style.color = '#1e40af';
            alertDiv.style.border = '2px solid #3b82f6';
        }
        
        document.body.appendChild(alertDiv);
        
        // Add slide-in animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideInRight {
                from {
                    opacity: 0;
                    transform: translateX(100%);
                }
                to {
                    opacity: 1;
                    transform: translateX(0);
                }
            }
        `;
        document.head.appendChild(style);
        
        // Remove after 4 seconds
        setTimeout(() => {
            alertDiv.style.animation = 'slideInRight 0.4s ease-out reverse';
            setTimeout(() => alertDiv.remove(), 400);
        }, 4000);
    }
});
