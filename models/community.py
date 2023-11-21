#!/usr/bin/python3
from models import db
from models.base import Base

"""community model"""

genre_communities = db.Table(
    "genre_communities",
    db.Column("genre_id", db.Integer, db.ForeignKey("genre.id")),
    db.Column("community_id", db.Integer, db.ForeignKey("community.id")),
)
user_communities = db.Table(
    "user_communities",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("community_id", db.Integer, db.ForeignKey("community.id")),
)


class Community(Base, db.Model):
    """the community model to handle users and chats"""

    __tablename__ = "community"
    name = db.Column(db.String(60), nullable=False)
    active = db.Column(db.Integer, default=0, nullable=False)
    creator_id = db.Column(db.String(60), db.ForeignKey("user.id"), nullable=False)
    genres = db.relationship("Genre", secondary=genre_communities, back_populates="community")
    messages = db.relationship("Message", backref="community")
    users = db.relationship("User",secondary=user_communities, back_populates="community")
