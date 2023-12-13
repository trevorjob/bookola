from models.engine.db_storage import DbStorage
from models.user import User
from models import app, db
from flask import Flask

def create_app():
    app = Flask(__name__)
    # You may need to configure your app here (e.g., database URI)
    return app

def test_all():
    app = create_app()
    app.app_context().push()  # Push an application context

    storage = DbStorage()
    # Assuming you have some test data in your database
    authors = storage.all(User)
    assert len(authors) > 0

    app.app_context().pop()  # Pop the application context after the test


def test_delete():
    app = create_app()
    app.app_context().push()

    storage = DbStorage()
    author = User(name="Author to delete")
    storage.new(author)
    storage.save()

    storage.delete(author)
    deleted_author = storage.get(User, author.id)
    assert deleted_author is None

    app.app_context().pop()