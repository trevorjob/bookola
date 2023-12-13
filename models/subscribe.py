#!/usr/bin/python3
"""Subscription"""
from models import db, app, stripe
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class SubscriptionForm(FlaskForm):
    """Subscription form
    
    Args:
    email (str): The user's email address.
    plan (str): The user's subscription plan.
    submit = SubmitField('Subscribe')
    """
    email = StringField('Email')
    plan = StringField('Subscription Plan')
    submit = SubmitField('Subscribe')