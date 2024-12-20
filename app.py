import os
import sys
from flask import Flask, render_template, g, request
from flask_cors import CORS
import psycopg
from dotenv import load_dotenv

if sys.platform == "darwin":
    from main import generate_embeddings_text

load_dotenv()

DB_CONN_INFO = str(os.environ.get("PG_CONN_STR"))

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, resources={r"/*": {"origins": "*"}})

def similarity(distance_value):
    """Calculate similarity percentage from distance."""

def get_conn():
    """Get database connection, creating it if necessary."""
    if "conn" not in g:
        g.conn = psycopg.connect(DB_CONN_INFO)
    return g.conn

@app.teardown_appcontext
def close_conn(exception):
    """Close the database connection at the end of the request."""
    conn = g.pop('conn', None)
    if conn is not None:
        conn.close()

@app.route("/")
def home():
    """Render the home page with random images."""
    with get_conn() as conn:
        query = "SELECT id, height, width, caption FROM images ORDER BY RANDOM() LIMIT %(limit)s"
        params = {"limit": 80}
        images = conn.cursor().execute(query, params).fetchall()

        if not images:
            return render_template('404.html'), 404

        images = [{'id': id, 'height': height, 'width': width, 'caption': caption} for (id, height, width,caption,) in images]
        count = conn.cursor().execute("SELECT COUNT(*) FROM images WHERE embedding IS NOT NULL").fetchone()[0]
        return render_template('home.html', images=images, count=count)

@app.route("/search")
def search():
    """Render search results based on a query."""
    search_query = request.args.get('q') or request.args.get('query')
    if sys.platform == "darwin":
        embedding = generate_embeddings_text(search_query)

        with get_conn() as conn:
            query = """
                SELECT id, images.embedding <=> %(embedding)s AS distance
                FROM images WHERE embedding IS NOT NULL
                AND 1 - (images.embedding <=> %(embedding)s) > 0.3
                ORDER BY distance ASC LIMIT 30
            """
            images = conn.cursor().execute(query, {"embedding": str(embedding)}).fetchall()
            count = conn.cursor().execute("SELECT COUNT(*) FROM images WHERE embedding IS NOT NULL").fetchone()[0]

            if not images:
                return render_template('404.html', count=count), 404

            images = [{'id': id, "distance": round(distance, 2), "similarity": similarity(distance)} for (id, distance) in images]

            return render_template('home.html', images=images, count=count, query=search_query)

@app.route("/count")
def count():
    """Return the count of images with embeddings."""
    with get_conn() as conn:
        count = conn.cursor().execute("SELECT COUNT(*) FROM images WHERE embedding IS NOT NULL").fetchone()[0]
        return {"count": count}

@app.route("/<image_id>")
def image(image_id):
    """Render details for a specific image and similar images."""
    with get_conn() as conn:
        with conn.cursor() as cursor:
            image = cursor.execute("SELECT id, height, width, caption FROM images WHERE id = %(id)s", {"id": image_id}).fetchone()
            query = """
                SELECT id, height, width, caption, images.embedding <=> (SELECT embedding FROM images WHERE id = %(id)s) AS distance
                FROM images WHERE id != %(id)s AND embedding IS NOT NULL
                AND 1 - (images.embedding <=> (SELECT embedding FROM images WHERE id = %(id)s)) > 0.5
                ORDER BY distance ASC LIMIT 30
            """
            images = cursor.execute(query, {"id": image_id}).fetchall()
            (count,) = cursor.execute("SELECT COUNT(*) as count FROM images WHERE embedding IS NOT NULL").fetchone()
            if not images:
                return render_template('404.html', count=count), 404
            images = [{'id': id, "distance": round(distance, 2), "similarity": similarity(distance), "height": height, "width": width, 'caption': caption} for (id, height, width, caption, distance) in images]
            image = {'id': image[0], 'height': image[1], 'width': image[2], 'caption': image[3]}
            return render_template('image.html', image=image, images=images, count=count)

if __name__ == "__main__":
    app.run(debug=True, port=5050)
