from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder="../web_flask/templates", static_url_path="/web_flask/static/styles/")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sites.db"
app.config["SECRET_KEY"] = "8BYkEfBA6O6donzWlSihBXox7C0sKR6b"
db = SQLAlchemy(app)
# db.init_app(app)


if __name__ == "__main__":
    app.run(debug=True)
