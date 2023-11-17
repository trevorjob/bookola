#!/usr/bin/python3
from models import db
from models.base_model import Base

"""community model"""


class Communtiy(Base, db.Model):
    """the community model to handle users and chats"""

    name = db.Column(db.String(60), nullable=False)
    active = db.Column(db.Integer, default=0, nullable=False)
    # creator_id = db.Column(db.String(60), db.ForeignKey("user.id"))
