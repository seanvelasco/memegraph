"""Example scripts for generating embeddings"""

import os
import hashlib
from PIL import Image
import psycopg
from main import process_image

NAME = os.environ.get("DATABASE_NAME", "postgres")
USER = os.environ.get("DATABASE_USER", "postgres")
PASS = os.environ.get("DATABASE_PASS", "")
HOST = os.environ.get("DATABASE_HOST", "")
PORT = os.environ.get("DATABASE_PORT", "5432")

def get_or_create_database():
    """Create PostgreSQL database"""
    conn_str = f"dbname={NAME} user={USER} password={PASS} host={HOST} port={PORT}"
    with psycopg.connect(conn_str) as conn:
        conn.cursor().execute('CREATE EXTENSION IF NOT EXISTS vector')
        conn.cursor().execute('CREATE TABLE IF NOT EXISTS images (id TEXT NOT NULL PRIMARY KEY, md5 TEXT NOT NULL, embedding VECTOR(512))')
        conn.cursor().execute('CREATE INDEX IF NOT EXISTS idx_images_id ON images (id)')
        conn.commit()
        return conn

def get_all_images_in_db():
    """Get list of id's of all images in the database that has an embedding"""
    with get_or_create_database() as conn:
        query = "SELECT (id) embedding FROM images WHERE embedding IS NOT NULL"
        images = conn.cursor().execute(query).fetchall()
        return [image for [image] in images]

# def upload_iamges_to_bucket(dir):
#     for file in os.listdir(dir):
#         id, ext = os.path.splitext(file)
#         if ext in [".jpeg", ".jpg", ".png", ".gif"]:
#             print(f"Uploading {id}")
#             image_path = os.path.join(dir, file)
#             bucket.upload_file(image_path, f"images/{id}")

def process_images(dir):
    """Generate image embeddings in a directory and insert into database"""
    with get_or_create_database() as conn:
        all_images_in_db = get_all_images_in_db()
        for file in os.listdir(dir):
            image_id, ext = os.path.splitext(file)
            if ext in [".jpeg", ".jpg", ".png", ".gif"]:
                if image_id in all_images_in_db:
                    continue
            
                image_path = os.path.join(dir, file)

                image = Image.open(image_path)

                image = image.convert("RGB")

                md5_hash = hashlib.md5(image.tobytes()).hexdigest()

                embedding = process_image(image)

                query = "INSERT INTO images (id, md5, embedding) VALUES (%(id)s, %(hash)s, %(embedding)s)"

                conn.cursor().execute(query, {"id": id, "hash": md5_hash, "embedding": embedding})

                print(f"Inserted {id} with hash {hash}")

        conn.commit()