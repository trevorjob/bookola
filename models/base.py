#!/usr/bin/python3
from flask import Flask
from models import db
from datetime import datetime

"""Base class"""


class Base(db.Model):
    """The Base class from which future classes will be derived"""

    id = db.Column(db.String(60), primary_key=True, autoincrement=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    update_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
