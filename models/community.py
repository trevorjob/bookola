#!/usr/bin/python3
from models import db
from models.base import Base
from models.user import user_communities

"""community model"""


class Community(Base, db.Model):
    """the community model to handle users and chats"""

    __tablename__ = "community"
    name = db.Column(db.String(60), nullable=False)
    active = db.Column(db.Integer, default=0, nullable=False)
    creator_id = db.Column(db.String(60), db.ForeignKey("user.id"), nullable=False)
    creator = db.relationship(
        "User", backref=db.backref("created_communities", lazy="dynamic")
    )
    messages = db.relationship("ChatMessage", backref="community")
    # users = db.relationship(
    #     "User", secondary=user_communities, back_populates="community"
    # )
