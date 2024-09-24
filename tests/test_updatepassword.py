import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from extensions import db
from models.user import User

class UpdatePasswordTestCase(unittest.TestCase):
    def setUp(self):
        """
        Set up a blank database before each test.
        """
        self.app = create_app('testing')  # Use 'testing' config with CSRF disabled
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create a test user
        self.test_user = User(username='testuser', email='test@example.com')
        self.test_user.set_password('OldPassword123')
        db.session.add(self.test_user)
        db.session.commit()

        # Verify user creation and password hashing
        user = User.query.filter_by(username='testuser').first()
        print('Test user exists:', user is not None)
        print('Password check (correct):', user.check_password('OldPassword123'))
        print('Password check (incorrect):', user.check_password('WrongPassword'))

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
        response = self.client.post('/auth/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)
        print('Login response status:', response.status_code)
        print('Login response data:', response.data.decode())
        return response

    def logout(self):
        """
        Helper method to log out a user.
        """
        response = self.client.post('/auth/logout', follow_redirects=True)
        print('Logout response status:', response.status_code)
        print('Logout response data:', response.data.decode())
        return response

    def test_update_password_success(self):
        """
        Test that a user can successfully update their password.
        """
        # Log in as the test user
        response = self.login('testuser', 'OldPassword123')
        self.assertIn(b'Welcome back, testuser!', response.data)  # Check for welcome message

        # Submit the update_password form with correct current password
        response = self.client.post('/auth/update_password', data=dict(
            current_password='OldPassword123',
            new_password='NewPassword456',
            confirm_new_password='NewPassword456'
        ), follow_redirects=True)
        print('Update password response status:', response.status_code)
        print('Update password response data:', response.data.decode())

        # Check for success flash message
        self.assertIn(b'Your password has been updated successfully.', response.data)

        # Log out
        response = self.logout()
        self.assertIn(b'Login - Nairobi Boutique Hub', response.data)  # Assuming 'Login - Nairobi Boutique Hub' is the title of the login page

        # Attempt to log in with the new password
        response = self.login('testuser', 'NewPassword456')
        self.assertIn(b'Welcome back, testuser!', response.data)  # Successful login with new password

    def test_update_password_incorrect_current_password(self):
        """
        Test that updating the password fails when the current password is incorrect.
        """
        # Log in as the test user
        response = self.login('testuser', 'OldPassword123')
        self.assertIn(b'Welcome back, testuser!', response.data)

        # Attempt to update password with incorrect current password
        response = self.client.post('/auth/update_password', data=dict(
            current_password='WrongPassword',
            new_password='NewPassword456',
            confirm_new_password='NewPassword456'
        ), follow_redirects=True)
        print('Update password with wrong current password response status:', response.status_code)
        print('Update password with wrong current password response data:', response.data.decode())

        # Check for error flash message
        self.assertIn(b'Current password is incorrect.', response.data)  # Matches the login route's flash message

    def test_update_password_mismatched_new_passwords(self):
        """
        Test that updating the password fails when the new passwords do not match.
        """
        # Log in as the test user
        response = self.login('testuser', 'OldPassword123')
        self.assertIn(b'Welcome back, testuser!', response.data)

        # Attempt to update password with mismatched new passwords
        response = self.client.post('/auth/update_password', data=dict(
            current_password='OldPassword123',
            new_password='NewPassword456',
            confirm_new_password='DifferentPassword789'
        ), follow_redirects=True)
        print('Update password with mismatched passwords response status:', response.status_code)
        print('Update password with mismatched passwords response data:', response.data.decode())

        # Check for validation error message
        self.assertIn(b'Passwords must match.', response.data)

    def test_update_password_short_new_password(self):
        """
        Test that updating the password fails when the new password is too short.
        """
        # Log in as the test user
        response = self.login('testuser', 'OldPassword123')
        self.assertIn(b'Welcome back, testuser!', response.data)

        # Attempt to update password with a short new password
        response = self.client.post('/auth/update_password', data=dict(
            current_password='OldPassword123',
            new_password='Short1',
            confirm_new_password='Short1'
        ), follow_redirects=True)
        print('Update password with short password response status:', response.status_code)
        print('Update password with short password response data:', response.data.decode())

        # Check for validation error message
        self.assertIn(b'Password must be at least 8 characters long.', response.data)

    def test_update_password_missing_fields(self):
        """
        Test that updating the password fails when required fields are missing.
        """
        # Log in as the test user
        response = self.login('testuser', 'OldPassword123')
        self.assertIn(b'Welcome back, testuser!', response.data)

        # Attempt to submit the form without filling in any fields
        response = self.client.post('/auth/update_password', data=dict(
            current_password='',
            new_password='',
            confirm_new_password=''
        ), follow_redirects=True)
        print('Update password with missing fields response status:', response.status_code)
        print('Update password with missing fields response data:', response.data.decode())

        # Check for multiple validation error messages
        self.assertIn(b'Please enter your current password.', response.data)
        self.assertIn(b'Please enter a new password.', response.data)
        self.assertIn(b'Please confirm your new password.', response.data)


if __name__ == '__main__':
    unittest.main()

