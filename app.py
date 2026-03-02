from flask import Flask, render_template_string
import sqlite3
import os

app = Flask(__name__)

# ================= DATABASE =================

def connect():
    return sqlite3.connect("fs25.db")

def setup():
    conn = connect()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS players (
        discord_id INTEGER PRIMARY KEY,
        discord_name TEXT,
        ingame_name TEXT,
        points INTEGER DEFAULT 0
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS vehicles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        owner_id INTEGER,
        plate TEXT
    )
    """)

    conn.commit()
    conn.close()

setup()

# ================= LAYOUT =================

def layout(content):

    return f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">

<style>
body {{
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
}}
.sidebar {{
    height: 100vh;
    background: #111827;
    padding-top: 20px;
}}
.sidebar a {{
    color: #cbd5e1;
    display: block;
    padding: 12px 20px;
    text-decoration: none;
}}
.sidebar a:hover {{
    background: #1f2937;
    color: white;
}}
.card-custom {{
    background: #1e293b;
    border: none;
    border-radius: 12px;
}}
</style>
</head>
<body>

<div class="container-fluid">
<div class="row">

<div class="col-2 sidebar">
    <h4 class="text-center text-white mb-4">FS25 Admin</h4>
    <a href="/">🏠 Dashboard</a>
    <a href="/players">👤 Jucători</a>
    <a href="/vehicles">🚜 Utilaje</a>
    <a href="/attachments">🔧 Atașamente</a>
    <a href="/fields">🌾 Terenuri</a>
    <a href="/factories">🏭 Fabrici</a>
    <a href="/animals">🐄 Animale</a>
    <a href="/rules">📊 Reguli Puncte</a>
    <a href="/pending">⏳ Activități Pending</a>
    <a href="/penalties">⚠ Penalizări</a>
</div>

<div class="col-10 p-4">
{content}
</div>

</div>
</div>

</body>
</html>
"""

# ================= DASHBOARD =================

@app.route("/")
def dashboard():
    content = """
    <h2>Dashboard Premium</h2>
    <div class="card card-custom p-4 mt-3">
        Sistem activ și stabil.
    </div>
    """
    return layout(content)

# ================= PLACEHOLDER ROUTES =================

@app.route("/players")
def players():
    return layout("<h2>Jucători</h2>")

@app.route("/vehicles")
def vehicles():
    return layout("<h2>Utilaje</h2>")

@app.route("/attachments")
def attachments():
    return layout("<h2>Atașamente</h2>")

@app.route("/fields")
def fields():
    return layout("<h2>Terenuri</h2>")

@app.route("/factories")
def factories():
    return layout("<h2>Fabrici</h2>")

@app.route("/animals")
def animals():
    return layout("<h2>Animale</h2>")

@app.route("/rules")
def rules():
    return layout("<h2>Reguli Puncte</h2>")

@app.route("/pending")
def pending():
    return layout("<h2>Activități Pending</h2>")

@app.route("/penalties")
def penalties():
    return layout("<h2>Penalizări</h2>")

# ================= START =================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
