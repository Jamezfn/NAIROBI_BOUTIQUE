import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from extensions import db
from models.user import User
from models.item import Boutique

class BoutiqueTestCase(unittest.TestCase):
    def setUp(self):
        """
        Set up a blank database before each test.
        """
        self.app = create_app('testing')  # Use 'testing' config
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create a test user
        self.test_user = User(username='testuser', email='test@example.com')
        self.test_user.set_password('TestPassword123')  # Ensure you have a method to set hashed passwords
        db.session.add(self.test_user)
        db.session.commit()

    def tearDown(self):
        """
        Tear down the database after each test.
        """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self, username, password):
        """
        Helper method to log in a user.
        """
        return self.client.post('/auth/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        """
        Helper method to log out a user.
        """
        return self.client.post('/auth/logout', follow_redirects=True)

    def test_create_boutique_get(self):
        """
        Test that the create boutique page loads correctly.
        """
        # Log in first
        self.login('testuser', 'TestPassword123')

        response = self.client.get('/boutiques/create')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Create Boutique', response.data)  # Assuming 'Create Boutique' is in the template

    def test_create_boutique_post_success(self):
        """
        Test that a boutique is successfully created with valid data.
        """
        # Log in first
        self.login('testuser', 'TestPassword123')

        response = self.client.post('/boutiques/create', data=dict(
            name='Test Boutique',
            description='A test boutique.',
            location='Nairobi'
        ), follow_redirects=True)

        # Check that the response contains the success flash message
        self.assertIn(b'Boutique created successfully!', response.data)

        # Check that the Boutique was created in the database
        boutique = Boutique.query.filter_by(name='Test Boutique').first()
        self.assertIsNotNone(boutique)
        self.assertEqual(boutique.description, 'A test boutique.')
        self.assertEqual(boutique.location, 'Nairobi')
        self.assertEqual(boutique.owner_id, self.test_user.id)

    def test_create_boutique_post_missing_name(self):
        """
        Test that creating a boutique fails when the name is missing.
        """
        # Log in first
        self.login('testuser', 'TestPassword123')

        response = self.client.post('/boutiques/create', data=dict(
            name='',  # Missing name
            description='A test boutique without a name.',
            location='Nairobi'
        ), follow_redirects=True)

        # Check that the response contains the error flash message
        self.assertIn(b'Please enter the boutique name.', response.data)

        # Check that the Boutique was not created in the database
        boutique = Boutique.query.filter_by(description='A test boutique without a name.').first()
        self.assertIsNone(boutique)

    def test_create_boutique_post_missing_location(self):
        """
        Test that creating a boutique fails when the location is missing.
        """
        # Log in first
        self.login('testuser', 'TestPassword123')

        response = self.client.post('/boutiques/create', data=dict(
            name='Test Boutique',
            description='A test boutique without a location.',
            location=''  # Missing location
        ), follow_redirects=True)

        # Check that the response contains the error flash message
        self.assertIn(b'Please enter the boutique location.', response.data)

        # Check that the Boutique was not created in the database
        boutique = Boutique.query.filter_by(name='Test Boutique', description='A test boutique without a location.').first()
        self.assertIsNone(boutique)

    def test_create_boutique_unauthenticated(self):
        """
        Test that unauthenticated users cannot access the create boutique page.
        """
        response = self.client.get('/boutiques/create', follow_redirects=True)
        # Assuming unauthenticated users are redirected to login page
        self.assertIn(b'Please log in to access this page.', response.data)
        # Alternatively, check the status code or the redirect location
        self.assertEqual(response.status_code, 200)  # Because of follow_redirects
        # Optionally, check if the login form is present
        self.assertIn(b'Login', response.data)  # Assuming 'Login' is in the login template

if __name__ == '__main__':
    unittest.main()

