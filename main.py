"""Functions to generate embeddings from image and text"""

from clip.image_processor import CLIPImageProcessor
from clip.model import CLIPModel
from clip.tokenizer import CLIPTokenizer

# Load the model, tokenizer and image processor from the OpenAI CLIP transformer model
def load_clip(model_dir):
    """Return model, tokenizer, and image processor"""
    return (
        CLIPModel.from_pretrained(model_dir),
        CLIPTokenizer.from_pretrained(model_dir),
        CLIPImageProcessor.from_pretrained(model_dir)
    )

# Load PIL image, preprocess image, and generate embeddings
def process_image(image):
    """Preprocess image / generate embeddings for a PIL image"""
    processed_image = img_processor([image])
    model_input = {"pixel_values": processed_image}
    model_output = model(**model_input)
    [embeds] = model_output.image_embeds
    return embeds.tolist()

# Generate embeddings for text
def process_text(text):
    """Preprocess text / generate embeddings for a text"""
    tokens = tokenizer([text])
    model_input = {"input_ids": tokens}
    model_output = model(**model_input)
    [embeds] = model_output.text_embeds
    return embeds.tolist()

model, tokenizer, img_processor = load_clip("clip/mlx_model")
