import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from extensions import db
from models.user import User

class TestAuth(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app('testing')
        cls.app.config['TESTING'] = True
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        cls.client = cls.app.test_client()
        cls.db = db
        with cls.app.app_context():
            cls.db.create_all()

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            cls.db.drop_all()

    def setUp(self):
        # Clear the database before each test
        with self.app.app_context():
            self.db.session.remove()
            self.db.drop_all()
            self.db.create_all()

    def test_registration(self):
        # Perform registration
        response = self.client.post('/auth/register', data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword123',
            'confirm-password': 'newpassword123'
        }, follow_redirects=True)

        # Check if redirected to login page
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_login(self):
        # Create a user to test login
        with self.app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.set_password('password123')
            self.db.session.add(user)
            self.db.session.commit()

        # Perform login
        response = self.client.post('/auth/login', data={
            'username': 'testuser',
            'password': 'password123'
        }, follow_redirects=True)

        # Check for the status code and content
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h2 class="display-4">Discover Boutiques Around Nairobi</h2>', response.data)

    def test_logout(self):
        # Create a user and log in
        with self.app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.set_password('password123')
            self.db.session.add(user)
            self.db.session.commit()

        # Log the user in
        self.client.post('/auth/login', data={
            'username': 'testuser',
            'password': 'password123'
        }, follow_redirects=True)

        # Check that the user is logged in by verifying session
        with self.client.session_transaction() as session:
            self.assertIn('_user_id', session)

        # Perform logout (make sure it's a POST request)
        response = self.client.post('/auth/logout', follow_redirects=True)

        # Verify the user is logged out and redirected to the login page
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<title>Login - Nairobi Boutique Hub</title>', response.data)

        # Check that the user is logged out by verifying session
        with self.client.session_transaction() as session:
            self.assertNotIn('_user_id', session)

    def test_profile(self):
        # Create a user and log in
        with self.app.app_context():
            user = User(username='testuser', email='test@example.com', is_owner=True)
            user.set_password('password123')
            self.db.session.add(user)
            self.db.session.commit()

        # Log the user in
        self.client.post('/auth/login', data={
            'username': 'testuser',
            'password': 'password123'
        }, follow_redirects=True)

        # Access the profile page
        response = self.client.get('/auth/profile', follow_redirects=True)

        # Check that the profile page loads with correct user info
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'testuser', response.data)  # Check if the username is in the response
        self.assertIn(b'test@example.com', response.data)  # Check if the email is in the response

        # Check for the presence of "Manage Your Boutiques" and the add boutique button
        self.assertIn(b'Manage Your Boutiques', response.data)
        self.assertIn(b'Add New Boutique', response.data)

        # Check for the "Your Bucket List" section
        self.assertIn(b'Your Bucket List', response.data)

        # Check if the user has no boutiques and no bucket list items
        self.assertIn(b"You don't have any boutiques yet. Create one above!", response.data)
        self.assertIn(b"Your bucket list is empty. Add items to your bucket list!", response.data)

    def test_update_password(self):
        # Register a user first
        self.client.post('/auth/register', data={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password123',
            'confirm-password': 'password123'
        })

        # Login with the registered user
        self.client.post('/auth/login', data={
            'username': 'testuser',
            'password': 'password123'
        })

        # Test case 1: No new password provided
        response = self.client.post('/auth/update_password', data={
            'new_password': ''
        }, follow_redirects=True)
        
        # Check if redirected to the profile page
        self.assertEqual(response.status_code, 200)
        
        # Check if the flash message is present in the response after redirect
        self.assertIn(b'New password is required', response.data)

        # Test case 2: New password provided
        response = self.client.post('/auth/update_password', data={
            'new_password': 'newpassword123'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Password updated successfully!', response.data)

        # Logout after updating password
        self.client.post('/auth/logout')

        # Login with the new password to verify update
        response = self.client.post('/auth/login', data={
            'username': 'testuser',
            'password': 'newpassword123'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h2 class="display-4">Discover Boutiques Around Nairobi</h2>', response.data)  
        
if __name__ == '__main__':
    unittest.main()

