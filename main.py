from models import load_clip, load_blip

clip_model, clip_tokenizer, clip_img_processor = load_clip()
blip_model, blip_processor = load_blip()

def generate_embeddings_image(image):
    processed_image = clip_img_processor([image])
    model_input = {"pixel_values": processed_image}
    model_output = clip_model(**model_input)
    [embeds] = model_output.image_embeds
    return embeds.tolist()

def generate_embeddings_text(text):
    tokens = clip_img_processor([text])
    model_input = {"input_ids": tokens}
    model_output = clip_model(**model_input)
    [embeds] = model_output.text_embeds
    return embeds.tolist()

def generate_caption(image):
    inputs = blip_processor(images=image, return_tensors="pt")
    output = blip_model.generate(**inputs, max_new_tokens=1000)
    caption = blip_processor.decode(output[0], skip_special_tokens=True)
    return caption.replace("arafed", "").lstrip() # yes
