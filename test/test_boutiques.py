import unittest
from flask_testing import TestCase
from app import app, db
from models.boutique import Boutique
from models.user import User
from flask_login import login_user

class TestBoutiques(TestCase):

    def create_app(self):
        # Configure the app for testing with an in-memory SQLite database
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        return app

    def setUp(self):
        with self.app.app_context():  # Ensure the app context is available
            db.create_all()
            # Create a test user
            self.test_user = User(username="testuser", email="test@example.com")
            self.test_user.set_password("password")
            db.session.add(self.test_user)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():  # Ensure the app context is available
            db.session.remove()
            db.drop_all()

    def test_create_boutique(self):
        # Log in the test user using a POST request to the login route
        with self.client:
            self.client.post('/auth/login', data={
                'username': 'testuser',
                'password': 'password'
            }, follow_redirects=True)

            # Create a new boutique
            response = self.client.post('/boutiques/create', data=dict(
                name='Test Boutique',
                location='Nairobi',
                description='A test boutique'
            ), follow_redirects=True)

            # Check the status code and content
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Boutique created successfully!', response.data)

if __name__ == '__main__':
    unittest.main()

