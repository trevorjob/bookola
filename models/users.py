#!/usr/bin/python3
"""
Define the User class for the 'users' table in the database.
"""
import models
from models import db
from models.base import *
from models.reviews import *
from datetime import datetime


class User(Base):
    """
    Table name in the database

    Attributes:
        __tablename__ (str): The name of the database table.
        email (str): The email address of the user. Required field.
        first_name (str): The first name of the user. Required field.
        last_name (str): The last name of the user. Required field.
        username (str): The username chosen by the user. Required field.
        password_hash (str): The hashed password of the user. Required field.
        profile_pic_url (str): The URL of the user's profile picture.
    """
    __tablename__ = 'users'
    # User attributes/columns
    email = db.Column(db.String(128), unique=True, nullable=False)
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    username = db.Column(db.String(60), nullable=False)
    password_hash = db.Column(db.String(80), nullable=False)
    profile_pic_url = db.Column(db.String(128), nullable=True)

    # reviews = db.relationship("Review", backref="user")
