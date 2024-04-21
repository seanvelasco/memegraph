# Memegraph

### Generate image embeddings

Navigate to `clip/` directory

```bash
cd clip
```

Install dependencies

```bash
pip install -r requirements.txt
```

Download OpenAI CLIP model (clip-vit-base-patch32) from Hugging Face and convert to Apple's MLX

```bash
python convert.py
```

The model is dowloaded to `mlx_model/` directory unless argument `--model_dir` is provided.

Modify `main.py` to point to the correct image directory and database

### Running the web app

Navigate to `web/` directory

```bash
cd web
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the app

```bash
flask --app web run
```
