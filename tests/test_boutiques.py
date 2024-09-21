import unittest
from flask_testing import TestCase
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from extensions import db
from models.boutique import Boutique
from models.user import User

class TestBoutiques(TestCase):

    def create_app(self):
        """Set up the application in testing mode."""
        app = create_app('testing')
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dev_app.db'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        return app

    def setUp(self):
        """Set up the database and create a test user."""
        self.app = self.create_app()  # Make sure the app is created here
        with self.app.app_context():  # Use app context to bind the database
            db.create_all()

            # Create a test user
            self.test_user = User(username="testuser", email="test@example.com")
            self.test_user.set_password("password")
            db.session.add(self.test_user)
            db.session.commit()

    def tearDown(self):
        """Clean up after each test."""
        with self.app.app_context():  # Ensure app context during tear down
            db.session.remove()
            db.drop_all()

    def test_get_create_boutique(self):
        """Test GET request to the create boutique page."""
        # Log in the test user
        self.client.post('/auth/login', data={
            'username': 'testuser',
            'password': 'password'
        }, follow_redirects=True)

        # Access the create boutique page
        response = self.client.get('/boutiques/create')

        # Ensure the page renders successfully
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Create a New Boutique', response.data)

    def test_post_create_boutique(self):
        """Test POST request to create a new boutique."""
        # Log in the test user
        self.client.post('/auth/login', data={
            'username': 'testuser',
            'password': 'password'
        }, follow_redirects=True)

        # Send a POST request to create a new boutique
        response = self.client.post('/boutiques/create', data=dict(
            name='Test Boutique',
            location='Nairobi',
            description='A test boutique'
        ), follow_redirects=True)

        # Ensure the POST request was successful
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Boutique created successfully!', response.data)

        # Check if the boutique exists in the database
        boutique = Boutique.query.filter_by(name='Test Boutique').first()
        self.assertIsNotNone(boutique)

    def test_create_boutique_invalid_input(self):
        """Test POST request with invalid input."""
        # Log in the test user
        self.client.post('/auth/login', data={
            'username': 'testuser',
            'password': 'password'
        }, follow_redirects=True)

        # Send a POST request with invalid data (missing location)
        response = self.client.post('/boutiques/create', data=dict(
            name='',
            location='',
            description='A test boutique with missing fields'
        ), follow_redirects=True)

        # Ensure the POST request failed due to invalid input
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid input', response.data)

if __name__ == '__main__':
    unittest.main()

