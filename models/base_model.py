#!/usr/bin/python3
from flask import Flask
from models import db
from datetime import datetime
"""Base class"""

class Base(db.Model):
    """The Base class from which future classes will be derived"""
    id = db.Column(db.string(30), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    update_at = db.Column(db.DateTime, default=datetime.utcnow)