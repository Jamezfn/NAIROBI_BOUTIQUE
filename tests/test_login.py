import unittest
from flask_testing import TestCase
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from extensions import db
from models.user import User
from flask import url_for

class TestAuth(TestCase):
    """Test cases for authentication routes."""

    def create_app(self):
        """Create and configure a new app instance for each test."""
        app = create_app('testing')  # Ensure 'testing' config is set up
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory DB for testing
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        return app

    def setUp(self):
        """Set up test variables and initialize app."""
        db.create_all()

        # Create a test user
        self.test_user = User(username='testuser', email='testuser@example.com')
        self.test_user.set_password('password')  # Ensure password hashing
        db.session.add(self.test_user)
        db.session.commit()

    def tearDown(self):
        """Clean up after each test."""
        db.session.remove()
        db.drop_all()

    def test_login_success(self):
        """Test that a user can log in with valid credentials."""
        response = self.client.post(
            url_for('auth.login'),
            data={'username': 'testuser', 'password': 'password'},
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome back, testuser!', response.data)
        self.assertIn(b'Logout', response.data)  # Assuming a 'Logout' link appears on successful login

    def test_login_missing_username(self):
        """Test login attempt with missing username."""
        response = self.client.post(
            url_for('auth.login'),
            data={'password': 'password'},
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Please enter both username and password', response.data)

    def test_login_missing_password(self):
        """Test login attempt with missing password."""
        response = self.client.post(
            url_for('auth.login'),
            data={'username': 'testuser'},
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Please enter both username and password', response.data)

    def test_login_invalid_credentials(self):
        """Test login attempt with invalid credentials."""
        # Invalid password
        response = self.client.post(
            url_for('auth.login'),
            data={'username': 'testuser', 'password': 'wrongpassword'},
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 401)
        self.assertIn(b'Invalid login credentials', response.data)

        # Invalid username
        response = self.client.post(
            url_for('auth.login'),
            data={'username': 'nonexistent', 'password': 'password'},
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 401)
        self.assertIn(b'Invalid login credentials', response.data)

    def test_login_case_insensitive_username(self):
        """Test that the login is case-insensitive for usernames."""
        response = self.client.post(
            url_for('auth.login'),
            data={'username': 'TestUser', 'password': 'password'},  # Different case
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome back, testuser!', response.data)
        self.assertIn(b'Logout', response.data)

if __name__ == '__main__':
    unittest.main()

