# tests/test_bucketlist.py

import unittest
from flask_testing import TestCase
from flask import url_for
import sys
import os

# Adjust the path to import modules correctly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from extensions import db
from models.user import User
from models.item import Item, BucketList, Boutique


class TestBucketList(TestCase):
    """Test cases for bucket list routes."""

    def create_app(self):
        """Create and configure a new app instance for each test."""
        app = create_app('testing')
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF protection in the testing configuration
        return app

    def setUp(self):
        """Set up test variables and initialize app."""
        db.create_all()

        # Create a test user
        self.test_user = User(username='testuser', email='testuser@example.com')
        self.test_user.set_password('password')
        db.session.add(self.test_user)
        db.session.commit()

        # Create a test boutique owned by the test user
        self.test_boutique = Boutique(
            name='Test Boutique',
            description='A test boutique',
            location='Test Location',
            owner_id=self.test_user.id
        )
        db.session.add(self.test_boutique)
        db.session.commit()

        # Create a test item associated with the boutique
        self.test_item = Item(
            name='Test Item',
            price=10.0,
            description='A test item.',
            boutique_id=self.test_boutique.id,
            image='test_image.jpg'
        )
        db.session.add(self.test_item)
        db.session.commit()

    def tearDown(self):
        """Clean up after each test."""
        db.session.remove()
        db.drop_all()

    def login(self, username, password):
        """Helper method to log in a user."""
        return self.client.post(
            url_for('auth.login'),
            data={'username': username, 'password': password},
            follow_redirects=True
        )

    def logout(self):
        """Helper method to log out the current user."""
        return self.client.post(
            url_for('auth.logout'),
            follow_redirects=True
        )

    def test_add_valid_item_to_bucketlist(self):
        """Test adding a valid item to the bucket list."""
        with self.client:
            # Log in the test user
            login_response = self.login('testuser', 'password')
            print("Login response status code:", login_response.status_code)
            print("Login response data:", login_response.data.decode())

            self.assertEqual(login_response.status_code, 200)
            self.assertIn(b'Welcome back, testuser!', login_response.data)
            self.assertIn(b'Logout', login_response.data)

            # Scenario 1: Add a valid item to the bucket list
            add_response = self.client.post(
                url_for('bucketlist.add_to_bucketlist'),
                data={'item_id': str(self.test_item.id)},
                follow_redirects=True
            )
            print("Add to bucketlist response status code:", add_response.status_code)
            print("Add to bucketlist response data:", add_response.data.decode())

            self.assertEqual(add_response.status_code, 200)
            self.assertIn(b'Item added to your bucket list!', add_response.data)

            # Verify that the item is in the bucket list
            bucketlist_entry = BucketList.query.filter_by(user_id=self.test_user.id, item_id=self.test_item.id).first()
            self.assertIsNotNone(bucketlist_entry)

    def test_add_duplicate_item_to_bucketlist(self):
        """Test adding the same item again should not allow duplicates."""
        with self.client:
            # Log in the test user
            self.login('testuser', 'password')

            # Add the item first time
            self.client.post(
                url_for('bucketlist.add_to_bucketlist'),
                data={'item_id': str(self.test_item.id)},
                follow_redirects=True
            )

            # Scenario 2: Add the same item again
            duplicate_response = self.client.post(
                url_for('bucketlist.add_to_bucketlist'),
                data={'item_id': str(self.test_item.id)},
                follow_redirects=True
            )
            print("Duplicate add response status code:", duplicate_response.status_code)
            print("Duplicate add response data:", duplicate_response.data.decode())

            self.assertEqual(duplicate_response.status_code, 200)
            self.assertIn(b'Item already in your bucket list', duplicate_response.data)

    def test_add_item_with_invalid_item_id(self):
        """Test adding an item with an invalid (non-integer) item_id."""
        with self.client:
            # Log in the test user
            self.login('testuser', 'password')

            # Scenario 3: Add an item with invalid item_id (non-integer)
            invalid_id_response = self.client.post(
                url_for('bucketlist.add_to_bucketlist'),
                data={'item_id': 'abc'},
                follow_redirects=True
            )
            print("Invalid item_id response status code:", invalid_id_response.status_code)
            print("Invalid item_id response data:", invalid_id_response.data.decode())

            self.assertEqual(invalid_id_response.status_code, 200)
            self.assertIn(b'Invalid Item ID', invalid_id_response.data)

    def test_add_item_with_missing_item_id(self):
        """Test adding an item with missing item_id."""
        with self.client:
            # Log in the test user
            self.login('testuser', 'password')

            # Scenario 4: Add an item with missing item_id
            missing_id_response = self.client.post(
                url_for('bucketlist.add_to_bucketlist'),
                data={},  # No item_id provided
                follow_redirects=True
            )
            print("Missing item_id response status code:", missing_id_response.status_code)
            print("Missing item_id response data:", missing_id_response.data.decode())

            self.assertEqual(missing_id_response.status_code, 200)
            self.assertIn(b'Item ID is required', missing_id_response.data)

    def test_add_nonexistent_item_to_bucketlist(self):
        """Test adding a non-existent item to the bucket list."""
        with self.client:
            # Log in the test user
            self.login('testuser', 'password')

            # Scenario 5: Add a non-existent item
            nonexistent_item_response = self.client.post(
                url_for('bucketlist.add_to_bucketlist'),
                data={'item_id': '999'},  # Assuming this ID does not exist
                follow_redirects=True
            )
            print("Non-existent item response status code:", nonexistent_item_response.status_code)
            print("Non-existent item response data:", nonexistent_item_response.data.decode())

            self.assertEqual(nonexistent_item_response.status_code, 200)
            self.assertIn(b'Item not found', nonexistent_item_response.data)

    def test_add_item_without_logging_in(self):
        """Test attempting to add an item to the bucket list without being logged in."""
        with self.client:
            # Ensure the user is logged out
            self.logout()

            # Scenario 6: Attempt to add an item without being logged in
            unauthorized_add_response = self.client.post(
                url_for('bucketlist.add_to_bucketlist'),
                data={'item_id': str(self.test_item.id)},
                follow_redirects=True
            )
            print("Unauthorized add response status code:", unauthorized_add_response.status_code)
            print("Unauthorized add response data:", unauthorized_add_response.data.decode())

            self.assertEqual(unauthorized_add_response.status_code, 200)
            self.assertIn(b'Login', unauthorized_add_response.data)


if __name__ == '__main__':
    unittest.main()

