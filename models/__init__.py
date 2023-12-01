from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_socketio import SocketIO
from flask_login import LoginManager
import stripe
import os

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sites.db"
app.config["SECRET_KEY"] = "8BYkEfBA6O6donzWlSihBXox7C0sKR6b"
app.config["MAIL_SERVER"] = "smtp.googlemail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = "redeks123456@gmail.com"
app.config["MAIL_PASSWORD"] = "blessedacademy12"
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
mail = Mail(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
socketio = SocketIO(app)
stripe.api_key = os.environ["STRIPE_SECRET_KEY"]
YOUR_DOMAIN = "http://localhost:5000"


if __name__ == "__main__":
    app.run(debug=True)
