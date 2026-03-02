from flask import Flask, request, redirect
import sqlite3

app = Flask(__name__)

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

@app.route("/")
def index():
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM players")
    players = c.fetchall()
    conn.close()

    html = "<h1>FS25 Admin Panel</h1>"
    html += "<a href='/add'>Adaugă Jucător</a><br><br>"

    for p in players:
        html += f"""
        <b>{p[2]}</b> ({p[1]})<br>
        ID: {p[0]}<br>
        Nr: {p[3]}<br>
        Puncte: {p[4]}<br>
        <a href='/edit/{p[0]}'>Modifică</a> |
        <a href='/delete/{p[0]}'>Șterge</a>
        <hr>
        """

    return html


@app.route("/add", methods=["GET", "POST"])
def add():
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
        return redirect("/")

    return """
    <h2>Adaugă Jucător</h2>
    <form method="post">
        Discord ID: <input name="discord_id"><br>
        Nume Discord: <input name="discord_name"><br>
        Nume în joc: <input name="ingame_name"><br>
        Nr înmatriculare: <input name="plate"><br>
        <button type="submit">Salvează</button>
    </form>
    """


@app.route("/edit/<int:discord_id>", methods=["GET", "POST"])
def edit(discord_id):
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
        return redirect("/")

    c.execute("SELECT * FROM players WHERE discord_id=?", (discord_id,))
    p = c.fetchone()
    conn.close()

    return f"""
    <h2>Modifică Jucător</h2>
    <form method="post">
        Nume Discord: <input name="discord_name" value="{p[1]}"><br>
        Nume în joc: <input name="ingame_name" value="{p[2]}"><br>
        Nr înmatriculare: <input name="plate" value="{p[3]}"><br>
        Puncte: <input name="points" value="{p[4]}"><br>
        <button type="submit">Salvează</button>
    </form>
    """


@app.route("/delete/<int:discord_id>")
def delete(discord_id):
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM players WHERE discord_id=?", (discord_id,))
    conn.commit()
    conn.close()
    return redirect("/")
