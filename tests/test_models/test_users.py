#!/usr/bin.python3
"""Test Base for expected behaviour and documentation"""
import unittest
import models
import inspect
from models import db, Flask
import pep8 as pycodestyle
User = models.users.User


class TestUserDocs(unittest.TestCase):
    """Documentation and style test check"""

    @classmethod
    def setUpClass(cls):
        cls.functions = inspect.getmodule(User)

    def test_pep8_conformance_user(cls):
        """Test that models/user.py conforms to PEP8."""
        pep8s = pycodestyle.StyleGuide(quiet=True)
        result = pycodestyle.check_files(['models/user.py'])
        cls.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_user(cls):
        """Test that tests/test_models/test_user.py conforms to PEP8."""
        pep8s = pycodestyle.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_user.py'])
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
        for func in cls.func:
            cls.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            cls.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))
