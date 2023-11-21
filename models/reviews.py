#!/usr/bin/python3
"""
Define the Review class for the 'reviews' table in the database.
"""
from models import db
from models.base import *


class Review(Base, db.Model):
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

    __tablename__ = "review"
    user_id = db.Column(db.String(60), db.ForeignKey("user.id"), nullable=False)
    book_id = db.Column(db.String(60), db.ForeignKey("book.id"), nullable=False)
    review_text = db.Column(db.String(200), nullable=False)
    user = db.relationship('User', back_populates='review')