#!/usr/bin/python3
"""
Define the User class for the 'users' table in the database.
"""
from flask import url_for
from flask_login import UserMixin
from flask_mail import Message
from itsdangerous import URLSafeSerializer as Serializer

from models import db, mail, app, login_manager
from models.base import Base

user_communities = db.Table(
    "user_communities",
    db.Column("user_id", db.String, db.ForeignKey("user.id")),
    db.Column("community_id", db.String, db.ForeignKey("community.id")),
)


class User(Base, UserMixin, db.Model):
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

    # super()
    __tablename__ = "user"
    # User attributes/columns
    email = db.Column(db.Text, unique=True, nullable=False)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    profile_pic_url = db.Column(db.Text, nullable=True)
    subscribed = db.Column(db.Boolean, default=False, nullable=False)
    password_reset_token = db.Column(db.String(128), unique=True, nullable=True)

    # reviews = db.relationship("Review", backref="user")
    communities = db.relationship(
        "Community",
        secondary=user_communities,
        backref=db.backref("members", lazy="dynamic"),
    )

    def is_active(self):
        """Define your own logic for determining if the user is active or not"""
        return True

    def is_authenticated(self):
        """check if the user is authenticated"""
        return True

    def is_anonymous(self):
        """Returns False for users"""
        return False

def get_token(self,expired_sec=300):
    """Get token for users"""
    serial=Serializer(app.config['SECRET_KEY'], expire_in=expired_sec)
    return serial.dumps({'user_id':self.id}).decode('utf-8')

@staticmethod
def verify_token(token):
    """Verify users"""
    serial=Serializer(app.config['SECRET_KEY'])
    try:
        user_id=serial.loads(token)['user_id']
    except:
        return None
    return User.query.get(user_id)



def send_password_reset_email(email, token):
    """Send password reset email to user"""
    subject = "Password Reset Request"
    reset_url = url_for("reset_password", token=token, _external=True)
    body = f"Click the following link to reset your password: {reset_url}"

    message = Message(subject, recipients=[email], body=body)
    mail.send(message)
