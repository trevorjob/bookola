#!/usr/bin/python3
"""Subscription"""
from models import db, app, stripe
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class SubscriptionForm(FlaskForm):
    email = StringField('Email')
    plan = StringField('Subscription Plan')
    submit = SubmitField('Subscribe')