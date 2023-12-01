import csv
import json
import time
from pprint import pprint
from uuid import uuid4

import requests

from bookdata import BOOKS_M
from models.book import Book

# CSV file path
file_path = "books.json"
csv_file = "data.csv"

top = []
with open(csv_file, "r", encoding="utf-8") as f:
    csvreader = csv.reader(f)
    for row in csvreader:
        # time.sleep(0.5)
        print(row[0])
        Book(
            id=str(uuid4()),
            title=row[0],
            genre_id=row[1],
            cover_image_url=row[2],
            description=row[3],
            publication_date=row[4],
            language=row[5],
            author=row[6],
        )
        top.append(
            {
                "id": str(uuid4()),
                "title": row[0],
                "genre_id": row[1],
                "cover_image_url": row[2],
                "description": row[3],
                "publication_date": row[4],
                "language": row[5],
                "author": row[6],
            }
        )


# json_gern = {}
# for uniq in unique:
#     genre = Genre(id=str(uuid4()), name=uniq)
#     top.append({"name": genre.name, "id": genre.id})

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(top, f, indent=4)
