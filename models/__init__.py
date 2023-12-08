from flask import Flask
from flask_sqlalchemy import SQLAlchemy
<<<<<<< HEAD
# from flask_gravatar import Gravatar
=======
>>>>>>> 66a986f9ec6e6b328f816481cc0f0a10596b5621
from flask_mail import Mail
from flask_socketio import SocketIO
from flask_login import LoginManager
import stripe
import os

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URI", "sqlite:///sites.db")
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY")
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
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
YOUR_DOMAIN = "https://bookola.onrender.com"


if __name__ == "__main__":
    app.run(debug=True)
