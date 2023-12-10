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
    # db.drop_all()
    # db.create_all()
    # with open("genres.json", "r", encoding="utf-8") as f:
    #     genres = json.load(f)
    #     for genre in genres:
    #         gen = Genre(
    #             id=genre["id"],
    #             name=genre["name"],
    #             description=genre["description"],
    #             img_url=genre["img_url"],
    #         )
    #         db.session.add(gen)

    # with open("books.json", "r", encoding="utf-8") as f:
    #     books = json.load(f)
    #     for book in books:
    #         for genre in genres:
    #             if book["genre_id"] == genre["name"]:
    #                 boo = Book(
    #                     id=book["id"],
    #                     title=book["title"],
    #                     genre_id=genre["id"],
    #                     cover_image_url=book["cover_image_url"],
    #                     description=book["description"],
    #                     publication_date=book["publication_date"],
    #                     language=book["language"],
    #                     author=book["author"],
    #                     rating=randint(5, 10),
    #                 )
    #                 db.session.add(boo)
    # db.session.commit()
    book_of = choice(Book.query.all())
    latest = sample(Book.query.all(), k=4)
    gens = sample(Genre.query.all(), k=4)

    cur_id = {}


# HELPER FUNCTIONS
########################### HELPER FUNCTIONS ##########################################
def get_data(data):
    """A method that get data from the database"""
    return request.form.get(data)


def get_json(data):
    """A method that get data from the database in form of json"""
    return request.json.get(data)


def get_info(info, check):
    """Retrive infomation/data of a class"""
    return db.session.execute(db.select(info).where(info.id == check)).scalar()


def getFormData(name):
    """get the form data for a given name from the site"""
    return request.form.get(name)


def getOneFromDB(model, id):
    """get one model from the database"""
    return db.session.execute(db.select(model).where(model.id == id)).scalar()


def getAllFromDB(model):
    """get all models from the database"""
    return db.session.execute(db.select(model)).scalars().all()


def saveDB():
    """save to the database"""
    db.session.commit()


def addToDB(model):
    """add a model to the database"""
    db.session.add(model)


def updateDB(model, update, value):
    """update a model in the database"""
    model[update] = value


@login_manager.user_loader
def load_user(user_id):
    """A method for login through get users id"""
    return User.query.get(user_id)


################### FUNCTION DECORATORS #######################
def is_subed(function):
    @wraps(function)
    def wrapped(*args, **kwargs):
        if current_user.subscribed:
            return function(*args, **kwargs)
        else:
            return redirect(url_for("subscription"))

    return wrapped


def is_logged(function):
    @wraps(function)
    def wrapped(*args, **kwargs):
        if current_user.is_authenticated:
            return function(*args, **kwargs)
        else:
            return redirect(url_for("login"))

    return wrapped


########################## HOME PAGE ROUTE #########################
@app.route("/", methods=["GET"])
def homepage():
    lastest_books = latest
    book_of_the_week = book_of
    genres = gens
    session.setdefault("ses", [])
    subed = bool(request.args.get("subed"))
    if subed:
        current_user.subscribed = True
        saveDB()

    return render_template(
        "homepage.html",
        lastest_books=lastest_books,
        book_of_the_week=book_of_the_week,
        genres=genres,
        current_user=current_user,
    )


########################## SEARCH RESULT PAGE ROUTE #########################


@app.route("/search_results", methods=["POST"])
def search_results():
    search_term = request.form.get("q")
    results = Book.query.filter(Book.title.ilike(f"%{search_term}%")).all()
    return render_template("search-result.html", results=results, q=search_term)


########################## LOGIN PAGE ROUTE #########################


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login route"""
    if request.method == "POST":
        email = get_data("email")
        password = get_data("password")

        remember_me = get_data("rememberme")

        if email is not None and password is not None:
            user = User.query.filter_by(email=email).first()

            if user and check_password_hash(user.password_hash, password):
                cur_id["user_id"] = user.id
                session["user_id"] = user.id
                login_user(user, remember=remember_me)
                return redirect(url_for("homepage"))
        return redirect(url_for("login"))

    if current_user.is_authenticated:
        return redirect(url_for("homepage"))

    return render_template("login.html")


########################## LOG OUT ROUTE #########################


@app.route("/logout")
@is_logged
def logout():
    """Logout users"""
    if current_user.is_authenticated:
        sess = session.get("profile", None)
        if sess:
            session["profile"] = None

        logout_user()
        flash("Logged out successful", "success")

    return redirect(url_for("login"))


########################## SIGN UP PAGE ROUTE #########################


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Signup route"""
    if request.method == "POST":
        first_name = get_data("firstname")
        last_name = get_data("lastname")
        username = get_data("username")
        email = get_data("email")
        password = get_data("password")
        email_bytes = email.lower().encode("utf-8")
        email_hash = hashlib.md5(email_bytes).hexdigest()
        gravatar_url = f"https://www.gravatar.com/avatar/{email_hash}?s=200&d=retro&r=g"
        # password_token = get_data("password_token")

        user = User.query.filter_by(email=email).first()

        if user:
            print("All fields are required", "danger")
            return redirect(url_for("signup"))

        password_hash = generate_password_hash(password)

        new_user = User(
            id=str(uuid4()),
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            password_hash=password_hash,
            profile_pic_url=gravatar_url,
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Account created successfully. You can log in.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")


########################## USER PROFILE PAGE ROUTE #########################
def generate_profile(curs):
    from openai import OpenAI

    if len(curs) >= 3:
        prompt = f"Generate a very short personality profile and special charachter for me. my name is {current_user.username} who has read the following books: {', '.join(curs)}. return as html element in html div with my fictional persona as the heading in a h2 tag e.g(<h2>Sam, Mythic Wanderer</h2> or <h2>The Adventurous Mavin</h2>) also refer to me as you and your"
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a creative assistant, skilled in explaining complex book related concepts with creative flair. you are very direct and always goes straight to the point",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        session["profile"] = completion.choices[0].message.content


def get_head(html_string):
    from bs4 import BeautifulSoup

    if not html_string:
        return
    # Create a BeautifulSoup object
    soup = BeautifulSoup(html_string, "html.parser")

    # Get the first h2 tag
    first_h2_tag = soup.find("h2")

    # Initialize variables to store the extracted h2 tag and modified HTML
    extracted_h2_tag = None
    modified_html = None

    # Check if the first h2 tag exists
    if first_h2_tag:
        # Store the first h2 tag
        extracted_h2_tag = str(first_h2_tag)

        # Remove the first h2 tag from the HTML
        first_h2_tag.extract()

        # Store the modified HTML
        modified_html = str(soup)

    return modified_html, extracted_h2_tag


@app.route("/user", methods=["GET", "POST"])
@is_logged
def user_profile():
    cur_ses = []
    for sess in session["ses"]:
        cur_ses.append(getOneFromDB(Book, sess))

    if len(cur_ses) <= 6:
        curs = cur_ses
    else:
        curs = cur_ses[-6:]
    profile_data = session.get("profile", None)
    if not profile_data:
        generate_profile([co.title for co in curs])
        profile_data = session.get("profile", None)
    if profile_data:
        rest_bod, h2_head = get_head(profile_data)
    else:
        h2_head = "<h2>You Are Still A Mystery</h2>"
        rest_bod = (
            "<p>Explore Our Massive Collection Of Books And Show Us Who You Are And What You're Made Of. </p>"
            "<p>Happy Reading.</p>"
        )

    return render_template(
        "user.html",
        current_user=current_user,
        recents=reversed(curs),
        profile_data=rest_bod,
        header=h2_head,
    )


########################## BOOK GENRES PAGE ROUTE #########################


@app.route("/books/<genre_id>", methods=["GET"])
@is_logged
def books(genre_id):
    genre = getOneFromDB(Genre, genre_id)
    return render_template(
        "books.html", current_user=current_user, books=genre.books, genre=genre.name
    )


############################# ALL GENRES PAGE #################
@app.route("/genres")
@is_logged
def genres():
    genres = getAllFromDB(Genre)
    return render_template("genres.html", genres=genres)


########################## BOOK DETAILS PAGE ROUTE #########################
@app.route("/book/<bk_id>", methods=["GET", "POST"])
@is_logged
@is_subed
def book_detail(bk_id):
    if request.method == "POST":
        comment = get_data("comment")
        review = Review(
            review_text=comment,
            id=str(uuid4()),
            book_id=bk_id,
            user_id=current_user.id,
        )

        db.session.add(review)
        db.session.commit()

    book = getOneFromDB(Book, bk_id)
    similar_books = sample(Book.query.filter_by(genre_id=book.genre_id).all(), k=6)
    same_author = Book.query.filter_by(author=book.author).all()
    recents = list(book.reviews)
    reviews = []
    if recents:
        if len(recents) <= 5:
            reviews = recents
        else:
            reviews = recents[-5:]

    return render_template(
        "book_detail.html",
        current_user=current_user,
        book=book,
        similar_books=similar_books,
        same_author=same_author,
        reviews=reversed(reviews),
    )


@app.route("/rand/<bk_id>")
def rand(bk_id):
    if bk_id not in session["ses"]:
        new_ses = session["ses"]
        new_ses.append(bk_id)
        session["ses"] = new_ses
    return render_template("rand.html")


########################## SUBSCRIPTION PAGE ROUTE #########################
@app.route("/subscription", methods=["GET", "POST"])
@is_logged
def subscription():
    """Subscription packages"""
    packages = [
        {"name": "Free", "price": 0.00},
        {"name": "Premium", "price": 5.99},
        {"name": "Platinum", "price": 10.00},
    ]
    return render_template(
        "subscription.html", packages=packages, current_user=current_user
    )


@app.route("/checkout", methods=["GET", "POST"])
@is_logged
def checkout_subs():
    """A method route for subscription packages"""
    logout_user()
    if request.method == "POST":
        subscription_level = request.form.get("subs")

        if subscription_level == "free":
            checkout_session = stripe.checkout.Session.create(
                line_items=[{"price": "price_1OIK6TLr3itnznEmmFb6Rboj", "quantity": 1}],
                mode="payment",
                success_url=YOUR_DOMAIN + "/success",
                cancel_url=YOUR_DOMAIN + "/fail",
            )
            return redirect(checkout_session.url, code=303)
        elif subscription_level == "premium":
            checkout_session = stripe.checkout.Session.create(
                line_items=[{"price": "price_1OHpulLr3itnznEm553iHv2g", "quantity": 3}],
                mode="subscription",
                success_url=YOUR_DOMAIN + "/success",
                cancel_url=YOUR_DOMAIN + "/fail",
            )
            return redirect(checkout_session.url, code=303)
        elif subscription_level == "platinum":
            checkout_session = stripe.checkout.Session.create(
                line_items=[{"price": "price_1OHpydLr3itnznEm1hxM1If1", "quantity": 5}],
                mode="subscription",
                success_url=YOUR_DOMAIN + "/Success",
                cancel_url=YOUR_DOMAIN + "/fail",
            )

            return redirect(checkout_session.url, code=303)
    return "Invalid subcription"


@app.route("/success")
def success():
    """Success page route"""
    user = getOneFromDB(User, cur_id["user_id"])
    login_user(user)
    return render_template("success.html")


@app.route("/fail")
def fail():
    """Failure to load page route"""
    user = getOneFromDB(User, cur_id["user_id"])
    login_user(user)
    return render_template("fail.html")


########################## CHATROOM ROUTES #########################
@app.route("/chatroom/<community_id>", methods=["GET"])
@is_logged
@is_subed
def chatroom(community_id):
    """Community route"""
    session["chat"] = community_id
    check = False
    community = getOneFromDB(Community, community_id)
    if current_user.communities:
        for c_com in current_user.communities:
            if c_com.id == community.id:
                check = True
    if not check:
        current_user.communities.append(community)
        saveDB()

    if community:
        print(community.messages)
        return render_template(
            "chat_room.html",
            community=community,
            messages=community.messages,
            current_user=current_user,
        )


@socketio.on("connect")
def connect(auth):
    """Aunthenticate and connect users to the chatroom"""
    chat = session.get("chat")
    join_room(chat)
    community = getOneFromDB(Community, chat)
    community.active += 1
    saveDB()


@socketio.on("disconnect")
def disconnect():
    """Disconnect users for the chat room"""
    chat = session.get("chat")
    leave_room(chat)

    community = getOneFromDB(Community, chat)
    community.active -= 1
    saveDB()


@socketio.on("message")
def message(data):
    """Users messages/chats"""
    chat = session.get("chat")
    if not chat:
        return
    user = getOneFromDB(User, session.get("user_id"))
    content = {
        "name": user.username,
        "message": data["data"],
        "img": user.profile_pic_url,
    }
    message = ChatMessage(
        id=str(uuid4()),
        text=content["message"],
        user_id=user.id,
        community_id=chat,
        created_at=datetime.utcnow(),
    )
    content["time"] = message.created_at.strftime("%H:%M")
    send(content, to=chat)

    addToDB(message)
    saveDB()


def check_id(model, id):
    """Confirmation and authentication"""
    if not model.communities:
        return False
    for mod in model.communities:
        if mod.id == id:
            return True
    return False


@app.route("/chat_select", methods=["GET"])
@is_logged
@is_subed
def select_chat():
    """Users select chat"""
    communities = getAllFromDB(Community)
    user = current_user
    check = False
    user_comms = []
    other_comms = []

    for community in communities:
        check = check_id(user, community.id)
        if check:
            user_comms.append(community)
        else:
            other_comms.append(community)
    return render_template(
        "chat_select.html",
        user_communities=user_comms,
        other_communities=other_comms,
        current_user=current_user,
    )


@app.route("/create_chatroom", methods=["GET", "POST", "DELETE", "PUT"])
@is_logged
def create_chatroom():
    """Users create chatroom"""
    all_genres = getAllFromDB(Genre)
    if request.method == "POST":
        name = get_data("name")
        community = Community(id=str(uuid4()), name=name, creator_id=current_user.id)
        addToDB(community)
        current_user.communities.append(community)
        saveDB()
        return redirect(url_for("select_chat"))
    return render_template("create_chatroom.html", genres=all_genres)


########################## PASSWORD MANAGER ROUTE #########################


@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    """Forgot password route"""
    form = ResetRequestForm()

    if request.method == "POST":
        email = request.form.get("email")
        user = User.query.filter_by(email=email).first()
        print(user.email)

        if user:
            # Generate a password reset token and save it to the user
            password_reset_token = secrets.token_urlsafe(32)
            user.password_reset_token = password_reset_token
            db.session.commit()

            # Build the reset link using url_for
            # reset_link = url_for('reset_password', token=password_reset_token, _external=True, _scheme='http')

            # Send password reset email with the reset link
            send_password_reset_email(user.email, password_reset_token)
            flash("Password recovery email sent")
            return redirect(url_for("nandom"))
        else:
            flash("Email not found. Please check the email address and try again.")

    return render_template("forgot_password.html", current_user=current_user, form=form)


@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    """Reset password and authentication"""
    user = User.query.filter_by(password_reset_token=token).first()
    if not user:
        flash("Invalid or expired password reset token")
        return redirect(url_for("login"))

    form = ResetPasswordForm()
    if request.method == "POST":
        new_password = form.new_password.data

        # Update the user's password and reset the password reset token
        user.password_hash = generate_password_hash(new_password)
        user.password_reset_token = None
        db.session.commit()

        flash(
            "Password reset successfully. You can now log in with your new password.",
            "success",
        )
        return redirect(url_for("login"))

    return render_template("reset_password.html", form=form, token=token)


@app.route("/nandom", methods=["GET", "POST"])
def nandom():
    """Email success notification request route"""
    return render_template("nandom.html")


@app.route("/terms_of_service", methods=["GET", "POST"])
def terms_of_service():
    return render_template("terms_of_service.html")


@app.errorhandler(404)
@app.errorhandler(500)
def handle_errors(error):
    # 404 & 500 error handler
    return render_template("error.html")


if __name__ == "__main__":
    app.run(debug=True)
