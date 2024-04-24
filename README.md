# Memegraph

Memegraph is a meme search engine that uses OpenAI CLIP image embeddings to find similar visually similar images.

It can be used to search for memes using keywords, explore memes with the same template, and discover memes that are visually similar. It's a search engine and a recommendation engine for memes.

Built for the [Supabase Open Source Hackathon 2024](https://supabase.com/blog/supabase-oss-hackathon).

### Capabilities

![https://img.sean.app/memegraph-jim.png](https://img.sean.app/memegraph-jim.png)
Jimbo, Jim, James, Jimothy

![https://img.sean.app/memegraph-obama-kanye.png](https://img.sean.app/memegraph-obama-kanye.png)
Ability to recognize both Obama and Kanye on an edited face swap meme

![https://img.sean.app/memegraph-skyrim.png](https://img.sean.app/memegraph-skyrim.png)
Searching for Skyrim memes using keyword "skyrim"

![https://img.sean.app/memegraph-leos.png](https://img.sean.app/memegraph-leos.png)
The many times Leonardo DiCaprio has become a meme template

![https://img.sean.app/memegraph-spongebob.png](https://img.sean.app/memegraph-spongebob.png)
Spongebob memes

![https://img.sean.app/memegraph-suggestion-meme.png](https://img.sean.app/memegraph-suggestion-meme.png)
Search for memes with the same template

![https://img.sean.app/memegraph-dragons.png](https://img.sean.app/memegraph-dragons.png)
Search for memes with the same template

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

## Image data

All memes were sourced from the top posts of all time on [Reddit's meme subreddits](https://www.reddit.com/t/memes) using [PRAW](https://praw.readthedocs.io/en/stable/) on the free tier of Reddit's API.

## Stack

Transformer model - OpenAI CLIP using Apple MLX format

Vector database - PostgreSQL with pgvector in Supabase

Object storage - Supabase Storage

API - Flask hosted locally (exposed via tunneling) and in Render

Web app - Solid.js hosted in Cloudflare Pages
