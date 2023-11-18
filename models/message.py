#!/usr/bin/python3
from models import db
from models.base import Base

"""community model"""


class Message(Base, db.Model):
    """the community model to handle users and chats"""

    text = db.Column(db.Text, nullable=False)
    # user_id = db.Column(db.String(60), db.ForeignKey("user.id"))
    # community_id = db.Column(db.String(60), db.ForeignKey("community.id"))
