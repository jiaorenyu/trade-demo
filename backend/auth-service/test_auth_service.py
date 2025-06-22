#!/usr/bin/env python3
"""
TECH-001 Validation Test Script
Tests all Flask microservice components
"""
import requests
import json
import time
import sys

BASE_URL = "http://localhost:5000"

def test_health_check():
    """Test health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ Health Check: {response.status_code} - {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Health Check Failed: {e}")
        return False

def test_user_registration():
    """Test user registration with marshmallow validation"""
    try:
        user_data = {
            "email": "test@example.com",
            "password": "securepassword123"
        }
        response = requests.post(f"{BASE_URL}/register", json=user_data)
        print(f"✅ User Registration: {response.status_code} - {response.json()}")
        return response.status_code == 201
    except Exception as e:
        print(f"❌ User Registration Failed: {e}")
        return False

def test_user_login():
    """Test user login and JWT token generation"""
    try:
        login_data = {
            "email": "test@example.com", 
            "password": "securepassword123"
        }
        response = requests.post(f"{BASE_URL}/login", json=login_data)
        print(f"✅ User Login: {response.status_code} - {response.json()}")
        
        if response.status_code == 200:
            token = response.json().get('access_token')
            print(f"✅ JWT Token Generated: {token[:50]}...")
            return True, token
        return False, None
    except Exception as e:
        print(f"❌ User Login Failed: {e}")
        return False, None

def test_jwt_validation(token):
    """Test JWT token validation"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/protected", headers=headers)
        print(f"✅ JWT Validation: {response.status_code} - {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ JWT Validation Failed: {e}")
        return False

def test_token_verification(token):
    """Test token verification endpoint for API Gateway"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/verify", headers=headers)
        print(f"✅ Token Verification: {response.status_code} - {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Token Verification Failed: {e}")
        return False

def test_marshmallow_validation():
    """Test marshmallow input validation"""
    try:
        # Test invalid email
        invalid_data = {
            "email": "invalid-email",
            "password": "short"
        }
        response = requests.post(f"{BASE_URL}/register", json=invalid_data)
        print(f"✅ Marshmallow Validation (Invalid): {response.status_code} - {response.json()}")
        return response.status_code == 400
    except Exception as e:
        print(f"❌ Marshmallow Validation Failed: {e}")
        return False

def main():
    """Run all TECH-001 validation tests"""
    print("🧪 TECH-001: Flask Microservices Technology Validation")
    print("=" * 60)
    
    # Wait for server to be ready
    print("⏳ Waiting for Flask server to be ready...")
    time.sleep(2)
    
    tests_passed = 0
    total_tests = 6
    
    # Test 1: Health Check
    if test_health_check():
        tests_passed += 1
    
    # Test 2: User Registration (SQLAlchemy + Marshmallow)
    if test_user_registration():
        tests_passed += 1
    
    # Test 3: User Login (JWT Token Generation)
    login_success, token = test_user_login()
    if login_success:
        tests_passed += 1
    
    # Test 4: JWT Token Validation
    if token and test_jwt_validation(token):
        tests_passed += 1
    
    # Test 5: Token Verification Endpoint
    if token and test_token_verification(token):
        tests_passed += 1
    
    # Test 6: Marshmallow Input Validation
    if test_marshmallow_validation():
        tests_passed += 1
    
    print("=" * 60)
    print(f"🎯 TECH-001 Validation Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("✅ TECH-001: Flask microservices setup verification PASSED")
        print("✅ All required components working correctly:")
        print("   - Flask application framework")
        print("   - Flask-RESTful API endpoints")
        print("   - Flask-JWT-Extended token handling")
        print("   - SQLAlchemy ORM database operations")
        print("   - Marshmallow input validation")
        print("   - Werkzeug security (password hashing)")
        return True
    else:
        print("❌ TECH-001: Flask microservices setup verification FAILED")
        print(f"   {total_tests - tests_passed} tests failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
