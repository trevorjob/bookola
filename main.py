from models import app, db
from models.base import *
from models.author import *
from models.books import *
from models.community import *
from models.reviews import *
from models.users import *
from models.message import *
from models.genre import *

with app.app_context():
    db.drop_all()
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
