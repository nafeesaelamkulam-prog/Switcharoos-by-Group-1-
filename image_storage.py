import io
import sqlite3
from contextlib import contextmanager
from pathlib import Path

from PIL import Image

DB_PATH = Path(__file__).with_name("closet.db")


@contextmanager
def _connect():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    try:
        with connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS clothes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    colour TEXT NOT NULL,
                    image BLOB NOT NULL
                )
            """)
            yield connection
    finally:
        connection.close()


def save_image(image, name, category, colour, remove_background=True):
    if isinstance(image, (str, Path)):
        with Image.open(image) as opened:
            image = opened.convert("RGBA")
    elif isinstance(image, Image.Image):
        image = image.convert("RGBA")
    else:
        raise TypeError("image must be a file path or PIL Image")

    if remove_background:
        from rembg import remove
        image = remove(image)

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")

    with _connect() as db:
        cursor = db.execute(
            "INSERT INTO clothes (name, category, colour, image) VALUES (?, ?, ?, ?)",
            (name, category, colour, buffer.getvalue()),
        )
        return cursor.lastrowid


def get_images(category=None, colour=None):
    query = "SELECT * FROM clothes WHERE 1=1"
    values = []
    if category:
        query += " AND LOWER(category) = LOWER(?)"
        values.append(category)
    if colour:
        query += " AND LOWER(colour) = LOWER(?)"
        values.append(colour)

    with _connect() as db:
        rows = db.execute(query, values).fetchall()

    items = []
    for row in rows:
        image = Image.open(io.BytesIO(row["image"]))
        image.load()
        items.append({
            "id": row["id"],
            "name": row["name"],
            "category": row["category"],
            "colour": row["colour"],
            "image": image,
        })
    return items


def get_image(image_id):
    return next((item for item in get_images() if item["id"] == image_id), None)


def delete_image(image_id):
    with _connect() as db:
        result = db.execute("DELETE FROM clothes WHERE id = ?", (image_id,))
        return result.rowcount > 0
