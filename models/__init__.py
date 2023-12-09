from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_socketio import SocketIO
from flask_login import LoginManager
import stripe
import os

app = Flask(__name__, template_folder="../templates", static_folder="../static")

# Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URI", "sqlite:///sites.db")

# Secret Key
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY")

# Mail Configuration
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = "doe70097@gmail.com"
app.config["MAIL_PASSWORD"] = "awhw jjwx ktbr lyls"
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
# Enable mail debugging for development
app.config["MAIL_DEBUG"] = True
app.config["MAIL_DEFAULT_SENDER"] = "adeolaesther761@gmail.com"

mail = Mail(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
socketio = SocketIO(app)
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
YOUR_DOMAIN = "https://bookola.onrender.com"
# YOUR_DOMAIN = "http://127.0.0.1:5000"


if __name__ == "__main__":
    app.run(debug=True)
