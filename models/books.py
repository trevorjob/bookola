#!/usr/bin/python3
"""
Define the Book class for the 'books' table in the database.
"""
from models import db
from models.base import *


book_genres = db.Table(
    "book_genres",
    db.Column("book_id", db.Integer, db.ForeignKey("book.id")),
    db.Column("genre_id", db.Integer, db.ForeignKey("genre.id")),
)


class Book(Base, db.Model):
    """
    The Book class represents book information in the 'books' table.

    Attributes:
        __tablename__ (str): The name of the database table.
        title (str): The title of the book. It is a required field.
        author (str): The author(s) of the book. It is a required field.
        publiication_date (date): The date when the book was published.
                It can be None if the publication date is unknown.
        genre (str): The genre or category of the book.
                It can be None if the genre is not specified.
        language (str): The language in which the book is written.
                It can be None if the language is not specified.
        description (str): A brief summary or description of the book.
                It can be None if a summary is not available.
        cover_image_url (str): The URL of the book's cover image.
                It can be None if the cover image is not available.
        rating (Integer): Rating.
    """

    __tablename__ = "book"
    # Book attributes/columns
    title = db.Column(db.String(128), nullable=False)
    publication_date = db.Column(db.Date, nullable=True)
    language = db.Column(db.String(60), nullable=True)
    description = db.Column(db.String(128), nullable=True)
    cover_image_url = db.Column(db.String(128), nullable=True)
    genre_id = db.Column(db.String(60), db.ForeignKey("genre.id"), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    author = db.relationship("Author", backref="book")
    genres = db.relationship("Genre", secondary=book_genres, back_populates="book")
    reviews = db.relationship("Review", backref="book")
