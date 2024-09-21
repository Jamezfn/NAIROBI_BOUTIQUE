import unittest
from flask_testing import TestCase
from app import create_app, db
from models.boutique import Boutique
from models.user import User
from flask_login import login_user

class TestBoutiques(TestCase):

    def create_app(self):
        # Set up the application in testing mode
        app = create_app('testing')
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        return app

    def setUp(self):
        # Set up the database and create a test user
        with self.app.app_context():
            db.create_all()
            self.test_user = User(username="testuser", email="test@example.com")
            self.test_user.set_password("password")
            db.session.add(self.test_user)
            db.session.commit()

    def tearDown(self):
        # Clean up after each test
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_create_boutique(self):
        # Log in the test user using a POST request to the login route
        with self.client:
            self.client.post('/auth/login', data={
                'username': 'testuser',
                'password': 'password'
            }, follow_redirects=True)

            # Send a GET request to access the create boutique page
            response = self.client.get('/boutiques/create')

            # Ensure the page renders successfully
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Create a New Boutique', response.data)  # Check if the form title is in the response

    def test_post_create_boutique(self):
        # Log in the test user using a POST request to the login route
        with self.client:
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

            # Ensure the POST request was successful and the boutique was created
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Boutique created successfully!', response.data)

            # Optionally, check if the boutique exists in the database
            with self.app.app_context():
                boutique = Boutique.query.filter_by(name='Test Boutique').first()
                self.assertIsNotNone(boutique)

    def test_create_boutique_invalid_input(self):
        # Log in the test user using a POST request to the login route
        with self.client:
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

            # Ensure the POST request redirects back due to invalid input
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Invalid input', response.data)

if __name__ == '__main__':
    unittest.main()
