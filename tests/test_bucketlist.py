import unittest
from flask_testing import TestCase
from flask import url_for
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from extensions import db
from models.user import User
from models.item import Item, BucketList, Boutique

class TestBucketList(TestCase):

    def create_app(self):
        app = create_app('testing')
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF protection in the testing configuration
        return app

    def setUp(self):
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

        self.client = self.app.test_client()

        with self.app.app_context():
            print("Registered Endpoints:")
            for rule in self.app.url_map.iter_rules():
                print(f"{rule.endpoint}: {rule}")

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_add_to_bucketlist(self):
        """Test the add_to_bucketlist route for various scenarios."""

        # Log in the test user
        with self.client:
           login_response = self.client.post('/auth/login', data={
                'username': 'testuser',
                'password': 'password'
            }, follow_redirects=True)
            print("Login response status code:", login_response.status_code)
            print("Login response data:", login_response.data.decode())

            self.assertEqual(response.status_code, 200)

            # Scenario 1: Add a valid item to the bucket list
           add_response = self.client.post('/bucketlist/add', data={
                'item_id': str(self.test_item.id)
            }, follow_redirects=True)
            print("Add to bucketlist response status code:", add_response.status_code)
            print("Add to bucketlist response data:", add_response.data.decode())


            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Item added to your bucket list!', response.data)

            # Verify that the item is in the bucket list
            bucketlist_entry = BucketList.query.filter_by(user_id=self.test_user.id, item_id=self.test_item.id).first()
            self.assertIsNotNone(bucketlist_entry)

            # Scenario 2: Add the same item again (should not allow duplicates)
            response = self.client.post('/bucketlist/add', data={
                'item_id': str(self.test_item.id)
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Item already in your bucket list', response.data)

            # Scenario 3: Add an item with invalid item_id (non-integer)
            response = self.client.post('/bucketlist/add', data={
                'item_id': 'abc'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Invalid Item ID', response.data)

            # Scenario 4: Add an item with missing item_id
            response = self.client.post('/bucketlist/add', data={}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Item ID is required', response.data)

            # Scenario 5: Add a non-existent item
            response = self.client.post('/bucketlist/add', data={
                'item_id': '999'  # Assuming this ID does not exist
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Item not found', response.data)

            # Log out the test user
            response = self.client.get('/auth/logout', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

            # Scenario 6: Attempt to add an item without being logged in
            response = self.client.post('/bucketlist/add', data={
                'item_id': str(self.test_item.id)
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Login', response.data)

if __name__ == '__main__':
    unittest.main()

