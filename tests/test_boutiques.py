import unittest
from flask_testing import TestCase
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from flask_wtf import CSRFProtect
from extensions import db
from models.item import Boutique
from models.user import User

class TestBoutiques(TestCase):

    def create_app(self):
        """Set up the application in testing mode."""
        app = create_app('testing')
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        return app

    def setUp(self):
        """Set up the database and create a test user."""
        with self.app.app_context():
            db.create_all()
            self.test_user = User(username="testuser", email="test@example.com")
            self.test_user.set_password("password")
            db.session.add(self.test_user)
            db.session.commit()
            self.test_user_id = self.test_user.id

    def tearDown(self):
        """Clean up after each test."""
        with self.app.app_context():  # Ensure app context during tear down
            db.session.remove()
            db.drop_all()

    def test_get_create_boutique(self):
        """Test GET request to the create boutique page."""
        # Log in the test user using email (if your login uses email)
        self.client.post('/auth/login', data={
            'username': 'testuser',  # or 'email': 'test@example.com' depending on auth.py
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
            'username': 'testuser',  # or 'email': 'test@example.com'
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
            'username': 'testuser',  # or 'email': 'test@example.com'
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
        self.assertIn(b'Invalid input', response.data)  # Ensure the flash message is correct

    def test_get_boutique(self):
        """Test GET request to view a boutique."""
        with self.app.app_context():
            test_user = User.query.filter_by(username='testuser').first()
            self.assertIsNotNone(test_user, "Test user should exist in the database.")

            # Create a boutique owned by the test user
            boutique = Boutique(
                name='Test Boutique',
                description='A test boutique',
                location='Nairobi',
                owner_id=self.test_user.id
            )
            db.session.add(boutique)
            db.session.commit()
            boutique_id = boutique.id

        # Log in the test user
        self.client.post('/auth/login', data={
            'username': 'testuser',
            'password': 'password'
            }, follow_redirects=True)

        # Access the boutique as the owner
        response = self.client.get(f'/boutiques/{boutique_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Boutique', response.data)
        self.assertIn(b'A test boutique', response.data)

        # Create a second user
        with self.app.app_context():
            other_user = User(username='otheruser', email='other@example.com')
            other_user.set_password('password')
            db.session.add(other_user)
            db.session.commit()

        # Log in as the other user
        self.client.post('/auth/logout', follow_redirects=True)
        self.client.post('/auth/login', data={
            'username': 'otheruser',
            'password': 'password'
        }, follow_redirects=True)

        # Try to access the boutique as a non-owner
        response = self.client.get(f'/boutiques/{boutique_id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You are not authorized to view this boutique', response.data)
        self.assertIn(b'Profile', response.data)  # Adjust based on your profile page content

    def test_update_boutique(self):
        """Test the update_boutique route for both GET and POST requests."""
        with self.app.app_context():
            # Create a boutique owned by the test user
            boutique = Boutique(
                name='Original Name',
                description='Original Description',
                location='Original Location',
                owner_id=self.test_user_id
            )
            db.session.add(boutique)
            db.session.commit()
            boutique_id = boutique.id

            # Create a second user
            other_user = User(username='otheruser', email='other@example.com')
            other_user.set_password('password')
            db.session.add(other_user)
            db.session.commit()

        # Log in as the test user (owner)
        self.client.post('/auth/login', data={
            'username': 'testuser',
            'password': 'password'
        }, follow_redirects=True)

        # Access the edit page (GET request)
        response = self.client.get(f'/boutiques/{boutique_id}/edit')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Edit Boutique', response.data)
        self.assertIn(b'Original Name', response.data)

        # Submit updated data via POST request
        response = self.client.post(f'/boutiques/{boutique_id}/edit', data={
            'name': 'Updated Name',
            'description': 'Updated Description',
            'location': 'Updated Location'
        }, follow_redirects=True)

        # Check that the response contains the success message
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Boutique updated successfully!', response.data)

        # Verify that the boutique was updated in the database
        with self.app.app_context():
            updated_boutique = Boutique.query.get(boutique_id)
            self.assertEqual(updated_boutique.name, 'Updated Name')
            self.assertEqual(updated_boutique.description, 'Updated Description')
            self.assertEqual(updated_boutique.location, 'Updated Location')

        # Log out the owner and log in as a different user
        self.client.post('/auth/logout', follow_redirects=True)
        self.client.post('/auth/login', data={
            'username': 'otheruser',
            'password': 'password'
        }, follow_redirects=True)

        # Attempt to access the edit page as a non-owner
        response = self.client.get(f'/boutiques/{boutique_id}/edit', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You are not authorized to edit this boutique', response.data)
        self.assertIn(b'User Profile', response.data)

if __name__ == '__main__':
    unittest.main()

