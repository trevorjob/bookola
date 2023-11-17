from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sites.db"
db = SQLAlchemy(app)
# db.init_app(app)

# community
# message authos
