# REST API Quick Start Guide

## Prerequisites
- Django and REST API packages are already installed
- Database is migrated and ready

## Starting the API Server

```bash
python manage.py runserver
```

The API will be available at: `http://localhost:8000/api/`

---

## Quick Test Steps

### 1. View API Overview
Open your browser and go to:
```
http://localhost:8000/api/
```

You'll see a JSON response with all available endpoints.

---

### 2. Create a User Account

**Using Browser (Browsable API):**
1. Go to `http://localhost:8000/api/auth/register/`
2. Fill in the form:
   - Username: `testuser`
   - Email: `test@example.com`
   - Password: `testpass123`
   - Password2: `testpass123`
3. Click POST

**Using cURL (PowerShell):**
```powershell
curl -X POST http://localhost:8000/api/auth/register/ `
  -H "Content-Type: application/json" `
  -d '{\"username\":\"testuser\",\"email\":\"test@example.com\",\"password\":\"testpass123\",\"password2\":\"testpass123\"}'
```

---

### 3. Login and Get Token

**Using Browser:**
1. Go to `http://localhost:8000/api/auth/token/`
2. Enter:
   - Username: `testuser`
   - Password: `testpass123`
3. Click POST
4. **COPY the `access` token** (you'll need it)

**Using cURL:**
```powershell
curl -X POST http://localhost:8000/api/auth/token/ `
  -H "Content-Type: application/json" `
  -d '{\"username\":\"testuser\",\"password\":\"testpass123\"}'
```

---

### 4. Create a Session (Admin Required)

First, create a superuser if you haven't:
```bash
python manage.py createsuperuser
```

Then login with admin credentials and create a session:

**Using Browser:**
1. Go to `http://localhost:8000/api/sessions/`
2. Login with admin credentials if prompted
3. Fill the form:
   - Title: `Test Workshop`
   - Teacher: `Dr. Test`
   - Start time: `2025-10-24T10:00:00Z`
   - End time: `2025-10-24T12:00:00Z`
4. Click POST
5. **Note the `session_code`** generated

---

### 5. Register as Attendee (No Auth Required)

**Using Browser:**
1. Go to `http://localhost:8000/api/attendees/`
2. Fill the form:
   - Name: `John Doe`
   - Phone: `1234567890`
   - Email: `john@example.com`
   - Age: `25`
   - Place: `Boston`
   - Session code: `<use code from step 4>`
3. Click POST

---

### 6. View Active Sessions

**Using Browser:**
```
http://localhost:8000/api/sessions/active_sessions/
```

No authentication required!

---

### 7. Get Questions for a Session

**Using Browser:**
1. Go to `http://localhost:8000/api/questions/`
2. Login with your user credentials
3. Add filter: `?class_session=1` (replace 1 with your session ID)

---

### 8. Submit a Response

**Using Browser:**
1. Go to `http://localhost:8000/api/responses/`
2. Make sure you're logged in
3. Fill the form:
   - Attendee: `<your attendee ID>`
   - Question: `<question ID>`
   - Selected option: `1` (for multiple choice)
4. Click POST

---

## Testing with Python Script

Save this as `test_api.py`:

```python
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_api():
    print("=" * 60)
    print("REST API Test Script")
    print("=" * 60)
    
    # 1. Register user
    print("\n1. Registering user...")
    register_data = {
        "username": "apitest",
        "email": "apitest@example.com",
        "password": "testpass123",
        "password2": "testpass123",
        "first_name": "API",
        "last_name": "Tester"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register/", json=register_data)
        if response.status_code == 201:
            print("✓ User registered successfully")
            print(json.dumps(response.json(), indent=2))
        else:
            print("User already exists or error:", response.json())
    except Exception as e:
        print(f"Error: {e}")
    
    # 2. Login
    print("\n2. Logging in...")
    login_data = {
        "username": "apitest",
        "password": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/token/", json=login_data)
    tokens = response.json()
    access_token = tokens.get('access')
    
    if access_token:
        print("✓ Login successful")
        print(f"Access Token: {access_token[:50]}...")
    else:
        print("✗ Login failed")
        return
    
    # 3. Get profile
    print("\n3. Getting user profile...")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{BASE_URL}/auth/profile/", headers=headers)
    
    if response.status_code == 200:
        print("✓ Profile retrieved")
        print(json.dumps(response.json(), indent=2))
    
    # 4. Get active sessions
    print("\n4. Getting active sessions...")
    response = requests.get(f"{BASE_URL}/sessions/active_sessions/")
    sessions = response.json()
    
    print(f"✓ Found {len(sessions)} active session(s)")
    if sessions:
        print(json.dumps(sessions[0], indent=2))
    
    # 5. Get all sessions
    print("\n5. Getting all sessions...")
    response = requests.get(f"{BASE_URL}/sessions/")
    data = response.json()
    
    print(f"✓ Total sessions: {data.get('count', 0)}")
    
    # 6. Verify a session code (if exists)
    if sessions and len(sessions) > 0:
        session_code = sessions[0].get('session_code')
        print(f"\n6. Verifying session code: {session_code}")
        
        response = requests.post(
            f"{BASE_URL}/sessions/verify_code/",
            json={"session_code": session_code}
        )
        
        if response.status_code == 200:
            print("✓ Session code valid")
            print(json.dumps(response.json(), indent=2))
    
    print("\n" + "=" * 60)
    print("Test completed!")
    print("=" * 60)

if __name__ == "__main__":
    test_api()
```

Run it:
```bash
python test_api.py
```

---

## Common Issues & Solutions

### Issue: "Authentication credentials were not provided"
**Solution:** Make sure you include the Authorization header:
```
Authorization: Bearer <your_access_token>
```

### Issue: "Token has expired"
**Solution:** Use the refresh token to get a new access token:
```bash
curl -X POST http://localhost:8000/api/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh":"<your_refresh_token>"}'
```

### Issue: "CSRF verification failed"
**Solution:** When using forms in browser, make sure cookies are enabled. For API calls with POST/PUT/DELETE, use JSON data with `Content-Type: application/json`.

### Issue: Can't access from another computer
**Solution:** Update `ALLOWED_HOSTS` in `settings.py`:
```python
ALLOWED_HOSTS = ['*']  # For development only
```

And run server with:
```bash
python manage.py runserver 0.0.0.0:8000
```

---

## Using Postman

1. **Import Collection:**
   - Create a new collection in Postman
   - Add the base URL variable: `{{base_url}}` = `http://localhost:8000/api`

2. **Set Authorization:**
   - Type: Bearer Token
   - Token: `<your_access_token>`

3. **Test Endpoints:**
   - GET `/sessions/` - List sessions
   - POST `/auth/register/` - Register user
   - POST `/auth/token/` - Login
   - GET `/auth/profile/` - Get profile

---

## Next Steps

1. Explore all endpoints in the browsable API at `http://localhost:8000/api/`
2. Read the full documentation in `REST_API_DOCUMENTATION.md`
3. Test with your favorite HTTP client (Postman, Insomnia, etc.)
4. Integrate with frontend applications (React, Vue, Angular, etc.)

---

## API Features

✅ **Complete CRUD operations** for all models  
✅ **JWT Authentication** with token refresh  
✅ **Permission-based access** (Admin, Authenticated, Public)  
✅ **Filtering & Search** on most endpoints  
✅ **Pagination** for list views  
✅ **Progress Tracking** for quizzes  
✅ **Attendance History** tracking  
✅ **Analytics & Statistics** endpoints  
✅ **Browsable API** for easy testing  

---

## Support

For detailed documentation, see `REST_API_DOCUMENTATION.md`

Happy coding! 🚀
