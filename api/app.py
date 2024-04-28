"""API handling vector embedding search"""

import os
from flask import Flask, render_template, g, request
from flask_cors import CORS
import psycopg
from main import process_text

NAME = os.environ.get("DATABASE_NAME", "postgres")
USER = os.environ.get("DATABASE_USER", "postgres")
PASS = os.environ.get("DATABASE_PASS", "")
HOST = os.environ.get("DATABASE_HOST", "")
PORT = os.environ.get("DATABASE_PORT", "5432")

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

def similarity(distance_value):
    """Return similarity percentage given a distance float"""
    return round((1 - distance_value) * 100)

def get_conn():
    """Connect to database and connection"""
    if "conn" not in g:
        conn_str = f"dbname={NAME} user={USER} password={PASS} host={HOST} port={PORT}"
        g.conn = psycopg.connect(conn_str)
    return g.conn

@app.route("/")
def home():
    """Get images for display in home page"""
    with get_conn() as conn:
        query = "SELECT id FROM images ORDER BY RANDOM() LIMIT %(limit)s"
        params = {"limit":42}
        images = conn.cursor().execute(query, params).fetchall()
        if not images:
            return render_template('404.html'), 404
        return [{'id': id} for (id,) in images]

@app.route("/count")
def count():
    """Get number of images in the database with embeddings"""
    with get_conn() as conn:
        query = "SELECT COUNT(*) FROM images WHERE embedding IS NOT NULL"
        return conn.cursor().execute(query).fetchone()[0]

@app.route("/search")
def search():
    """Return similar images given a search query"""
    query = request.args.get("query")
    embedding = process_text(query)
    with get_conn() as conn:
        query = """SELECT id, images.embedding <=> %(embedding)s AS distance
        FROM images WHERE embedding IS NOT NULL
        ORDER BY distance ASC LIMIT 30
        """
        images = conn.cursor().execute(query,  {"embedding": str(embedding)}).fetchall()
        images = [{'id': id ,"distance": round(distance, 2), "similarity": similarity(distance)} for (id, distance) in images]
        return images
    
@app.route("/<image>")
def image(image_id):
    """Return image corresponding to the id"""
    with get_conn() as conn:
        query = """SELECT id,
        images.embedding <=> (SELECT embedding FROM images WHERE id = %(id)s) AS distance
        FROM images WHERE id != %(id)s
        AND embedding IS NOT NULL
        AND 1 - (images.embedding <=> (SELECT embedding FROM images WHERE id = %(id)s)) > 0.7
        ORDER BY distance ASC LIMIT 30"""
        images = conn.cursor().execute(query,  {"id": image_id}).fetchall()
        images = [{'id': id ,"distance": round(distance, 2),"similarity": similarity(distance)}
                  for (id, distance) in images]
        return images

@app.errorhandler(404)
def not_found():
    """Return 404 error"""
    return

if __name__ == "__main__":
    app.run(debug=True)
