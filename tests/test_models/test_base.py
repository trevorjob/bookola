#!/usr/bin.python3
"""Test Base for expected behaviour and documentation"""
import unittest
import models
from models.base import Base
import inspect
from models import db, app, Flask
import pep8 as pycodestyle
Base = models.base.Base
doc = models.base.__doc__


class TestBaseDoc(unittest.TestCase):
    """Documentation and style test check"""

    @classmethod
    def setUpClass(cls):
        cls.app = app
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

        cls.functions = inspect.getmembers(Base, inspect.isfunction)

    @classmethod
    def tearDownClass(cls):
        cls.app_context.pop()

    def test_pep8_conformance(cls):
        """PEP8 test check"""
        for path in ['models/base.py',
                     'tests/test_models/test_base.py']:
            with cls.subTest(path=path):
                errs = pycodestyle.Checker(path).check_all()
                cls.assertEqual(errs, 0)

    def test_module_docstring(cls):
        """Docstring test check"""
        cls.assertIsNot(doc, None,
                        "base.py need a docstring")
        cls.assertTrue(len(doc) > 1,
                       "base.py needs a docstring")

    def test_class_docstring(cls):
        """Class Docstring test check"""
        cls.assertIsNot(Base.__doc__, None,
                        "Base class needs a docstring")
        cls.assertTrue(len(Base.__doc__) >= 1,
                       "Bases class needs a docstring")

    def test_func_docstrings(cls):
        """Test for functions docstring"""
        for func_name, func_obj in cls.functions:
            with cls.subTest(function=func_name):
                cls.assertIsNotNone(
                    func_obj.__doc__,
                    f"Function {func_name} has no docstring."
                )

    """
    def test_base_model_creation(self):
        # Create a Base instance
        base_instance = Base(id='246t39g6532989db')

        # Add and commit the instance to the in-memory database
        db.session.add(base_instance)
        db.session.commit()

        # Retrieve the instance from the database
        retrieved_base_instance = Base.query.get('some_id')

        # Assert that the instance was stored and retrieved correctly
        self.assertIsNotNone(retrieved_base_instance)
        self.assertEqual(retrieved_base_instance.id, 'some_id')
        self.assertIsInstance(retrieved_base_instance.created_at, datetime)
        self.assertIsInstance(retrieved_base_instance.update_at, datetime)
  """
