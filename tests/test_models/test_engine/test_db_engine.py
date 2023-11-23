#!/usr/bin/python3
"""DBStorage test unittest"""
import unittest
from models import app, db
from models.engine.db_storage import DbStorage
from models.books import Book
from models.users import User
from models.community import Community
import models


class TestDBStorage(unittest.TestCase):
    """Db setup"""
    def setUp(cls):
        """Setup db storage"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        cls.app = app.test_client()
        db.create_all()

    def tearDown(cls):
        """Test to remove/drop object"""
        db.session.remove()
        db.drop_all()

    def test_all(cls):
        """Test the 'all' method"""
        storage = DbStorage()
        user = models.users.User(username="Joe Doe")
        book = models.books.Book(Id='1234ui5')
        db.session.add_all([user, book])
        db.session.commit()

        # Test 'all' without specifying a class
        all_objs = storage.all()
        cls.assertEqual(len(all_objs), 2)

        # Test 'all' with specifying a class
        users = storage.all(models.users.User)
        cls.assertEqual(len(users), 1)

    def test_new(cls):
        """Test the 'new' method"""
        storage = DbStorage()

        user = models.users(username='Jon Doe')

        # Test 'new'
        storage.new(user)
        db_objs = models.users.User.query.all()
        cls.assertEqual(len(db_objs), 1)
        cls.assertEqual(db_objs[0], user)

    def test_relaod(cls):
        """Test the 'reload' method"""
        storage = DbStorage()

        user = models.users.User(username='Jon Doe')

        # Test 'new' 'save' and 'relaod'
        storage.new(user)
        storage.save(user)
        storage.reload()

        db_objs = models.users.User.query.all()
        cls.assertEqaul(len(db_objs), 0)

    def test_delete(cls):
        """Test the 'delete' method"""
        storage = DbStorage()

        user = models.users.User(username="Jon Doe")

        # Test 'new', 'delete', and 'save'
        storage.new(user)
        storage.delete(user)
        storage.save()

        db_objs = models.users.User.query.all()
        cls.assertEqual(len(db_objs), 0)

    def test_close(cls):
        """Test the 'close' method"""
        storage = DbStorage()

        # Test 'close'
        storage.close()

    def test_get(cls):
        """Test the 'get' method"""
        storage = DbStorage()

        user = models.users.User(username="Jon Doe")
        db.session.add(user)
        db.session.commit()

        # Test 'get'
        get_user = storage.get(models.users.User, user.id)
        cls.assertEqual(get_user, user)

    def test_count(cls):
        """Test the 'count' method"""
        storage = DbStorage()

        # Create some test data
        user1 = models.users.User(username="Jon Doe")
        user2 = models.users.User(username="Amy Joe")
        book = models.books.Book(id="24749501fdgr")
        db.session.add([user1, user2, book])
        db.session.commit()

        # Test 'count' without specifying a class
        sum_count = storage.count()
        cls.assertEqual(sum_count, 3)

        # Test 'count' with specifying a class
        total = storage.count(models.user.User)
        cls.assertEqual(total, 2)


if __name__ == "__main__":
    unittest.main()
