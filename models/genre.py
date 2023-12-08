#!/usr/bin/python3
"""
Define the Review class for the 'reviews' table in the database.
"""
from models import db
from models.base import *

genre_communities = db.Table(
    "genre_communities",
    db.Column("genre_id", db.String(60), db.ForeignKey("genre.id"), primary_key=True),
    db.Column(
        "community_id", db.String(60), db.ForeignKey("community.id"), primary_key=True
    ),
)


class Genre(Base, db.Model):
    """
    The Genre class represents the different book genres

    Attributes:
        name (str): the name of the particular genre

    """

    __tablename__ = "genre"
    name = db.Column(db.String(60), nullable=False)
    description = db.Column(db.Text, nullable=False)
    img_url =  db.Column(db.Text, nullable=False)
    books = db.relationship("Book", backref="genre")
    communities = db.relationship(
        "Community",
        secondary=genre_communities,
        backref=db.backref("genre", lazy="dynamic"),
    )
