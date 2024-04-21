from flask import Flask, render_template, g
import psycopg
import os

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

def count_records():
    with get_conn() as conn:
            [count] = conn.cursor().execute("SELECT COUNT(*) FROM images WHERE embedding IS NOT NULL").fetchone()
            return count

@app.route("/")
def home():
    conn = get_conn()

    with get_conn() as conn:

        images = conn.cursor().execute("SELECT id FROM images ORDER BY RANDOM() LIMIT %(limit)s", {"limit":42}).fetchall()

        count = count_records()

        if not images:
            return render_template('404.html'), 404

        images = [{'id': id} for (id,) in images]
        
        return render_template('index.html', count=count, images=images)
           
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

        count = count_records()

        if not images:
            return render_template('404.html'), 404

        images = [{'id': id ,"distance": round(distance, 2), "similarity": round((1 - distance) * 100)} for (id, distance) in images]

        return render_template('image.html', count=count, image=image, images=images)

@app.errorhandler(404)
@app.route("/404")
def not_found():
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True)