from uuid import uuid4

from models import app, db

from models.base import *
from models.author import *
from models.book import *
from models.community import *

from models.genre import *
from models.message import *

from models.reviews import *
from models.user import *

user_id = str(uuid4())
community_id = str(uuid4())
genre_id = str(uuid4())
with app.app_context():
    # db.drop_all()
    # db.create_all()
    # db.session.add(
    #     User(
    #         id=user_id,
    #         username="nandom",
    #         email="nandom@gmail.com",
    #         password_hash="blessed",
    #         first_name="nandom",
    #         last_name="john",
    #     )
    # )
    # db.session.add(Community(id=community_id, name="the nandoms", creator_id=user_id))

    # db.session.add(
    #     Message(
    #         id=str(uuid4()),
    #         text="how far how tins",
    #         user_id=user_id,
    #         community_id=community_id,
    #     )
    # )

    # db.session.add(
    #     # Message(
    #     #     id=str(uuid4()),
    #     #     text="watin de",
    #     #     user_id=user_id,
    #     #     community_id=community_id,
    #     # )
    #     # Genre(id=genre_id, name="horror")
    #     # Genre("horror")
    # )
    user = db.session.execute(
        db.select(User).where(User.id == "fca76536-86fe-46d6-9271-97022ea52aa2")
    ).scalar()
    # genre = db.session.execute(
    #     db.select(Genre).where(Genre.id == "bc457aaa-92ef-4634-8137-0c0de2b4e4ca")
    # ).scalar()
    comm = db.session.execute(
        db.select(Community).where(
            Community.id == "a40d0ec8-f698-48be-ad5c-a8c71be3bf4a"
        )
    ).scalar()
    # comm.genre.append(genre)
    comm.members.append(user)
    # print(genre.communities, comm.genre)
    # for i in genre.communities:
    #     print(i)
    # for i in comm.genre:
    #     print(i)
    for i in user.communities:
        print(i)
        print(comm.creator)
    # db.session.commit()


if __name__ == "__main__":
    app.run(debug=True)
