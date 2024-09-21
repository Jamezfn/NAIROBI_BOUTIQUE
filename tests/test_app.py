import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import create_app and db from app.py
from app import create_app, db

class TestApp(unittest.TestCase):

    def setUp(self):
        """Set up the Flask test client and application context."""
        # Create the app with the 'testing' config
        self.app = create_app('testing')  # Use the testing configuration
        self.client = self.app.test_client()

        # Push the application context to handle app-level operations
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Create the database (only for testing purposes)
        db.create_all()

    def tearDown(self):
        """Clean up the app context after tests."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        """Test if the home page is loading correctly."""
        response = self.client.get('/')  # Simulate a GET request to the home page
        self.assertEqual(response.status_code, 200)  # Assert that the response code is 200 (OK)
        self.assertIn(b'Nairobi Boutique Hub', response.data)  # Check if specific content is in the page

    def test_404_page(self):
        """Test if a non-existent page returns a 404 status code."""
        response = self.client.get('/nonexistent-page')  # Simulate a GET request to a non-existent page
        self.assertEqual(response.status_code, 404)  # Assert that the response code is 404 (Not Found)

if __name__ == '__main__':
    unittest.main()
