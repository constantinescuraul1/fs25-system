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
        points INTEGER DEFAULT 0
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS vehicles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        owner_id INTEGER,
        license_plate TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS attachments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        owner_id INTEGER,
        name TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS fields (
        field_id INTEGER PRIMARY KEY,
        hectares REAL
    )
    """)

    conn.commit()
    conn.close()

setup()

# ================= TEMPLATE =================

def layout(content):
    return f"""
    <style>
    body{{margin:0;font-family:Arial;background:#0f172a;color:white}}
    .sidebar{{width:220px;height:100vh;background:#1e293b;position:fixed;padding-top:20px}}
    .sidebar a{{display:block;color:white;padding:12px;text-decoration:none}}
    .sidebar a:hover{{background:#334155}}
    .content{{margin-left:240px;padding:20px}}
    .card{{background:#1e293b;padding:15px;margin-bottom:15px;border-radius:8px}}
    .btn{{padding:6px 12px;border-radius:6px;text-decoration:none;margin-right:5px}}
    .green{{background:#22c55e;color:white}}
    .blue{{background:#3b82f6;color:white}}
    .red{{background:#ef4444;color:white}}
    input{{padding:6px;margin:4px;border-radius:4px;border:none}}
    </style>

    <div class="sidebar">
        <a href="/panel">Dashboard</a>
        <a href="/players">Jucători</a>
        <a href="/vehicles">Utilaje</a>
        <a href="/attachments">Atașamente</a>
        <a href="/points">Puncte</a>
        <a href="/fields">Terenuri</a>
    </div>

    <div class="content">
        {content}
    </div>
    """

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

def check():
    if "admin" not in session:
        return False
    return True

# ================= DASHBOARD =================

@app.route("/panel")
def panel():
    if not check():
        return redirect("/")

    conn = connect()
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM players")
    players = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM vehicles")
    vehicles = c.fetchone()[0]

    conn.close()

    content = f"""
    <h1>Dashboard</h1>
    <div class="card">Total Jucători: {players}</div>
    <div class="card">Total Utilaje: {vehicles}</div>
    """

    return layout(content)

# ================= PLAYERS =================

@app.route("/players")
def players():
    if not check():
        return redirect("/")

    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM players")
    data = c.fetchall()
    conn.close()

    content = "<h1>Jucători</h1>"
    content += "<a class='btn green' href='/add_player'>Adaugă</a><br><br>"

    for p in data:
        content += f"""
        <div class="card">
        {p[2]} ({p[1]}) - {p[3]} puncte
        <br><br>
        <a class="btn blue" href="/edit_player/{p[0]}">Edit</a>
        <a class="btn red" href="/delete_player/{p[0]}">Șterge</a>
        </div>
        """

    return layout(content)

# ADD PLAYER

@app.route("/add_player", methods=["GET","POST"])
def add_player():
    if not check():
        return redirect("/")

    if request.method == "POST":
        conn = connect()
        c = conn.cursor()
        c.execute("INSERT INTO players VALUES (?,?,?,0)", (
            request.form["discord_id"],
            request.form["discord_name"],
            request.form["ingame_name"]
        ))
        conn.commit()
        conn.close()
        return redirect("/players")

    content = """
    <h1>Adaugă Jucător</h1>
    <form method="post">
    Discord ID:<br><input name="discord_id"><br>
    Nume Discord:<br><input name="discord_name"><br>
    Nume în joc:<br><input name="ingame_name"><br><br>
    <button class="btn green">Salvează</button>
    </form>
    """
    return layout(content)

# DELETE PLAYER

@app.route("/delete_player/<int:id>")
def delete_player(id):
    if not check():
        return redirect("/")

    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM players WHERE discord_id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/players")

# ================= START =================

if __name__ == "__main__":
    app.run()
