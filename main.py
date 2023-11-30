#!/usr/bin/python3
from uuid import uuid4

from flask import jsonify, redirect, render_template, request, session, url_for
from flask_login import UserMixin, current_user, login_user, logout_user
from flask_socketio import join_room, leave_room, send
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from models import app, db, login_manager, socketio
from models.author import *
from models.base import *
from models.book import *
from models.community import *
from models.genre import *
from models.message import *
from models.reviews import *
from models.user import *

# with app.app_context():
#     db.drop_all()
#     db.create_all()
#     Message


def get_data(data):
    return request.form.get(data)


def get_json(data):
    return request.json.get(data)


def get_info(info, check):
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
    return User.query.get(user_id)


def get_payment_amount(subscription_name):
    """Get the payment amount based on the selected
    subscription package."""
    package_prices = {
        "Regular": 0.00,
        "Premium": 5.99,
        "Platinum": 10.00,
    }
    return package_prices.get(subscription_name, 0.00)


@app.route("/homepage", methods=["GET"])
def homepage():
    lastest_books = Book.query.order_by(Book.created_at.desc()).limit(4).all()
    book_of_the_week = Book.query.order_by(Book.created_at.desc()).limit(4).all()
    genres = Genre.query.all()

    return render_template(
        "homepage.html",
        lastest_books=lastest_books,
        book_of_the_week=book_of_the_week,
        genres=genres,
        current_user=current_user,
    )


@app.route("/", methods=["GET", "POST"])
def login():
    """login redirection"""
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


@app.route("/user", methods=["GET", "POST", "DELETE", "PUT"])
def user():
    return render_template("user.html")


@app.route("/user/<id>", methods=["GET", "POST", "DELETE", "PUT"])
def user_profile():
    if request.method == "GET":
        email = user.email
        first_name = user.first_name
        last_name = user.last_name
        username = user.username
        user_data = get_data(User)
        return render_template("user.html", user=user_data)

    elif request.method == "POST":
        user_id = get_data(id)
        if user_id:
            user = get_info(User, id)
            if user:
                user.email = (get_data("email"),)
                user.first_name = (get_data("first_name"),)
                user.last_name = (get_data("last_name"),)
                user.username = get_data("username")
                db.session.commit()
                return "User infor updated successfully"
            else:
                return (
                    render_template("error.html", error_message="User not found"),
                    404,
                )
        else:
            new_user = User(
                email=get_data("email"),
                first_name=get_data("first_name"),
                last_name=get_data("last_name"),
                username=get_data("username"),
            )
            db.session.add()
            db.session.commit()
            return "User created successfully"

    elif request.method == "DELETE":
        if get_data("id"):
            user = get_info(User, get_data("id"))
            if user:
                db.session.delete(user)
                db.session.commit()
                return "User deleted successfully"
            else:
                return (
                    render_template("error.html", error_message="User not found"),
                    404,
                )
        else:
            return (
                render_template("error.html", error_message="User ID not provided"),
                400,
            )

    elif request.method == "PUT":
        if get_data("id"):
            user = get_info(User, get_data("id"))
            if user:
                user.email = get_data("email")
                user.first_name = get_data("first_name")
                user.last_name = get_data("last_name")
                user.username = get_data("username")
                db.session.commit()
                return "User information updated successfully"
            else:
                return (
                    render_template("error.html", error_message="User not found"),
                    404,
                )
        else:
            return (
                render_template("error.html", error_message="User ID not provided"),
                400,
            )

    return render_template("user.html", current_user=current_user)


@app.route("/books", methods=["GET"])
def books():
    return render_template("books.html", current_user=current_user)


@app.route("/subscription", methods=["GET", "POST"])
def subscription():
    """Subscription packages"""
    packages = [
        {"name": "Regular", "price": 0.00},
        {"name": "Premium", "price": 5.99},
        {"name": "Platinum", "price": 10.00},
    ]
    return render_template(
        "subscription.html", packages=packages, current_user=current_user
    )


@app.route("/subscribe/<subscription_name>", methods=["GET"])
def subcribe(subscription_name):
    """Logic to process the selected subscription package"""
    payment_amout = get_payment_amount(subscription_name)

    return redirect("/")


@app.route("/chatroom/<community_id>", methods=["GET"])
def chatroom(community_id):
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
    chat = session.get("chat")
    join_room(chat)
    community = getOneFromDB(Community, chat)
    community.active += 1
    saveDB()


@socketio.on("disconnect")
def disconnect():
    chat = session.get("chat")
    leave_room(chat)

    community = getOneFromDB(Community, chat)
    community.active -= 1
    saveDB()


@socketio.on("message")
def message(data):
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
    if not model.communities:
        return False
    for mod in model.communities:
        if mod.id == id:
            return True
    return False


@app.route("/chat_select", methods=["GET"])
def select_chat():
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
    print(request.method)
    if request.method == "POST":
        name = get_data("name")
        community = Community(id=str(uuid4()), name=name, creator_id=current_user.id)
        addToDB(community)
        current_user.communities.append(community)
        saveDB()
        return redirect(url_for("select_chat"))
    return render_template("create_chatroom.html")


@app.route("/search_results", methods=["GET"])
def search_results():
    return render_template("search-result.html")


@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
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


@app.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
        print("Logged out successful")

    return redirect(url_for("login"))


# @app.errorhandler(404)
# @app.errorhandler(500)
# def handle_errors(error):
#     return render_template("error.html")


if __name__ == "__main__":
    app.run(debug=True)
