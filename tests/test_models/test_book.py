#!/usr/bin.python3
"""Test Base for expected behaviour and documentation"""
import unittest
import models
from models.base import Base
from models.book import Book
import inspect
from models import db, app, Flask
import pep8 as pycodestyle
from datetime import datetime
Book = models.book.Book


class TestUserDocs(unittest.TestCase):
    """Documentation and style test check"""

    @classmethod
    def setUpClass(cls):
        """set up class"""
        cls.app = app
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

        cls.db = db

        cls.functions = inspect.getmembers(Book, inspect.isfunction)

    @classmethod
    def tearDownClass(cls):
        """Pop the application context to clean up"""
        cls.app_context.pop()

    def test_pep8_conformance_user(cls):
        """Test that models/book.py conforms to PEP8."""
        pep8s = pycodestyle.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/book.py'])
        cls.assertEqual(result.total_errors, 0,
                        "Found code style errors (and warnings).")

    def test_pep8_conformance_test_user(cls):
        """Test that tests/test_models/test_book.py conforms to PEP8."""
        pep8s = pycodestyle.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_book.py'])
        cls.assertEqual(result.total_errors, 0,
                        "Found code style errors (and warnings).")

    def test_user_module_docstring(cls):
        """Test for the book.py module docstring"""
        cls.assertIsNot(Book.__doc__, None,
                        "book.py needs a docstring")
        cls.assertTrue(len(Book.__doc__) >= 1,
                       "book.py needs a docstring")

    def test_user_class_docstring(cls):
        """Test for the Book class docstring"""
        cls.assertIsNot(Book.__doc__, None,
                        "Book class needs a docstring")
        cls.assertTrue(len(Book.__doc__) >= 1,
                       "Book class needs a docstring")

    def test_user_func_docstrings(cls):
        """Test for the presence of docstrings in Book methods"""
        for func_name, func_obj in cls.functions:
            with cls.subTest(function=func_name):
                cls.assertIsNotNone(
                    func_obj.__doc__,
                    f"Function {func_name} has no docstring."
                )
