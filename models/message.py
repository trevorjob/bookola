#!/usr/bin/python3
from models import db
from models.base import Base

"""community model"""


class ChatMessage(Base, db.Model):
    """the community model to handle users and chats"""

    __tablename__ = "message"
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.String(60), db.ForeignKey("user.id"), nullable=False)
    community_id = db.Column(
        db.String(60), db.ForeignKey("community.id"), nullable=False
    )
    user = db.relationship("User", backref="message")
