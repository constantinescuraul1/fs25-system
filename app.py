from flask import Flask, render_template_string, request, redirect
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
    border-radius: 12px;
}}
input {{
    background: #334155 !important;
    border: none !important;
    color: white !important;
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
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM players")
    total = c.fetchone()[0]
    conn.close()

    content = f"""
    <h2>Dashboard</h2>
    <div class="card card-custom p-4 mt-3">
        Total jucători: {total}
    </div>
    """
    return layout(content)

# ================= PLAYERS =================

@app.route("/players")
def players():
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM players")
    data = c.fetchall()
    conn.close()

    content = """
    <h2>Jucători</h2>
    <a class="btn btn-success mb-3" href="/add_player">+ Adaugă Jucător</a>

    <div class="card card-custom p-3">
    <table class="table table-dark table-hover">
    <thead>
    <tr>
        <th>ID</th>
        <th>Nume Discord</th>
        <th>Nume în joc</th>
        <th>Puncte</th>
        <th>Acțiuni</th>
    </tr>
    </thead>
    <tbody>
    """

    for p in data:
        content += f"""
        <tr>
            <td>{p[0]}</td>
            <td>{p[1]}</td>
            <td>{p[2]}</td>
            <td>{p[3]}</td>
            <td>
                <a class="btn btn-primary btn-sm" href="/edit_player/{p[0]}">Edit</a>
                <a class="btn btn-danger btn-sm" href="/delete_player/{p[0]}">Șterge</a>
            </td>
        </tr>
        """

    content += "</tbody></table></div>"

    return layout(content)

# ================= ADD =================

@app.route("/add_player", methods=["GET","POST"])
def add_player():

    if request.method == "POST":
        conn = connect()
        c = conn.cursor()
        c.execute("""
        INSERT INTO players VALUES (?,?,?,?)
        """, (
            request.form["discord_id"],
            request.form["discord_name"],
            request.form["ingame_name"],
            request.form["points"]
        ))
        conn.commit()
        conn.close()
        return redirect("/players")

    content = """
    <h2>Adaugă Jucător</h2>
    <form method="post">
        <div class="mb-3">
            <label>ID Discord</label>
            <input name="discord_id" class="form-control">
        </div>
        <div class="mb-3">
            <label>Nume Discord</label>
            <input name="discord_name" class="form-control">
        </div>
        <div class="mb-3">
            <label>Nume în joc</label>
            <input name="ingame_name" class="form-control">
        </div>
        <div class="mb-3">
            <label>Puncte</label>
            <input name="points" value="0" class="form-control">
        </div>
        <button class="btn btn-success">Salvează</button>
    </form>
    """
    return layout(content)

# ================= EDIT =================

@app.route("/edit_player/<int:id>", methods=["GET","POST"])
def edit_player(id):

    conn = connect()
    c = conn.cursor()

    if request.method == "POST":
        c.execute("""
        UPDATE players
        SET discord_name=?, ingame_name=?, points=?
        WHERE discord_id=?
        """, (
            request.form["discord_name"],
            request.form["ingame_name"],
            request.form["points"],
            id
        ))
        conn.commit()
        conn.close()
        return redirect("/players")

    c.execute("SELECT * FROM players WHERE discord_id=?", (id,))
    p = c.fetchone()
    conn.close()

    content = f"""
    <h2>Modifică Jucător</h2>
    <form method="post">
        <div class="mb-3">
            <label>Nume Discord</label>
            <input name="discord_name" value="{p[1]}" class="form-control">
        </div>
        <div class="mb-3">
            <label>Nume în joc</label>
            <input name="ingame_name" value="{p[2]}" class="form-control">
        </div>
        <div class="mb-3">
            <label>Puncte</label>
            <input name="points" value="{p[3]}" class="form-control">
        </div>
        <button class="btn btn-primary">Salvează</button>
    </form>
    """
    return layout(content)

# ================= DELETE =================

@app.route("/delete_player/<int:id>")
def delete_player(id):
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM players WHERE discord_id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/players")

# ================= START =================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
