#!/usr/bin/python3
"""This is the main entry point of the web application.
It contains the initialisation of a web application, including setting
up route, defining views and configuring various settings."""
import json
from random import choice, choices, randint
from uuid import uuid4
from flask import jsonify, redirect, render_template, request, session, url_for
from flask_login import UserMixin, current_user, login_user, logout_user
from flask_socketio import join_room, leave_room, send
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from models import app, db, login_manager, stripe, YOUR_DOMAIN
import stripe
from werkzeug.security import check_password_hash, generate_password_hash
from models import app, db, login_manager, socketio
from models.base import *
from models.book import *
from models.community import *
from models.genre import *
from models.message import *
from models.reviews import *
from models.user import *
from models.subscribe import *
from sqlalchemy import text


with app.app_context():
#     db.drop_all()
#     db.create_all()
#     with open("genres.json", "r", encoding="utf-8") as f:
#         genres = json.load(f)
#         for genre in genres:
#             gen = Genre(id=genre["id"], name=genre["name"])
#             db.session.add(gen)

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
    book_of = choice(Book.query.all())
    latest = choices(Book.query.all(), k=4)
    gens = choices(Genre.query.all(), k=4)
    # db.session.commit()


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


sand = {}


@login_manager.user_loader
def load_user(user_id):
    """A method for login through get users id"""
    return User.query.get(user_id)


@app.route("/homepage", methods=["GET"])
def homepage():
    lastest_books = latest
    book_of_the_week = book_of
    genres = gens

    return render_template(
        "homepage.html",
        lastest_books=lastest_books,
        book_of_the_week=book_of_the_week,
        genres=genres,
        current_user=current_user,
    )


@app.route("/", methods=["GET", "POST"])
def login():
    """Login route"""
    if request.method == "POST":
        email = get_data("email")
        password = get_data("password")

        if email is not None and password is not None:
            user = User.query.filter_by(email=email).first()

            if user and check_password_hash(user.password_hash, password):
                print(user)
                print("this is the user")

                sand["user_id"] = user.id
                session["user_id"] = user.id

                login_user(user)
                return redirect(url_for("homepage"))
        return redirect(url_for("login"))

    if current_user.is_authenticated:
        return redirect(url_for("homepage"))

    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Signup route"""
    if request.method == "POST":
        first_name = get_data("firstname")
        last_name = get_data("lastname")
        username = get_data("username")
        email = get_data("email")
        password = get_data("password")
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
        )
        db.session.add(new_user)
        db.session.commit()
        print("Account created successfully. You can log in.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")



# @app.route("/user", methods=["GET", "POST", "DELETE", "PUT"])
# def user():
#     return render_template("user.html")


@app.route("/user", methods=["GET", "POST", "DELETE", "PUT"])
def user_profile():
    # if request.method == "GET":
    #     return render_template("user.html", current_user=current_user)

    if request.method == "POST":
        current_user.email = get_data("email")
        current_user.username = get_data("username")
        print(get_data("email"))
        print(get_data("username"))
        db.session.commit()

    return render_template("user.html", current_user=current_user)

@app.route("/books/<genre_id>", methods=["GET"])
def books(genre_id):
    genre = getOneFromDB(Genre, genre_id)
    return render_template(
        "books.html", current_user=current_user, books=genre.books, genre=genre.name
    )

@app.route("/subscription", methods=["GET", "POST"])
def subscription():
    """Subscription packages"""
    packages = [
        {"name": "Regular", "price": 0.00},
        {"name": "Premum", "price": 5.99},
        {"name": "Platinum", "price": 10.00},
    ]
    return render_template(
        "subscription.html", packages=packages, current_user=current_user
    )

@app.route("/checkout", methods=["GET", "POST"])
def checkout_subs():
    """A method route for subscription packages"""
    if request.method == "POST":
        subscription_level = request.form.get("subs")
        
        if subscription_level == 'free':
            checkout_session = stripe.checkout.Session.create(
                line_items= [
                    {
                        'price': "price_1OIK6TLr3itnznEmmFb6Rboj",
                        'quantity':1
                    }
                ],
                mode="payment",
                success_url=YOUR_DOMAIN + "/success",
                cancel_url=YOUR_DOMAIN + "/fail"
            )
            return redirect(checkout_session.url, code=303)
        elif subscription_level == 'premium':
            checkout_session = stripe.checkout.Session.create(
                line_items= [
                    {
                        'price': "price_1OHpulLr3itnznEm553iHv2g",
                        'quantity': 3
                    }
                ],
                mode="subscription",
                success_url=YOUR_DOMAIN + "/success",
                cancel_url=YOUR_DOMAIN + "/fail"
                )
            return redirect(checkout_session.url, code=303)
        elif subscription_level == 'platinum':
            checkout_session = stripe.checkout.Session.create(
                line_items= [
                    {
                        'price': "price_1OHpydLr3itnznEm1hxM1If1",
                        'quantity': 5
                    }
                ],
                mode="subscription",
                success_url=YOUR_DOMAIN + "/Success",
                cancel_url=YOUR_DOMAIN + "/fail"
            )
            return redirect(checkout_session.url, code=303)
    return "Invalid subcription"


@app.route("/chatroom/<community_id>", methods=["GET"])
def chatroom(community_id):
    """Community route"""
    session["chat"] = community_id
    check = False
    community = getOneFromDB(Community, community_id)
    if current_user.communities:
        print("looping for community")
        for c_com in current_user.communities:
            print(c_com)
            if c_com.id == community.id:
                check = True
    if not check:
        current_user.communities.append(community)
        saveDB()

    print(current_user.communities)

    if community:
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
    content = {"name": user.username, "message": data["data"]}
    message = ChatMessage(
        id=str(uuid4()), text=content["message"], user_id=user.id, community_id=chat
    )
    send(content, to=chat)

    addToDB(message)
    saveDB()
    print(f"{session.get('name')} said: {data['data']}")


def check_id(model, id):
    """Confirmation and authentication"""
    if not model.communities:
        return False
    for mod in model.communities:
        if mod.id == id:
            return True
    return False


@app.route("/chat_select", methods=["GET"])
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
def create_chatroom():
    """Users create chatroom"""
    print(request.method)
    if request.method == "POST":
        name = get_data("name")
        community = Community(id=str(uuid4()), name=name, creator_id=current_user.id)
        addToDB(community)
        current_user.communities.append(community)
        saveDB()
        return redirect(url_for("select_chat"))
    return render_template("create_chatroom.html")


@app.route("/search_results", methods=["POST"])
def search_results():

    search_term = request.form.get("q")
    results = Book.query.filter(Book.title.ilike(f"%{search_term}%")).all()
    return render_template("search-result.html", results=results, q=search_term)


@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    """Forgot password route"""
    if request.method == "POST":
        email = request.form.get("email")
        user = User.query.filter_by(email=email).first()

        if user:
            # Generate a password reset token and save it to the user
            password_reset_token = generate_password_hash(email, method="sha256")
            user.password_reset_token = password_reset_token
            db.session.commit()

            # Send password reset email
            send_password_reset_email(user.email, password_reset_token)
            print("Password recovery email sent")
            return redirect(url_for("login"))
        else:
            print("Email not found. Please check the email address and try again.")

    return render_template("forgot_password.html")


@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    """Reset password and authentication"""
    user = User.query.filter_by(password_reset_token=token).first()

    if not user:
        print("Invalid or expired password reset token")
        return redirect(url_for("login"))

    if request.method == "POST":
        new_password = request.form.get("new_password")

        # Update the user's password and reset the password reset token
        user.password_hash = generate_password_hash(new_password)
        user.password_reset_token = None
        db.session.commit()

        print(
            "Password reset successfully. You can now log in with your new password.",
            "success",
        )
        return redirect(url_for("login"))

    return render_template("reset_password.html", token=token)

@app.route('/terms_of_service', methods=["GET", "POST"])
def terms_of_service():
    return render_template("terms_of_service.html")

@app.route("/logout")
def logout():
    """Logout users"""
    if current_user.is_authenticated:
        logout_user()
        print("Logged out successful")

    return redirect(url_for("login"))


@app.route("/success")
def success():
    """Success page route"""
    return render_template("success.html")

@app.route("/fail")
def fail():
    """Failure to load page route"""
    return render_template("fail.html")


"""
@app.errorhandler(404)
@app.errorhandler(500)
def handle_errors(error):
    #404 & 500 error handler
    return render_template("error.html")
"""

if __name__ == "__main__":
    app.run(debug=True)
