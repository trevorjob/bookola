#!/usr/bin/python3
"""A DB Storage for sql db"""
from models import db
from models.author import Author
from models.base import Base
from models.books import Book
from models.community import Communtiy
from models.message import Message
from models.reviews import Review
from models.users import User


class DbStorage:
    """Methods that manipulate DB data"""
    def all(self, cls=None):
        """
        Retrieve all objects of a specified class or
        all objects from all models.

        Args:
            cls : The class of object to retrieve.

        Returns:
            list: A list of objects.
        """
        if cls:
            return cls.query.all()
        else:
            return db.session.query(Author, Base, Book, Communtiy,
                                    Message, Review, User).all()

    def new(self, obj):
        """
        Add a new object to the database session.

        Args:
            obj: The object to be added.
        """
        db.session.add(obj)
        db.session.commit()

    def save(self):
        """Commit changes to the database session."""
        db.session.commit()

    def reload(self):
        """Rollback the database session to
        discard any pending changes"""
        db.session.rollback()

    def delete(self, obj=None):
        """
        Delete an object from the database session.

        Args:
            obj: The object to be delated
        """
        if obj:
            db.session.delete(obj)
            db.session.commit()

    def close(cls):
        """Close the database session."""
        db.session.remove()

    def get(self, cls, id):
        """
        Retrieve an object by its class and ID.

        Args:
            cls: The class of the object.
            id: The ID of the object.

        Returns:
            object: The retrieved object.
        """
        return cls.query.get(id)

    def count(self, cls=None):
        """
        Count the number of objects for a specified class
        or all objects from all models.

        Args:
            cls: The class of the objects to count.

        Returns:
            int: The count of objects.
        """
        if cls:
            return cls.query.count()
        else:
            count = 0
            for model_class in [Author, Base, Book, Communtiy,
                                Message, Review, User]:
                count += model_class.query.count()
            return count
