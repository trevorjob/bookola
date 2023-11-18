#!/usr/bin/python3
"""
Define the User class for the 'users' table in the database.
"""
import models
from models import db
from models.base import Base
from sqlalchemy.orm import relationship

class User(Base):
    """
    Table name in the database
    
    Attributes:
        __tablename__ (str): The name of the database table associated with this class.
        email (str): The email address of the user. It is a required field.
        first_name (str): The first name of the user. It is a required field.
        last_name (str): The last name of the user. It is a required field.
        username (str): The username chosen by the user. It is a required field.
        id (str): The unique identifier for the user. It is a required primary key.
        password_hash (str): The hashed password of the user. It is a required field.
        profile_pic_url (str): The URL of the user's profile picture. It can be None.
        registration_date (TIMESTAMP): The registration date of a user.
        last_login (TIMESTAMP): last login of a user.
    """
    __tablename__ = 'users'
    # User attributes/columns
    id = db.Column(db.String(60), primary_key=True, nullable=False)
    email = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    username = db.Column(db.String(60), nullable=False)
    password_hash = db.Column(db.String(80), nullable=False)
    profile_pic_url = db.Column(db.String(128), nullable=True)
    registration_date =db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    last_login = db.Column(db.TIMESTAMP, nullable=True)

    # Define relationship
    reviews = relationship('Review', back_populates='user')