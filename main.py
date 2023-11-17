from models import app, db

# from models.base_model import Base
from models.community import Communtiy
from models.message import Message

with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
