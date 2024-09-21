# [memegraph](https://memegraph.sean.app)

Memegraph is a search engine and recommendation system for memes using OpenAI CLIP.

Search memes via keywords, explore memes with the same template, and discover memes that are visually similar.

### Don't know the name of a meme? Just describe the meme!

![Guy Thinking In Bed meme](https://img.sean.app/memegraph_thinking_in_bed_meme.png)

### Discover memes about your favorite topics

![The Office memes](https://img.sean.app/memegraph_the_office.png)

### Looking for THAT obscure meme? Look it up!

![Memes about Spongebob and Myers-Briggs Type Indicator (MBTI)](https://img.sean.app/memegraph_as_mbti.png)

### Discover similar memes

![Boardroom meme](https://img.sean.app/memegraph_boardroom.png)

### New way to browse memes

![Memegraph home](https://img.sean.app/memegraph_home.png)

## Development

> [!IMPORTANT]  
> This app uses MLX to run CLIP. To generate embeddings, a device with an Apple Silicon processor is needed. For non-Apple Silicon devices, the app can still run, provided there are already images and embeddings in the database, but it will not be able to search for memes by image similarity.

Install dependencies

```bash
pip install -r requirements.txt
```

Download OpenAI CLIP model (clip-vit-base-patch32) from Hugging Face and convert to Apple's MLX

```bash
python clip/convert.py
```

The model is dowloaded to `clip/mlx_model/` directory unless argument `--model_dir` is provided.

Modify `main.py` to point to the correct model. This contains the functions to generate the embeddings.

Modify `script.py` to point to your images directory, blob storage, and Postgres database.

Generate image embeddings, store images in an blob storage bucket, and store embeddings in a database

```bash
python script.py
```

Run the app

```bash
python app.py
```

## Data

All memes were retrieved from the top 1000 posts of all time on [Reddit's meme subreddits](https://www.reddit.com/t/memes) using [PRAW](https://praw.readthedocs.io/en/stable/) on the Reddit's API free tier.

### Notes from the author

Python is not my primary language and I'm new to machine learning, so I greatly appreciate and welcome constructive feedback!
