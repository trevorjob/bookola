#!/usr/bin/python3
"""
Define the Author class for the 'authors' table in the database.
"""

import models
from models import db
from models.base import *
from models.reviews import *


class Author(Base):
    """
    The Author class represents book information in the 'authors' table.

    Attributes:
        __tablename__ (str): The name of the database table.

    """
    __tablename__ = 'Authors'
    user_id = db.Column(db.String(60), db.ForeignKey('users.id'),
                        nullable=False)
    book_id = db.Column(db.String(60), db.ForeignKey('books.id'),
                        nullable=False)
