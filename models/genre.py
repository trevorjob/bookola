#!/usr/bin/python3
"""
Define the Review class for the 'reviews' table in the database.
"""
from models import db
from models.base import *
from models.community import genre_communities
from models.books import book_genres


class Genre(Base, db.Model):
    """
    The Genre class represents the different book genres

    Attributes:
        name (str): the name of the particular genre

    """

    __tablename__ = "genre"
    name = db.Column(db.String(60), nullable=False)
    books = db.relationship("Book", secondary=book_genres, back_populates="genre")
    communities = db.relationship(
        "Community", secondary=genre_communities, back_populates="genre"
    )
