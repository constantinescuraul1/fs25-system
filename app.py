from flask import Flask, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "fs25secretkey"

ADMIN_PASSWORD = "1234"

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
        plate TEXT,
        points INTEGER DEFAULT 0
    )
    """)
    conn.commit()
    conn.close()

setup()

# ================= LOGIN =================

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["password"] == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect("/panel")
    return """
    <style>
    body{background:#0f172a;color:white;font-family:Arial;text-align:center;margin-top:150px}
    input{padding:10px;border-radius:6px;border:none;width:200px}
    button{padding:10px 20px;background:#3b82f6;border:none;color:white;border-radius:6px}
    </style>
    <h1>FS25 Admin Login</h1>
    <form method="post">
        <input type="password" name="password" placeholder="Parolă"><br><br>
        <button type="submit">Login</button>
    </form>
    """

# ================= PANEL =================

@app.route("/panel")
def panel():
    if "admin" not in session:
        return redirect("/")

    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM players")
    players = c.fetchall()
    conn.close()

    html = """
    <style>
    body{background:#0f172a;color:white;font-family:Arial}
    .container{width:900px;margin:auto}
    .card{background:#1e293b;padding:20px;margin-bottom:15px;border-radius:10px}
    .btn{padding:6px 12px;border-radius:6px;text-decoration:none}
    .add{background:#22c55e;color:white}
    .edit{background:#3b82f6;color:white}
    .delete{background:#ef4444;color:white}
    a{color:white}
    </style>
    <div class='container'>
    <h1>FS25 Admin Panel</h1>
    <a class='btn add' href='/add'>Adaugă Jucător</a>
    <br><br>
    """

    for p in players:
        html += f"""
        <div class='card'>
        <b>{p[2]}</b> ({p[1]})<br>
        ID: {p[0]}<br>
        Nr: {p[3]}<br>
        Puncte: {p[4]}<br><br>
        <a class='btn edit' href='/edit/{p[0]}'>Modifică</a>
        <a class='btn delete' href='/delete/{p[0]}'>Șterge</a>
        </div>
        """

    html += "</div>"
    return html

# ================= ADD =================

@app.route("/add", methods=["GET", "POST"])
def add():
    if "admin" not in session:
        return redirect("/")

    if request.method == "POST":
        conn = connect()
        c = conn.cursor()
        c.execute("""
        INSERT INTO players (discord_id, discord_name, ingame_name, plate)
        VALUES (?, ?, ?, ?)
        """, (
            request.form["discord_id"],
            request.form["discord_name"],
            request.form["ingame_name"],
            request.form["plate"]
        ))
        conn.commit()
        conn.close()
        return redirect("/panel")

    return """
    <style>
    body{background:#0f172a;color:white;font-family:Arial;text-align:center;margin-top:100px}
    input{padding:10px;border-radius:6px;border:none;width:250px;margin:5px}
    button{padding:10px 20px;background:#22c55e;border:none;color:white;border-radius:6px}
    </style>
    <h2>Adaugă Jucător</h2>
    <form method="post">
        <input name="discord_id" placeholder="Discord ID"><br>
        <input name="discord_name" placeholder="Nume Discord"><br>
        <input name="ingame_name" placeholder="Nume în joc"><br>
        <input name="plate" placeholder="Nr înmatriculare"><br><br>
        <button type="submit">Salvează</button>
    </form>
    """

# ================= EDIT =================

@app.route("/edit/<int:discord_id>", methods=["GET", "POST"])
def edit(discord_id):
    if "admin" not in session:
        return redirect("/")

    conn = connect()
    c = conn.cursor()

    if request.method == "POST":
        c.execute("""
        UPDATE players
        SET discord_name=?, ingame_name=?, plate=?, points=?
        WHERE discord_id=?
        """, (
            request.form["discord_name"],
            request.form["ingame_name"],
            request.form["plate"],
            request.form["points"],
            discord_id
        ))
        conn.commit()
        conn.close()
        return redirect("/panel")

    c.execute("SELECT * FROM players WHERE discord_id=?", (discord_id,))
    p = c.fetchone()
    conn.close()

    return f"""
    <style>
    body{{background:#0f172a;color:white;font-family:Arial;text-align:center;margin-top:100px}}
    input{{padding:10px;border-radius:6px;border:none;width:250px;margin:5px}}
    button{{padding:10px 20px;background:#3b82f6;border:none;color:white;border-radius:6px}}
    </style>
    <h2>Modifică Jucător</h2>
    <form method="post">
        <input name="discord_name" value="{p[1]}"><br>
        <input name="ingame_name" value="{p[2]}"><br>
        <input name="plate" value="{p[3]}"><br>
        <input name="points" value="{p[4]}"><br><br>
        <button type="submit">Salvează</button>
    </form>
    """

# ================= DELETE =================

@app.route("/delete/<int:discord_id>")
def delete(discord_id):
    if "admin" not in session:
        return redirect("/")

    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM players WHERE discord_id=?", (discord_id,))
    conn.commit()
    conn.close()
    return redirect("/panel")
