from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

app = Flask(__name__, template_folder='../templates/', static_folder='../static/')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sites.db"
app.config["SECRET_KEY"] = "8BYkEfBA6O6donzWlSihBXox7C0sKR6b"
db = SQLAlchemy(app)

# mail = Mail(app)
"""
app.config['MAIL_SERVER'] = 'smtp.googlemail.com' 
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_password'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
"""

if __name__ == "__main__":
    app.run(debug=True)
