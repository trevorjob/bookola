import json
from pprint import pprint
from models.genre import Genre
from uuid import uuid4

import requests

from bookdata import BOOKS_M

# CSV file path
file_path = "genres.json"

unique = []
for item in BOOKS_M:
    if item["genre"] not in unique:
        print(item["genre"])
        unique.append(item["genre"])

json_gern = {}
top = []
for uniq in unique:
    genre = Genre(id=str(uuid4()), name=uniq)
    top.append({"name": genre.name, "id": genre.id})

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(top, f, indent=4)

# with open(file_path, "r", encoding="utf-8") as f:
#     dat = json.load(f)
#     pprint(dat[0])
