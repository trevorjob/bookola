#!/usr/bin/python3
"""
Define the User class for the 'users' table in the database.
"""
from models import db, mail
from models.base import Base
from flask import current_app, url_for
from flask_mail import Message


user_communities = db.Table(
    "user_communities",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column(
        "community_id", db.Integer, db.ForeignKey("community.id"), primary_key=True
    ),
)


class User(Base, db.Model):
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

    __tablename__ = "user"
    # User attributes/columns
    email = db.Column(db.String(128), unique=True, nullable=False)
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    username = db.Column(db.String(60), nullable=False)
    password_hash = db.Column(db.String(80), nullable=False)
    profile_pic_url = db.Column(db.String(128), nullable=True)
    # password_token = db.Column(db.String(128), nullable=True)

    reviews = db.relationship("Review", backref="user")
    communities = db.relationship(
        "Community",
        secondary=user_communities,
        backref=db.backref("members", lazy="dynamic"),
    ) 


def send_password_reset_email(email, token):
    subject = 'Password Reset Request'
    reset_url = url_for('reset_password', token=token, _external=True)
    body = f'Click the following link to reset your password: {reset_url}'

    message = Message(subject, recipients=[email], body=body)
    mail.send(message)