<img width="150" src="static/favicon.png" />

# memegraph

Memegraph is a search engine and recommendation engine for memes using OpenAI's CLIP model.

Search memes via keywords, explore memes with the same template, and discover memes that are visually similar.

### Don't know the name of a meme? Just describe the meme!

![Guy Thinking In Bed meme](https://img.sean.app/memegraph_thinking_in_bed_meme.png)

### Discover memes about your favorite topics

![The Office memes](https://img.sean.app/memegraph_the_office.png)

### Look up that obscure meme you saw

![Memes about Spongebob and Myers-Briggs Type Indicator (MBTI)](https://img.sean.app/memegraph_as_mbti.png)

### Discover memes that are visually similar

![Boardroom meme](https://img.sean.app/memegraph_boardroom.png)

### New way to browse memes

![Memegraph home](https://img.sean.app/memegraph_home.png)

## Development

MLX requires a Mac with an Apple Silicon processor to generate embeddings.

You can still run the app without image embeddings, but you will not be able to search for memes by image similarity.

### Generate image embeddings

Install dependencies

```bash
pip install -r requirements.txt
```

Download OpenAI CLIP model (clip-vit-base-patch32) from Hugging Face and convert to Apple's MLX

```bash
python clip/convert.py
```

The model is dowloaded to `mlx_model/` directory unless argument `--model_dir` is provided.

Modify `main.py` to point to the correct model, images source directory, blob storage bucket, and database.

Generate image embeddings, store images in an blob storage bucket, and store embeddings in a database

```bash
python main.py
```

Run the app

```bash
python app.py
```

## Data

All memes were retrieved from the top 1000 posts of all time on [Reddit's meme subreddits](https://www.reddit.com/t/memes) using [PRAW](https://praw.readthedocs.io/en/stable/) on the Reddit's API free tier.
