from flask import Flask, render_template_string

app = Flask(__name__)

# ================= LAYOUT TEMPLATE =================

layout = """
<!doctype html>
<html lang="ro">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">

<style>
body {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
}

.sidebar {
    height: 100vh;
    background: #111827;
    padding-top: 20px;
}

.sidebar a {
    color: #cbd5e1;
    display: block;
    padding: 12px 20px;
    text-decoration: none;
}

.sidebar a:hover {
    background: #1f2937;
    color: white;
}

.card-custom {
    background: #1e293b;
    border: none;
    border-radius: 12px;
}

.stat-number {
    font-size: 28px;
    font-weight: bold;
}

.badge-active {
    background: #22c55e;
}
</style>

</head>
<body>

<div class="container-fluid">
<div class="row">

<div class="col-2 sidebar">
    <h4 class="text-center text-white mb-4">FS25 Control</h4>
    <a href="/">🏠 Dashboard</a>
    <a href="#">👤 Jucători</a>
    <a href="#">🚜 Utilaje</a>
    <a href="#">🔧 Atașamente</a>
    <a href="#">🌾 Terenuri</a>
    <a href="#">🏭 Fabrici</a>
    <a href="#">🐄 Animale</a>
    <a href="#">📊 Reguli Puncte</a>
    <a href="#">⏳ Activități Pending</a>
    <a href="#">⚠ Penalizări</a>
</div>

<div class="col-10 p-4">

<h2 class="mb-4">Dashboard</h2>

<div class="row mb-4">
    <div class="col-md-3">
        <div class="card card-custom p-3 text-center">
            <div class="stat-number">12</div>
            <div>Jucători Activi</div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card card-custom p-3 text-center">
            <div class="stat-number">34</div>
            <div>Utilaje Personale</div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card card-custom p-3 text-center">
            <div class="stat-number">5</div>
            <div>Activități Pending</div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card card-custom p-3 text-center">
            <div class="stat-number">12,450</div>
            <div>Total Puncte</div>
        </div>
    </div>
</div>

<div class="card card-custom p-4">
<h4>Top 5 Jucători</h4>
<table class="table table-dark table-hover mt-3">
<thead>
<tr>
<th>#</th>
<th>Nume</th>
<th>Puncte</th>
<th>Status</th>
</tr>
</thead>
<tbody>
<tr>
<td>1</td>
<td>Raul</td>
<td>2450</td>
<td><span class="badge badge-active">Activ</span></td>
</tr>
<tr>
<td>2</td>
<td>Denis</td>
<td>2100</td>
<td><span class="badge badge-active">Activ</span></td>
</tr>
</tbody>
</table>
</div>

</div>
</div>
</div>

</body>
</html>
"""

# ================= ROUTE =================

@app.route("/")
def dashboard():
    return render_template_string(layout)

if __name__ == "__main__":
    app.run()
