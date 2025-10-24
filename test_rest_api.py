"""
Simple API Test Script
Tests basic API endpoints to verify REST API is working
"""

import requests
import json

BASE_URL = "http://localhost:8000/api"

def print_section(title):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def test_api_overview():
    """Test the API overview endpoint"""
    print_section("TEST 1: API Overview")
    
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print("✓ API is accessible")
            print(f"✓ API Version: {data.get('version', 'N/A')}")
            print(f"✓ Message: {data.get('message', 'N/A')}")
            print(f"\n✓ Available endpoint categories:")
            for category in data.get('endpoints', {}).keys():
                print(f"  - {category}")
            return True
        else:
            print(f"✗ Failed with status code: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to API. Is the server running?")
        print("  Run: python manage.py runserver")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_sessions_list():
    """Test getting sessions list"""
    print_section("TEST 2: Sessions List")
    
    try:
        response = requests.get(f"{BASE_URL}/sessions/", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            count = data.get('count', 0)
            print(f"✓ Sessions endpoint accessible")
            print(f"✓ Total sessions: {count}")
            
            if count > 0:
                print(f"\n✓ Sample session:")
                session = data['results'][0]
                print(f"  - ID: {session.get('id')}")
                print(f"  - Title: {session.get('title')}")
                print(f"  - Teacher: {session.get('teacher')}")
                print(f"  - Code: {session.get('session_code')}")
            else:
                print("  (No sessions created yet)")
            return True
        else:
            print(f"✗ Failed with status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_active_sessions():
    """Test getting active sessions"""
    print_section("TEST 3: Active Sessions")
    
    try:
        response = requests.get(f"{BASE_URL}/sessions/active_sessions/", timeout=5)
        
        if response.status_code == 200:
            sessions = response.json()
            print(f"✓ Active sessions endpoint accessible")
            print(f"✓ Currently active sessions: {len(sessions)}")
            
            if len(sessions) > 0:
                for i, session in enumerate(sessions, 1):
                    print(f"\n  Active Session {i}:")
                    print(f"    - Title: {session.get('title')}")
                    print(f"    - Teacher: {session.get('teacher')}")
                    print(f"    - Code: {session.get('session_code')}")
                    print(f"    - Attendees: {session.get('attendee_count', 0)}")
            else:
                print("  (No active sessions at the moment)")
            return True
        else:
            print(f"✗ Failed with status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_user_registration():
    """Test user registration endpoint"""
    print_section("TEST 4: User Registration")
    
    register_data = {
        "username": "api_test_user",
        "email": "apitest@example.com",
        "password": "testpass123",
        "password2": "testpass123",
        "first_name": "API",
        "last_name": "Test"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/register/",
            json=register_data,
            timeout=5
        )
        
        if response.status_code == 201:
            data = response.json()
            print("✓ User registration successful")
            print(f"✓ Username: {data['user']['username']}")
            print(f"✓ Email: {data['user']['email']}")
            return True
        elif response.status_code == 400:
            errors = response.json()
            if 'username' in errors and 'already exists' in str(errors.get('username', '')).lower():
                print("✓ Registration endpoint working (user already exists)")
                return True
            else:
                print(f"⚠ Validation error: {errors}")
                return False
        else:
            print(f"✗ Failed with status code: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_token_authentication():
    """Test JWT token authentication"""
    print_section("TEST 5: JWT Authentication")
    
    login_data = {
        "username": "api_test_user",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/token/",
            json=login_data,
            timeout=5
        )
        
        if response.status_code == 200:
            tokens = response.json()
            print("✓ Authentication successful")
            print(f"✓ Access token received: {tokens['access'][:50]}...")
            print(f"✓ Refresh token received: {tokens['refresh'][:50]}...")
            
            # Test using the token
            headers = {"Authorization": f"Bearer {tokens['access']}"}
            profile_response = requests.get(
                f"{BASE_URL}/auth/profile/",
                headers=headers,
                timeout=5
            )
            
            if profile_response.status_code == 200:
                profile = profile_response.json()
                print(f"\n✓ Token validation successful")
                print(f"✓ Logged in as: {profile.get('username')}")
                return True
            else:
                print(f"⚠ Token validation failed: {profile_response.status_code}")
                return False
        else:
            print(f"✗ Login failed with status code: {response.status_code}")
            print("  Make sure the test user exists (run test 4 first)")
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "     Django Quiz/Survey System - REST API Test Suite".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "═" * 68 + "╝")
    
    print("\nℹ️  Make sure the Django server is running:")
    print("   python manage.py runserver\n")
    
    tests = [
        ("API Overview", test_api_overview),
        ("Sessions List", test_sessions_list),
        ("Active Sessions", test_active_sessions),
        ("User Registration", test_user_registration),
        ("JWT Authentication", test_token_authentication),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except KeyboardInterrupt:
            print("\n\n⚠️  Tests interrupted by user")
            break
        except Exception as e:
            print(f"\n⚠️  Unexpected error in {test_name}: {e}")
            results.append((test_name, False))
    
    # Summary
    print_section("TEST SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\nTests Passed: {passed}/{total}")
    print("\nResults:")
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}  {test_name}")
    
    if passed == total:
        print("\n🎉 All tests passed! REST API is working correctly.")
    elif passed > 0:
        print(f"\n⚠️  {total - passed} test(s) failed. Check the output above.")
    else:
        print("\n❌ All tests failed. Make sure the server is running.")
    
    print("\n" + "=" * 70)
    print("For detailed documentation, see:")
    print("  - REST_API_DOCUMENTATION.md")
    print("  - REST_API_QUICK_START.md")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()
