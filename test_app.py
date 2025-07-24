import unittest
import json
from app import app
from user_service import UserService

class TestUserAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
    
    def test_sql_injection_protection(self):
        """Test that SQL injection attempts fail safely"""
        response = self.app.get("/user/'; DROP TABLE users; --")
        self.assertNotEqual(response.status_code, 500)
    
    def test_create_user_validation(self):
        """Test input validation works"""
        invalid_data = {"name": "", "email": "invalid"}
        response = self.app.post('/users', 
                                json=invalid_data,
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    def test_login_with_hashed_password(self):
        """Test that login works with bcrypt hashing"""
        # Create a user first
        user_data = {"name": "Test User", "email": "test@example.com", "password": "testpass123"}
        create_response = self.app.post('/users', 
                                       json=user_data,
                                       content_type='application/json')
        self.assertEqual(create_response.status_code, 201)
        
        # Test login
        login_data = {"email": "test@example.com", "password": "testpass123"}
        login_response = self.app.post('/login',
                                      json=login_data,
                                      content_type='application/json')
        self.assertEqual(login_response.status_code, 200)
        self.assertEqual(login_response.get_json()['status'], 'success')

    def test_password_strength_validation(self):
        """Test password strength requirements"""
        weak_password_data = {"name": "Test User", "email": "weak@example.com", "password": "123"}
        response = self.app.post('/users', 
                                json=weak_password_data,
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("at least 6 characters", response.get_json()['message'])
    
    def test_service_layer_directly(self):
        """Test service layer methods directly"""
        # Test user creation through service layer
        user_data = {"name": "Service Test", "email": "service@test.com", "password": "service123"}
        result, error = UserService.create_user(user_data)
        self.assertIsNone(error)
        self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main()
