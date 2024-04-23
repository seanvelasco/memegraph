from clip.image_processor import CLIPImageProcessor
from clip.model import CLIPModel
from clip.tokenizer import CLIPTokenizer
from PIL import Image
import os
import hashlib
import psycopg

# Load the model, tokenizer and image processor from the OpenAI CLIP transformer model
def load_clip(model_dir):
    model = CLIPModel.from_pretrained(model_dir)
    tokenizer = CLIPTokenizer.from_pretrained(model_dir)
    img_processor = CLIPImageProcessor.from_pretrained(model_dir)
    return model, tokenizer, img_processor

# Load image, preprocess image, and generate embeddings
def process_image(image):
    processed_image = img_processor([image])
    input = {"pixel_values": processed_image}
    output = model(**input)
    embeds = output.image_embeds[0]
    return embeds.tolist()

def process_text(text):
    tokens = tokenizer(text)
    input = {"input_ids": tokens}
    output = model(**input)
    embeds = output.text_embeds[0]
    return embeds.tolist()

# conn = psycopg.connect("")

# conn.cursor().execute('CREATE EXTENSION IF NOT EXISTS vector')

# conn.cursor().execute('CREATE TABLE IF NOT EXISTS images (id TEXT NOT NULL PRIMARY KEY, md5 TEXT NOT NULL, embedding VECTOR(512))')

# conn.cursor().execute('CREATE INDEX IF NOT EXISTS idx_images_id ON images (id)')

# conn.commit()

model, tokenizer, img_processor = load_clip("mlx_model")

def process_images(dir):
    for file in os.listdir(dir):
        name, ext = os.path.splitext(file)
        if ext in [".jpeg", ".jpg", ".png", ".gif"]:
        
            image_path = os.path.join(dir, file)

            image = Image.open(image_path)

            if ext == ".gif":
                image = image.convert("RGB")

            if ext == ".png":
                image = image.convert("RGB")

            hash = hashlib.md5(image.tobytes()).hexdigest()

            embedding = process_image(image)

            query = "INSERT INTO images (id, md5, embedding) VALUES (%(id)s, %(hash)s, %(embedding)s)"

            conn.cursor().execute(query, {"id": name, "hash": hash, "embedding": embedding})


    # conn.commit()