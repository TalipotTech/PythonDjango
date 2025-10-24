"""
Test user registration endpoint
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_registration():
    print("Testing User Registration Endpoint")
    print("=" * 60)
    
    # Test data
    user_data = {
        "username": "testuser123",
        "email": "testuser123@example.com",
        "password": "testpass123",
        "password2": "testpass123",
        "first_name": "Test",
        "last_name": "User"
    }
    
    print("\nSending registration request...")
    print(f"URL: {BASE_URL}/auth/register/")
    print(f"Data: {json.dumps(user_data, indent=2)}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/register/",
            json=user_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"\nResponse Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"\nResponse Body:")
        print(json.dumps(response.json(), indent=2))
        
        if response.status_code == 201:
            print("\n✅ SUCCESS! User registered successfully")
        elif response.status_code == 400:
            print("\n⚠️  Validation Error - Check the error details above")
        else:
            print(f"\n❌ Unexpected status code: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to server")
        print("Make sure the server is running: python manage.py runserver")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")

if __name__ == "__main__":
    test_registration()
