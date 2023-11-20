#!/usr/bin/python3
"""
Define the Review class for the 'reviews' table in the database.
"""
import models
from models import db
from models.base import *


class Review(Base):
    """
    The Review class represents reviews for books in the 'reviews' table.

    Attributes:
        user_id (str): The unique identifier of the user who wrote the review.
                    It is a foreign key that references the 'users' table.
        book_id (str): The unique identifier of the book.
                    It is a foreign key that references the 'users' table.
        rating (int): The rating given to the book review. It is required.
        review_text (str): The text review. It is a required field.
        review_date (date): The date when the review was written.
                    It is automatically set to the current date and time.
    """
    __tablename__ = 'reviews'
    user_id = db.Column(db.String(60), db.ForeignKey('users.id'),
                        nullable=False)
    book_id = db.Column(db.String(60), db.ForeignKey('books.id'),
                        nullable=False)
    review_text = db.Column(db.String(200), nullable=False)
    review_date = db.Column(db.DateTime, default=db.func.current_date(),
                            nullable=False)
    rating = db.Column(db.Integer, nullable=False)
