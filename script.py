import os
import hashlib
from PIL import Image
import psycopg
from main import process_image
import requests
from io import BytesIO
import asyncio
import asyncpg
from aiohttp import ClientSession

DB_CONN_INFO = os.environ.get("DB_CONN_INFO", "") # format: "user=sean password=1234 host=example.com port=5432 dbname=postgres"
DB_CONN_INFO_2 = os.environ.get("DB_CONN_INFO", "") # format: "postgresql://sean:1234@example.com:5432/postgres"

def get_or_create_db():
    with psycopg.connect(DB_CONN_INFO) as conn:
        conn.cursor().execute('CREATE EXTENSION IF NOT EXISTS vector')
        conn.cursor().execute('CREATE TABLE IF NOT EXISTS images (id TEXT NOT NULL PRIMARY KEY, md5 TEXT NOT NULL, embedding VECTOR(512), width INT, height INT, source TEXT, nsfw BOOL)')
        conn.cursor().execute('CREATE INDEX IF NOT EXISTS idx_images_id ON images (id)')
        conn.commit()
        return conn

def get_all_images_in_db():
    with psycopg.connect(DB_CONN_INFO) as conn:
        query = "SELECT (id) embedding FROM images WHERE embedding IS NOT NULL"
        images = conn.cursor().execute(query).fetchall()
        return [image for [image] in images]
    

def get_images_in_db_without_image_dimensions():
    with psycopg.connect(DB_CONN_INFO) as conn:
        query = "SELECT (id) embedding FROM images WHERE width IS NULL AND height IS NULL"
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

#########

async def update_entry_with_dimensions(pool, id, width, height):
    async with pool.acquire() as conn:
        # query = "UPDATE images SET width = %(width)s, height = %(height)s WHERE id = %(id)s"
        # await conn.execute(query, {"width": width, "height": height, "id": id})
        query = "UPDATE images SET width = $1, height = $2 WHERE id = $3"
        await conn.execute(query, width, height, id)
        print("Updated", id, "with dimensions", width, height)
    
async def open_image_and_update_db(session, pool, image):
    url = "https://memes.sean.app/" + image
    async with session.get(url) as res:
        image_data = await res.read()
        with Image.open(BytesIO(image_data)) as img:
            width, height = img.size
            await update_entry_with_dimensions(pool, image, width, height)
            return

async def process_all_images():
    async with await asyncpg.create_pool(DB_CONN_INFO_2) as pool:
        all_images = get_images_in_db_without_image_dimensions()
        print(len(all_images))
        async with ClientSession() as session:
            tasks = [open_image_and_update_db(session, pool, image) for image in all_images]
            await asyncio.gather(*tasks)

# async def main():
#     await process_all_images()

# if __name__ == "__main__":
#     asyncio.run(main())