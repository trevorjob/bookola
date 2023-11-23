from models.engine import db_storage
from models.author  import Author

def test_all():
    storage = DbStorage()
    # Assuming you have some test data in your database
    authors = storage.all(Author)
    assert len(authors) > 0


if __name__ == '__main__':
    test_all()