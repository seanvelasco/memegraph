# from transformers import CLIPProcessor, CLIPModel, CLIPTokenizer, CLIPImageProcessor
from mlx.image_processor import CLIPImageProcessor
from mlx.model import CLIPModel
from mlx.tokenizer import CLIPTokenizer
from mlx.convert import get_model_path, torch_to_mx, save_weights
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch
import os
from pathlib import Path
import shutil

CLIP_MODEL = "openai/clip-vit-base-patch32"
CLIP_MODEL_PATH = "./clip"
BLIP_MODEL = "Salesforce/blip-image-captioning-large"
BLIP_MODEL_PATH = "./blip"

def load_clip():
    if os.path.isdir(CLIP_MODEL_PATH) == False:
        torch_path = get_model_path(CLIP_MODEL)
        model_path = Path(CLIP_MODEL_PATH)
        model_path.mkdir(parents=True, exist_ok=True)
        torch_weights = torch.load(torch_path / "pytorch_model.bin")
        weights = {
            k: torch_to_mx(v, dtype="float32") for k, v in torch_weights.items()
        }
        save_weights(model_path, weights)
        for fn in ["config.json", "merges.txt", "vocab.json", "preprocessor_config.json"]:
            shutil.copyfile(
                str(torch_path / f"{fn}"),
                str(model_path / f"{fn}"),
            )
    return (
        CLIPModel.from_pretrained(CLIP_MODEL_PATH),
        CLIPTokenizer.from_pretrained(CLIP_MODEL_PATH),
        CLIPImageProcessor.from_pretrained(CLIP_MODEL_PATH)
    )

def load_blip():
    if os.path.isdir(BLIP_MODEL_PATH) == False:
        model = BlipForConditionalGeneration.from_pretrained(BLIP_MODEL)
        processor = BlipProcessor.from_pretrained(BLIP_MODEL)
        model.save_pretrained(BLIP_MODEL_PATH)
        processor.save_pretrained(BLIP_MODEL_PATH)
    else: 
        model = BlipForConditionalGeneration.from_pretrained(BLIP_MODEL_PATH)
        processor = BlipProcessor.from_pretrained(BLIP_MODEL_PATH)
    return model, processor