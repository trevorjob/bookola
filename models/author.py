#!/usr/bin/python3
"""
Define the Author class for the 'authors' table in the database.
"""

from models import db
from models.base import *


class Author(Base, db.Model):
    """
    The Author class represents book information in the 'authors' table.

    Attributes:
        __tablename__ (str): The name of the database table.

    """

    __tablename__ = "author"
    name = db.Column(db.String(60), nullable=False)
    books = db.relationship("Book", backref="author")
