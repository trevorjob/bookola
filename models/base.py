#!/usr/bin/python3
"""Base class"""
from flask import Flask
from models import db
from datetime import datetime


class Base(db.Model):
    """Base class from which future classes will be derived"""
    id = db.Column(db.String(60), primary_key=True,
                   nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow,
                           nullable=False)
    update_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        """Representation of the Base object."""
        return f'<Base {self.id}>'

