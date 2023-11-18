#!/usr/bin.python3
"""Test Base for expected behaviour and documentation"""
import unittest
import models
from models.base import Base
from models.users import User
import inspect
from models import db, app, Flask
import pep8 as pycodestyle
from datetime import datetime
User = models.users.User


class TestUserDocs(unittest.TestCase):
    """Documentation and style test check"""

    @classmethod
    def setUpClass(cls):
        """set up class"""
        cls.app = app
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

        cls.db = db

        cls.functions = inspect.getmembers(User, inspect.isfunction)

    @classmethod
    def tearDownClass(cls):
        """Pop the application context to clean up"""
        cls.app_context.pop()

    def test_pep8_conformance_user(cls):
        """Test that models/users.py conforms to PEP8."""
        pep8s = pycodestyle.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/users.py'])
        cls.assertEqual(result.total_errors, 0,
                        "Found code style errors (and warnings).")

    def test_pep8_conformance_test_user(cls):
        """Test that tests/test_models/test_users.py conforms to PEP8."""
        pep8s = pycodestyle.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_users.py'])
        cls.assertEqual(result.total_errors, 0,
                        "Found code style errors (and warnings).")

    def test_user_module_docstring(cls):
        """Test for the user.py module docstring"""
        cls.assertIsNot(User.__doc__, None,
                        "user.py needs a docstring")
        cls.assertTrue(len(User.__doc__) >= 1,
                       "user.py needs a docstring")

    def test_user_class_docstring(cls):
        """Test for the City class docstring"""
        cls.assertIsNot(User.__doc__, None,
                        "User class needs a docstring")
        cls.assertTrue(len(User.__doc__) >= 1,
                       "User class needs a docstring")

    def test_user_func_docstrings(cls):
        """Test for the presence of docstrings in User methods"""
        for func_name, func_obj in cls.functions:
            with cls.subTest(function=func_name):
                cls.assertIsNotNone(
                    func_obj.__doc__,
                    f"Function {func_name} has no docstring."
                )

    """def test_user_creation(self):
        #Create a user instance
        user = User(
            email='test@example.com',
            first_name='John',
            last_name='Doe',
            username='johndoe',
            password_hash='hashed_password',
            profile_pic_url='http://example.com/profile_pic.jpg'
        )

        ex_created_at = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        # Add and commit the user to the in-memory database
        with self.app.app_context():
            self.db.session.add(user)
            self.db.session.commit()

            # Retrieve the user from the database
            retrieved_user = User.query.get('johndoe')

            # Assert that the user was stored and retrieved correctly
            self.assertIsNotNone(retrieved_user)
            self.assertEqual(retrieved_user.email, 'test@example.com')
            self.assertEqual(retrieved_user.first_name, 'John')
            self.assertEqual(retrieved_user.last_name, 'Doe')
            self.assertEqual(retrieved_user.username, 'johndoe')
            self.assertEqual(retrieved_user.password_hash, 'hashed_password')
            self.assertEqual(retrieved_user.profile_pic_url,
                             'http://example.com/profile_pic.jpg')
    """
