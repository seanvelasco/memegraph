import os
from flask import Flask, render_template, g, request
from flask_cors import CORS
import psycopg
from main import process_text

DB_CONN_INFO = os.environ.get("DB_CONN_INFO")

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

def similarity(distance_value):
    return round((1 - distance_value) * 100)

def get_conn():
    if "conn" not in g:
        g.conn = psycopg.connect(DB_CONN_INFO)
    return g.conn


@app.route("/")
def home():
    with get_conn() as conn:
        query = "SELECT id FROM images ORDER BY RANDOM() LIMIT %(limit)s"
        params = {"limit": 80}
        images = conn.cursor().execute(query, params).fetchall()

        if not images:
            return render_template('404.html'), 404
        
        images = [{'id': id} for (id,) in images]

        best = request.accept_mimetypes.best_match(['application/json', 'text/html'])

        if best == 'application/json':
            return images
        else:
            count = conn.cursor().execute("SELECT COUNT(*) FROM images WHERE embedding IS NOT NULL").fetchone()[0]
            return render_template('home.html', images=images, count=count)

@app.route("/search")
def search():
    search_query = request.args.get('q') or request.args.get('query')
    print(search_query)
    embedding = process_text(search_query)
    with get_conn() as conn:
        query = """SELECT id, images.embedding <=> %(embedding)s AS distance
        FROM images WHERE embedding IS NOT NULL
        AND 1 - (images.embedding <=> %(embedding)s) > 0.3
        ORDER BY distance ASC LIMIT 30
        """
        images = conn.cursor().execute(query,  {"embedding": str(embedding)}).fetchall()
        # if not images:
        #     return render_template('404.html', count=count), 404
        # images = [{'id': id ,"distance": round(distance, 2), "similarity": similarity(distance)} for (id, distance) in images]

        images = [{'id': id ,"distance": round(distance, 2),"similarity": similarity(distance)}
                  for (id, distance) in images]
        
        best = request.accept_mimetypes.best_match(['application/json', 'text/html'])

        if best == 'application/json':
            return images
        else:
            count = conn.cursor().execute("SELECT COUNT(*) FROM images WHERE embedding IS NOT NULL").fetchone()[0]
            return render_template('home.html', images=images, count=count, query=search_query)
    
@app.route("/count")
def count():
    with get_conn() as conn:
        count = conn.cursor().execute("SELECT COUNT(*) FROM images WHERE embedding IS NOT NULL").fetchone()[0]
        return {"count": count}

@app.route("/<image>")
def image(image):
    with get_conn() as conn:
        query = """SELECT id,
        images.embedding <=> (SELECT embedding FROM images WHERE id = %(id)s) AS distance
        FROM images WHERE id != %(id)s
        AND embedding IS NOT NULL
        AND 1 - (images.embedding <=> (SELECT embedding FROM images WHERE id = %(id)s)) > 0.5
        ORDER BY distance ASC LIMIT 30"""
        images = conn.cursor().execute(query,  {"id": image}).fetchall()
        # if not images:
        #     return render_template('404.html', count=count), 404
        images = [{'id': id ,"distance": round(distance, 2),"similarity": similarity(distance)}
                  for (id, distance) in images]
        
        best = request.accept_mimetypes.best_match(['application/json', 'text/html'])

        if best == 'application/json':
            return images
        else:
            count = conn.cursor().execute("SELECT COUNT(*) FROM images WHERE embedding IS NOT NULL").fetchone()[0]
            return render_template('image.html', image=image, images=images, count=count)


if __name__ == "__main__":
    app.run(debug=True, port=5050)
