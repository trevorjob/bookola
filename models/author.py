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
    The Author class represents book information in the 'books' table.

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
    __tablename__ = 'author'
    
