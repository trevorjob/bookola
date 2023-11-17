#!/usr/bin.python3
"""Test Base for expected behaviour and documentation"""
import unittest
import models
import inspect
import pep8 as pycodestyle
Base = models.base.Base
doc = models.base.__doc__

class TestBaseDoc(unittest.TestCase):
    """Documentation and style test check"""

    @classmethod
    def setUpClass(cls):
        cls.functions = inspect.getmodule(Base)

    def test_pep8_conformance(cls):
        """PEP8 test check"""
        for path in ['models/base.py',
                     'tests/test_model/test_base.py']:
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
        cls.assertIsNot(Base)