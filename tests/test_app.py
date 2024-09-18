import unittest
from flask import Flask
from app import app, db
from models.user import User
from flask_login import current_user
from werkzeug.security import generate_password_hash

class AppTestCase(unittest.TestCase):

    def setUp(self):
        """Set up a test client and initialize the database."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory database for testing
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

        # Create a sample user
        self.user = User(username='testuser', email='test@example.com')
        self.user.set_password('password')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        """Remove the database and app context."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        """Test if the home page loads correctly."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to the Boutique Hub', response.data)  # Assuming this text exists in index.html

    def test_login_page(self):
        """Test if the login page loads correctly."""
        response = self.app.get('/auth/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_login(self):
        """Test user login functionality."""
        response = self.app.post('/auth/login', data=dict(
            username='testuser',
            password='password'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Profile', response.data)  # Assuming this text exists after login

    def test_login_invalid(self):
        """Test login with invalid credentials."""
        response = self.app.post('/auth/login', data=dict(
            username='testuser',
            password='wrongpassword'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password', response.data)

    def test_logout(self):
        """Test user logout functionality."""
        # First login
        self.app.post('/auth/login', data=dict(
            username='testuser',
            password='password'
        ), follow_redirects=True)

        # Then logout
        response = self.app.get('/auth/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Logged out', response.data)

    def test_boutique_page(self):
        """Test boutique page access."""
        response = self.app.get('/boutiques')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Boutiques', response.data)  # Assuming this text exists on the boutiques page

if __name__ == '__main__':
    unittest.main()
