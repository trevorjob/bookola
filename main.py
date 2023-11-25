#!/usr/bin/python3
from flask import render_template, request

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
def home():
    if request.method == "POST":
        email = request.form.get("email")
        print(f"thsi is the login email {email}")

    return render_template("login.html")



if __name__ == "__main__":
    app.run(debug=True)
