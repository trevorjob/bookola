#!/usr/bin/python3
from flask import render_template, request, redirect, url_for, flash
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

# with app.app_context():
#     db.drop_all()
#     db.create_all()

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            flash("Login successful!")
            return redirect(url_for("homepage"))
        else:
            flash("Invalid email or password. Please try again." "Danger! Danger!")
    return render_template("login.html")

@app.route('/homepage', methods=["GET"])
def homepage():
    lastest_books = Book.query.order_by(Book.created_at.desc()).limit(4).all()
    book_of_the_week = Book.query.order_by(Book.created_at.desc()).limit(4).all()
    genres = Genre.query.all()
    return render_template("homepage.html", lastest_books=lastest_books, book_of_the_week=book_of_the_week, genres=genres)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("lastname")
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        password_hash = generate_password_hash(password)

        new_user = User(first_name=first_name, last_name=last_name, email=email, username=username, password_hash=password_hash)
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
        {"name": "Platinum", "price": 10.00}
    ]
    return render_template('subscription.html', subscription_packages=subscription_packages)

@app.route('/subscribe/<subscription_name>', methods=["GET"])
def subcribe(subscription_name):
    """Logic to process the selected subscription package"""
    if subscription_name == "Free or Regular":
        payment_amount = 0.00
    elif subscription_name == "Premium":
        payment_amount = 5.99
    elif subscription_name == "Platinum":
        payment_amount = 10.00
    else:
        return render_template('error.html', error_message='Invalid subscription package')
        
    return render_template('subscription_confirmation.html', subscription_name=subscription_name, payment_amount=payment_amount) 

@app.route('/user', methods=["GET", "POST", "DELETE", "PUT"])
def user(user):
    return render_template('user.html')

@app.route('/homepage/chatroom', methods=["GET"])
def chatroom():
    return render_template('chat_room.html')

@app.route('/homepage/chatroom/create_chatroom', methods=["GET", "POST", "DELETE", "PUT"])
def create_chatroom():
    return render_template("create_chatroom.html")

@app.route("/homepage/chatroom/chat_select", methods=["GET"])
def select_chat():
    # Handle select chat logic here
    return render_template("chat_select.html")

@app.errorhandler(404)
@app.errorhandler(500)
def handle_errors(error):
    return render_template('error.html', error=error), error.code

if __name__ == "__main__":
    app.run(debug=True)
