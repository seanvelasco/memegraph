from flask import Flask, render_template, g, request
import psycopg
import os
from clip.main import process_text

DB_NAME = os.environ.get("DATABASE_NAME", "")
DB_USER = os.environ.get("DATABASE_USER", "")
DB_PASS = os.environ.get("DATABASE_PASS", "")
DB_HOST = os.environ.get("DATABASE_HOST", "")
DB_PORT = os.environ.get("DATABASE_PORT", "")

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

def get_conn():
    if "conn" not in g:
        g.conn = psycopg.connect(f"dbname={DB_NAME} user={DB_USER} password={DB_PASS} host={DB_HOST} port={DB_PORT}")
    return g.conn

@app.route("/")
def home():
    conn = get_conn()

    with get_conn() as conn:

        images = conn.cursor().execute("SELECT id FROM images ORDER BY RANDOM() LIMIT %(limit)s", {"limit":42}).fetchall()


        if not images:
            return render_template('404.html'), 404

        images = [{'id': id} for (id,) in images]
        
        return images
    
@app.route("/count")
def count():
    with get_conn() as conn:
        count = conn.cursor().execute("SELECT COUNT(*) FROM images").fetchone()[0]
        return count
    

@app.route("/search")
def search():
    query = request.args.get("text")

    print(query)

    with get_conn() as conn:

        embedding = process_text(query)

        print(embedding)

        query = """SELECT id, embedding <=> %(embedding)s AS distance
        FROM images
        WHERE embedding IS NOT NULL
        ORDER BY distance ASC LIMIT 30"""

        images = conn.cursor().execute(query,  {"embedding": embedding}).fetchall()

        print(images)

        images = [{'id': id ,"distance": round(distance, 2), "similarity": round((1 - distance) * 100)} for (id, distance) in images]

        return images
           
@app.route("/<image>")
def image(image):

    with get_conn() as conn:

        query = """SELECT id, images.embedding <=> (SELECT embedding FROM images WHERE id = %(id)s) AS distance
        FROM images
        WHERE id != %(id)s
        AND embedding IS NOT NULL
        AND 1 - (images.embedding <=> (SELECT embedding FROM images WHERE id = %(id)s)) > 0.7
        ORDER BY distance ASC LIMIT 30"""

        images = conn.cursor().execute(query,  {"id": image}).fetchall()

        images = [{'id': id ,"distance": round(distance, 2), "similarity": round((1 - distance) * 100)} for (id, distance) in images]

        return images

@app.errorhandler(404)
@app.route("/404")
def not_found():
    return 

if __name__ == "__main__":
    app.run(debug=True)