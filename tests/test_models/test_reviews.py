#!/usr/bin/python3
"""Test Base for expected behaviour and documentation"""
import unittest
import models
from models.base import Base
from models.reviews import Review
import inspect
from models import db, app, Flask
import pep8 as pycodestyle
from datetime import datetime
Review = models.reviews.Review


class TestUserDocs(unittest.TestCase):
    """Documentation and style test check"""

    @classmethod
    def setUpClass(cls):
        """set up class"""
        cls.app = app
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

        cls.db = db
        cls.functions = inspect.getmembers(Review, inspect.isfunction)

    @classmethod
    def tearDownClass(cls):
        """Pop the application context to clean up"""
        cls.app_context.pop()

    def test_pep8_conformance_user(cls):
        """Test that models/reviews.py conforms to PEP8."""
        pep8s = pycodestyle.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/reviews.py'])
        cls.assertEqual(result.total_errors, 0,
                        "Found code style errors (and warnings).")

    def test_pep8_conformance_test_user(cls):
        """Test that tests/test_models/test_reviews.py conforms to PEP8."""
        pep8s = pycodestyle.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_reviews.py'])
        cls.assertEqual(result.total_errors, 0,
                        "Found code style errors (and warnings).")

    def test_user_module_docstring(cls):
        """Test for the reviews.py module docstring"""
        cls.assertIsNot(Review.__doc__, None,
                        "reviews.py needs a docstring")
        cls.assertTrue(len(Review.__doc__) >= 1,
                       "reviews.py needs a docstring")

    def test_user_class_docstring(cls):
        """Test for the review class docstring"""
        cls.assertIsNot(Review.__doc__, None,
                        "Review class needs a docstring")
        cls.assertTrue(len(Review.__doc__) >= 1,
                       "Review class needs a docstring")

    def test_user_func_docstrings(cls):
        """Test for the presence of docstrings in Review methods"""
        for func_name, func_obj in cls.functions:
            with cls.subTest(function=func_name):
                cls.assertIsNotNone(
                    func_obj.__doc__,
                    f"Function {func_name} has no docstring."
                )
