import csv
from datetime import datetime

from my_app.models import TopSongPoularity

with open('top50contry.csv', 'r') as fin:
    reader = csv.reader(fin)
    headers = next(reader, None)
    for row in reader:
        obj = {
            "title": row[1],
            "artist": row[2],
            "top_genre": row[3],
            "year": int(row[4]),
            "pop": int(row[15]),
            "duration": int(row[12]),
            "country": row[16]
        }
        TopSongPoularity.objects.create(**obj)
