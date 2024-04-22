# Memegraph

> If it exists, there is a meme of it.

Memegraph is a meme search engine that uses OpenAI CLIP image embeddings to find similar visually similar images.

## Development

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

Modify `main.py` to point to the correct image directory and database.

Generate image embeddings, store images in an object storage bucket, and store embeddings in a database

```bash
python main.py
```

### Running the API

Navigate to `api/` directory

```bash
cd web
```

Modify `app.py` and populate the connection string for the Postgres database

Install dependencies

```bash
pip install -r requirements.txt
```

Run the app

```bash
flask --app app run
```

### Running the web app

Navigate to `web/` directory

```bash
cd web
```

Install dependencies

```bash
npm install
```

Run the development server

```bash
npm run dev
```

## Stack

Model is based on OpenAI's CLIP model and Apple's MLX format.

Image embeddings are stored in Postgres with pgvector.

API is built using Flask, handles image uploads and queries the database for similar images.

Web app is built using Solid.js. I initially used Flask for the frontend but I wanted to avoid page reloads when navigating between pages.
