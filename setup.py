#!/usr/bin/python3
"""This is the main entry point of the web application.
It contains the initialisation of a web application, including setting
up route, defining views and configuring various settings."""
import hashlib
import json
import os
import secrets
from functools import wraps
from random import choice, randint, sample
from uuid import uuid4

import stripe
from flask import flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_user, logout_user
from flask_mail import Message
from flask_socketio import join_room, leave_room, send
from werkzeug.security import check_password_hash, generate_password_hash

from models import YOUR_DOMAIN, app, db, login_manager, mail, socketio, stripe
from models.base import *
from models.book import *
from models.community import *
from models.forms import ResetPasswordForm, ResetRequestForm
from models.genre import *
from models.message import *
from models.reviews import *
from models.subscribe import *
from models.user import *

with app.app_context():
    db.drop_all()
    db.create_all()
    with open("genres.json", "r", encoding="utf-8") as f:
        genres = json.load(f)
        for genre in genres:
            gen = Genre(
                id=genre["id"],
                name=genre["name"],
                description=genre["description"],
                img_url=genre["img_url"],
            )
            db.session.add(gen)

    with open("books.json", "r", encoding="utf-8") as f:
        books = json.load(f)
        for book in books:
            for genre in genres:
                if book["genre_id"] == genre["name"]:
                    boo = Book(
                        id=book["id"],
                        title=book["title"],
                        genre_id=genre["id"],
                        cover_image_url=book["cover_image_url"],
                        description=book["description"],
                        publication_date=book["publication_date"],
                        language=book["language"],
                        author=book["author"],
                        rating=randint(5, 10),
                    )
                    db.session.add(boo)
    db.session.commit()
