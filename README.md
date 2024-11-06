<img src="./static/favicon.svg" width="150"></img>

# Memegraph

Memegraph is a search engine and recommendation system for memes using OpenAI CLIP and Salesforce BLIP.

Search memes in natural langauge, explore memes with the same template, and discover memes that are visually similar.

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

Modify scripts in `/scripts` to point to your images directory, blob storage, and Postgres database.

Generate image embeddings and generate image captions

```bash
python main.py
```

Run the app in development

```bash
python app.py
```

Run the app in production

```bash
waitress-serve app:app
```

## Data

All memes were retrieved from the top 1000 posts of all time on [Reddit's meme subreddits](https://www.reddit.com/t/memes) using [PRAW](https://praw.readthedocs.io/en/stable/) on the Reddit's API free tier.

### Notes from the author

Python is not my primary language and I'm new to machine learning, so I greatly appreciate and welcome constructive feedback!
