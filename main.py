#!/usr/bin/python3
from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import app, db
from models.author import *
from models.base import *
from models.book import *
from models.community import *
from models.genre import *
from models.message import *
from models.reviews import *
from models.user import *
from sqlalchemy import text


# with app.app_context():
#     db.drop_all()
#     db.create_all()

def get_data(data):
    return request.form.get(data)

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


@app.route("/", methods=["GET"])
def homepage():
    lastest_books = Book.query.order_by(Book.created_at.desc()).limit(4).all()
    book_of_the_week = Book.query.order_by(Book.created_at.desc()).limit(4).all()
    genres = Genre.query.all()

    return render_template(
        "homepage.html",
        lastest_books=lastest_books,
        book_of_the_week=book_of_the_week,
        genres=genres,
    )

@app.route("/login", methods=["GET", "POST"])
def login():
    """login redirection"""
    if request.method == 'POST':
        email = get_data('email')
        password = get_data('password')

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            return redirect(url_for('homepage'))
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        first_name = get_data("firstname")
        last_name = get_data("lastname")
        username = get_data("username")
        email = get_data("email")
        password = get_data("password")

        user = User.query.filter_by(email=email).first()

        if user:
            flash("All fields are required", "danger")
            return redirect(url_for("signup"))
        
        password_hash = generate_password_hash(password)

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            password_hash=password_hash,
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Account created successfully. You can log in.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/subscription", methods=["GET"])
def subscription():
    subscription_packages = [
        {"name": "Free or Regular", "price": 0.00},
        {"name": "Premium", "price": 5.99},
        {"name": "Platinum", "price": 10.00},
    ]
    return render_template(
        "subscription.html", subscription_packages=subscription_packages
    )


@app.route("/subscribe/<subscription_name>", methods=["GET"])
def subcribe(subscription_name):
    """Logic to process the selected subscription package"""
    if subscription_name == "Free or Regular":
        payment_amount = 0.00
    elif subscription_name == "Premium":
        payment_amount = 5.99
    elif subscription_name == "Platinum":
        payment_amount = 10.00
    else:
        return render_template(
            "error.html", error_message="Invalid subscription package"
        )

@app.route('/user/<id>', methods=["GET", "POST", "DELETE", "PUT"])
def user_profile(id):
    user = get_info(User, id)

    if user is None:
        return render_template('error.html', error_message='User not found'), 404

    if request.method == "GET":
        email = user.email
        first_name = user.first_name
        last_name = user.last_name
        username = user.username
        print(email, first_name, last_name, username)
        return render_template('user.html', email=email, username=username, first_name=first_name, last_name=last_name)

    elif request.method == "POST":
        user.email = get_data("email")
        user.first_name = get_data('first_name')
        user.last_name = get_data('last_name')
        user.username = get_data('username')

        db.session.commit()
        return "User information updated successfully"
    
    elif request.method == "DELETE":
        db.session.delete(user)
        db.session.commit()
        return "User deleted successfully"


    elif request.method == "PUT":
        user.email = get_data('email')
        user.first_name = get_data('first_name')
        user.last_name = get_data('last_name')
        user.username = get_data('username')

        db.session.commit()
        return "User information updated successfully"
    



@app.route('/chatroom', methods=["GET"])
def chatroom():
    communities = Community.query.all()
    return render_template('chat_room.html', communities=communities)



@app.route("/chat_select", methods=["GET"])
def select_chat(subscription_name):

    return render_template("chat_selet.html")

@app.route(
    "/create_chatroom", methods=["GET", "POST", "DELETE", "PUT"]
)
def create_chatroom():
    return render_template("create_chatroom.html")

"""
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = get_data('email')
        user = get_info( User, email)
        if user:
            password_reset_token = generate_password_reset_token(user)

            send_password_reset_email(user.email, password_reset_token)
            flash('Password recovery email sent')
            return redirect(url_for('login'))
        else:
            flash ('Email not found. Please check the email address and try again.')
    
    return render_template('forgot_password.html')
"""

@app.errorhandler(404)
@app.errorhandler(500)
def handle_errors(error):
    return render_template("error.html", error=error), error.code


if __name__ == "__main__":
    app.run(debug=True)
