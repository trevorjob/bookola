from models.engine.db_storage import DbStorage
from models.author  import Author
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
    authors = storage.all(Author)
    assert len(authors) > 0

    app.app_context().pop()  # Pop the application context after the test

def test_new_and_get():
    app = create_app()
    app.app_context().push()

    storage = DbStorage()
    author = Author(name="Test Author")
    storage.new(author)
    storage.save()

    retrieved_author = storage.get(Author, author.id)
    assert retrieved_author is not None
    assert retrieved_author.name == "Test Author"

    app.app_context().pop()

def test_delete():
    app = create_app()
    app.app_context().push()

    storage = DbStorage()
    author = Author(name="Author to delete")
    storage.new(author)
    storage.save()

    storage.delete(author)
    deleted_author = storage.get(Author, author.id)
    assert deleted_author is None

    app.app_context().pop()