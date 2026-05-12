from flask import Flask, render_template_string, request, redirect, session, jsonify
import sqlite3
from datetime import datetime
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE_DIR, "database.db")

app = Flask(__name__)
app.secret_key = "super_secret_key"



ADMIN_LOGIN = "admin"
ADMIN_PASSWORD = "12345"

SITE_HTML = """

<!DOCTYPE html>
<html lang="ru">
<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Atelier Nails</title>

<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">

<style>

*{
margin:0;
padding:0;
box-sizing:border-box;
}

html{
scroll-behavior:smooth;
}

body{
font-family:'Inter',sans-serif;
background:#0d0e11;
color:white;
overflow-x:hidden;
}

a{
text-decoration:none;
color:inherit;
}

.container{
width:min(1200px,92%);
margin:auto;
}

nav{
position:fixed;
top:0;
left:0;
width:100%;
padding:24px 0;
background:rgba(13,14,17,.7);
backdrop-filter:blur(20px);
border-bottom:1px solid rgba(255,255,255,.06);
z-index:1000;
}

.nav-inner{
display:flex;
justify-content:space-between;
align-items:center;
}

.logo{
font-size:14px;
letter-spacing:4px;
}

.nav-btn{
padding:14px 22px;
border-radius:999px;
background:white;
color:black;
font-size:14px;
transition:.3s;
}

.nav-btn:hover{
transform:translateY(-4px);
}

.hero{
min-height:100vh;
display:flex;
align-items:center;
padding-top:120px;
}

.hero-grid{
display:grid;
grid-template-columns:1fr 1fr;
gap:80px;
align-items:center;
}

.hero h1{
font-size:110px;
line-height:.9;
font-weight:500;
letter-spacing:-6px;
margin-bottom:30px;
}

.hero p{
color:rgba(255,255,255,.58);
line-height:1.9;
margin-bottom:40px;
max-width:500px;
}

.hero-buttons{
display:flex;
gap:16px;
flex-wrap:wrap;
}

.btn{
padding:18px 28px;
border-radius:999px;
transition:.35s;
display:inline-flex;
align-items:center;
justify-content:center;
}

.btn-dark{
background:white;
color:black;
}

.btn-light{
background:rgba(255,255,255,.05);
border:1px solid rgba(255,255,255,.08);
}

.btn:hover{
transform:translateY(-5px);
}

.hero-card{
height:760px;
border-radius:40px;
overflow:hidden;
position:relative;
}

.hero-card img{
width:100%;
height:100%;
object-fit:cover;
}

.overlay{
position:absolute;
inset:0;
background:linear-gradient(
transparent 40%,
rgba(0,0,0,.82)
);
display:flex;
align-items:flex-end;
padding:40px;
}

.overlay h2{
font-size:44px;
line-height:.95;
margin-bottom:12px;
}

.overlay p{
color:rgba(255,255,255,.6);
}

section{
padding:140px 0;
}

.section-title{
margin-bottom:60px;
}

.section-title h2{
font-size:76px;
line-height:.92;
letter-spacing:-4px;
margin-bottom:20px;
font-weight:500;
}

.section-title p{
max-width:680px;
line-height:1.9;
color:rgba(255,255,255,.58);
}

.grid{
display:grid;
grid-template-columns:repeat(auto-fit,minmax(260px,1fr));
gap:22px;
}

.card{
padding:34px;
border-radius:30px;
background:rgba(255,255,255,.03);
border:1px solid rgba(255,255,255,.06);
transition:.35s;
}

.card:hover{
transform:translateY(-10px);
}

.card h3{
font-size:30px;
margin-bottom:18px;
font-weight:500;
}

.card p{
color:rgba(255,255,255,.58);
line-height:1.8;
margin-bottom:28px;
}

.price{
font-size:34px;
}

.gallery{
display:grid;
grid-template-columns:1fr 1fr 1fr;
gap:20px;
}

.gallery img{
width:100%;
height:500px;
object-fit:cover;
border-radius:28px;
transition:.4s;
}

.gallery img:hover{
transform:translateY(-8px);
}

.review{
padding:30px;
border-radius:28px;
background:rgba(255,255,255,.03);
border:1px solid rgba(255,255,255,.06);
margin-bottom:20px;
}

.review h3{
margin-bottom:14px;
font-size:24px;
}

.review p{
color:rgba(255,255,255,.58);
line-height:1.8;
margin-bottom:14px;
}

.review small{
opacity:.35;
}

.form-box{
margin-top:50px;
padding:40px;
border-radius:34px;
background:rgba(255,255,255,.03);
border:1px solid rgba(255,255,255,.06);
}

.input{
width:100%;
padding:18px;
border:none;
outline:none;
border-radius:18px;
background:rgba(255,255,255,.05);
color:white;
margin-bottom:16px;
font-family:inherit;
}

textarea{
resize:none;
height:140px;
}

.submit-btn{
padding:18px 26px;
border:none;
border-radius:999px;
background:white;
color:black;
cursor:pointer;
font-size:15px;
transition:.3s;
}

.submit-btn:hover{
transform:translateY(-4px);
}

.route{
padding:60px;
border-radius:40px;
background:rgba(255,255,255,.03);
border:1px solid rgba(255,255,255,.06);
display:flex;
justify-content:space-between;
align-items:center;
gap:40px;
}

.route h2{
font-size:70px;
line-height:.92;
margin-bottom:20px;
letter-spacing:-4px;
font-weight:500;
}

.route p{
color:rgba(255,255,255,.58);
line-height:1.9;
max-width:520px;
}

footer{
padding:50px 0;
text-align:center;
color:rgba(255,255,255,.35);
}

.toast{
position:fixed;
bottom:30px;
left:50%;
transform:translateX(-50%) translateY(120px);
background:rgba(255,255,255,.08);
backdrop-filter:blur(20px);
border:1px solid rgba(255,255,255,.08);
padding:18px 26px;
border-radius:999px;
color:white;
font-size:14px;
z-index:99999;
opacity:0;
transition:.45s cubic-bezier(.22,1,.36,1);
}

.toast.show{
opacity:1;
transform:translateX(-50%) translateY(0);
}

@media(max-width:980px){

.hero-grid,
.gallery{
grid-template-columns:1fr;
}

.hero h1{
font-size:72px;
}

.hero-card{
height:540px;
}

.route{
flex-direction:column;
align-items:flex-start;
padding:40px 24px;
}

.route h2,
.section-title h2{
font-size:52px;
}

section{
padding:100px 0;
}

}

</style>

</head>

<body>

<nav>

<div class="container nav-inner">

<div class="logo">
ATELIER NAILS
</div>

<a 
href="https://t.me/example"
target="_blank"
class="nav-btn"
>
Telegram
</a>

</div>

</nav>

<section class="hero">

<div class="container">

<div class="hero-grid">

<div>

<h1>
Quiet<br>
luxury
</h1>

<p>
Минималистичный nail-сервис
с эстетикой дорогого спокойствия,
чистых форм
и premium-подачи.
</p>

<div class="hero-buttons">

<a 
href="https://t.me/example"
target="_blank"
class="btn btn-dark"
>
Запись
</a>

<a 
href="https://2gis.ru/moscow/routeSearch/rsType/car/to/37.617761,55.755773"
target="_blank"
class="btn btn-light"
>
Маршрут
</a>

</div>

</div>

<div class="hero-card">

<img src="https://images.unsplash.com/photo-1607779097040-26e80aa78e66?q=80&w=1400&auto=format&fit=crop">

<div class="overlay">

<div>

<h2>
Minimal<br>
Nails
</h2>

<p>
Москва · Петровка 21
</p>

</div>

</div>

</div>

</div>

</div>

</section>

<section>

<div class="container">

<div class="section-title">

<h2>
Services
</h2>

<p>
Основные услуги и эстетика premium nail-сервиса.
</p>

</div>

<div class="grid">

<div class="card">
<h3>Маникюр</h3>
<p>Аккуратная обработка и уход.</p>
<div class="price">2500 ₽</div>
</div>

<div class="card">
<h3>Гель-лак</h3>
<p>Стойкое покрытие premium материалами.</p>
<div class="price">3200 ₽</div>
</div>

<div class="card">
<h3>Френч</h3>
<p>Минималистичный дизайн и чистые линии.</p>
<div class="price">3900 ₽</div>
</div>

<div class="card">
<h3>Наращивание</h3>
<p>Эстетичная форма и прочность.</p>
<div class="price">4900 ₽</div>
</div>

</div>

</div>

</section>

<section>

<div class="container">

<div class="section-title">

<h2>
Portfolio
</h2>

<p>
Работы студии.
</p>

</div>

<div class="gallery">

<img src="https://images.unsplash.com/photo-1519014816548-bf5fe059798b?q=80&w=1400&auto=format&fit=crop">

<img src="https://images.unsplash.com/photo-1632345031435-8727f6897d53?q=80&w=1400&auto=format&fit=crop">

<img src="https://images.unsplash.com/photo-1519014816548-bf5fe059798b?q=80&w=1400&auto=format&fit=crop">

</div>

</div>

</section>

<section>

<div class="container">

<div class="section-title">

<h2>
Reviews
</h2>

<p>
Отзывы клиентов после модерации.
</p>

</div>

<div id="reviews"></div>

<div class="form-box">

<input
type="text"
class="input"
id="name"
placeholder="Ваше имя"
>

<textarea
class="input"
id="text"
placeholder="Ваш отзыв"
></textarea>

<button
class="submit-btn"
onclick="sendReview()"
>
Отправить отзыв
</button>

</div>

</div>

</section>

<section>

<div class="container">

<div class="route">

<div>

<h2>
Petrovka 21
</h2>

<p>
Маршрут до студии
можно открыть
в один клик через 2GIS.
</p>

</div>

<div class="hero-buttons">

<a
href="https://2gis.ru/moscow/routeSearch/rsType/car/to/37.617761,55.755773"
target="_blank"
class="btn btn-dark"
>
2GIS
</a>

<a
href="https://t.me/example"
target="_blank"
class="btn btn-light"
>
Telegram
</a>

</div>

</div>

</div>

</section>

<footer>

<div class="container">

© 2026 Atelier Nails

</div>

</footer>

<div class="toast" id="toast">
Отзыв отправлен на модерацию
</div>

<script>

async function loadReviews(){

const res = await fetch('/api/reviews');
const data = await res.json();

const reviews = document.getElementById('reviews');

reviews.innerHTML = '';

data.forEach(review=>{

reviews.innerHTML += `
<div class="review">
<h3>${review.name}</h3>
<p>${review.text}</p>
<small>${review.date}</small>
</div>
`;

});

}

async function sendReview(){

const name = document.getElementById('name').value;
const text = document.getElementById('text').value;

if(!name || !text){
return;
}

await fetch('/api/add-review',{

method:'POST',

headers:{
'Content-Type':'application/json'
},

body:JSON.stringify({
name,
text
})

});

document.getElementById('name').value = '';
document.getElementById('text').value = '';

const toast = document.getElementById('toast');

toast.classList.add('show');

setTimeout(()=>{

toast.classList.remove('show');

},2500);

}

loadReviews();

</script>

</body>
</html>

"""

ADMIN_HTML = """

<!DOCTYPE html>
<html lang="ru">
<head>

<meta charset="UTF-8">

<title>Admin</title>

<style>

body{
background:#111;
color:white;
font-family:Arial;
padding:40px;
}

.review{
padding:25px;
margin-bottom:20px;
border-radius:20px;
background:#1b1b1b;
}

button{
padding:12px 18px;
border:none;
border-radius:999px;
cursor:pointer;
margin-right:10px;
}

.approve{
background:#4caf50;
color:white;
}

.delete{
background:#ff4d4d;
color:white;
}

</style>

</head>

<body>

<h1>
Админ панель
</h1>

{% for review in reviews %}

<div class="review">

<h2>{{ review['name'] }}</h2>

<p>{{ review['text'] }}</p>

<small>{{ review['date'] }}</small>

<br><br>

{% if review['approved'] == 0 %}

<a href="/approve/{{ review['id'] }}">
<button class="approve">
Одобрить
</button>
</a>

{% endif %}

<a href="/delete/{{ review['id'] }}">
<button class="delete">
Удалить
</button>
</a>

</div>

{% endfor %}

</body>
</html>

"""

LOGIN_HTML = """

<!DOCTYPE html>
<html lang="ru">
<head>

<meta charset="UTF-8">

<title>Login</title>

<style>

body{
background:#111;
display:flex;
justify-content:center;
align-items:center;
height:100vh;
font-family:Arial;
}

form{
background:#1b1b1b;
padding:40px;
border-radius:24px;
width:320px;
}

input{
width:100%;
padding:16px;
margin-bottom:14px;
border:none;
border-radius:14px;
background:#2a2a2a;
color:white;
}

button{
width:100%;
padding:16px;
border:none;
border-radius:999px;
background:white;
cursor:pointer;
}

</style>

</head>

<body>

<form method="POST">

<input
name="login"
placeholder="Логин"
>

<input
type="password"
name="password"
placeholder="Пароль"
>

<button>
Войти
</button>

</form>

</body>
</html>

"""

def init_db():

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""

    CREATE TABLE IF NOT EXISTS reviews(

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        text TEXT,
        date TEXT,
        approved INTEGER DEFAULT 0

    )

    """)

    conn.commit()
    conn.close()

@app.route("/")
def home():
    return render_template_string(SITE_HTML)

@app.route("/api/reviews")
def reviews():

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    cur.execute("""
    SELECT * FROM reviews
    WHERE approved = 1
    ORDER BY id DESC
    """)

    data = [dict(row) for row in cur.fetchall()]

    conn.close()

    return jsonify(data)

@app.route("/api/add-review", methods=["POST"])
def add_review():

    data = request.json

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO reviews(name, text, date)
    VALUES (?, ?, ?)
    """, (

        data["name"],
        data["text"],
        datetime.now().strftime("%d.%m.%Y %H:%M")

    ))

    conn.commit()
    conn.close()

    return jsonify({"success": True})

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        login = request.form["login"]
        password = request.form["password"]

        if login == ADMIN_LOGIN and password == ADMIN_PASSWORD:

            session["admin"] = True

            return redirect("/admin")

    return render_template_string(LOGIN_HTML)

@app.route("/admin")
def admin():

    if not session.get("admin"):
        return redirect("/login")

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    cur.execute("""
    SELECT * FROM reviews
    ORDER BY id DESC
    """)

    reviews = cur.fetchall()

    conn.close()

    return render_template_string(
        ADMIN_HTML,
        reviews=reviews
    )

@app.route("/approve/<int:id>")
def approve(id):

    if not session.get("admin"):
        return redirect("/login")

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    UPDATE reviews
    SET approved = 1
    WHERE id = ?
    """, (id,))

    conn.commit()
    conn.close()

    return redirect("/admin")

@app.route("/delete/<int:id>")
def delete(id):

    if not session.get("admin"):
        return redirect("/login")

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    DELETE FROM reviews
    WHERE id = ?
    """, (id,))

    conn.commit()
    conn.close()

    return redirect("/admin")

if __name__ == "__main__":

    init_db()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )