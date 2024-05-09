import os
import hashlib
from PIL import Image
import psycopg
from api.clip.main import process_image

DB_CONN_INFO = os.environ.get("DB_CONN_INFO", "")

def get_or_create_db():
    with psycopg.connect(DB_CONN_INFO) as conn:
        conn.cursor().execute('CREATE EXTENSION IF NOT EXISTS vector')
        conn.cursor().execute('CREATE TABLE IF NOT EXISTS images (id TEXT NOT NULL PRIMARY KEY, md5 TEXT NOT NULL, embedding VECTOR(512))')
        conn.cursor().execute('CREATE INDEX IF NOT EXISTS idx_images_id ON images (id)')
        conn.commit()
        return conn

def get_all_images_in_db():
    with get_all_images_in_db() as conn:
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
    with get_all_images_in_db() as conn:
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

                conn.cursor().execute(query, {"id": image_id, "hash": md5_hash, "embedding": embedding})


        conn.commit()