from models import app, db
from models.base import Base

with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
