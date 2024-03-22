from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

@app.route("/")
def index():
    result = db.session.execute(text("SELECT content FROM messages"))
    messages = result.fetchall()
    return render_template("index.html", count=len(messages), messages=messages) 

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/registration")
def registration():
    return render_template("registration.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login_user",methods=["POST"])
def login_user():
    username = request.form["username"]
    password = request.form["password"]
    # TODO: check username and password
    session["username"] = username
    return redirect("/")

@app.route("/result", methods=["POST"])
def result():
    return render_template("result.html", name=request.form["name"])

@app.route("/send", methods=["POST"])
def send():
    content = request.form["content"]
    sql = "INSERT INTO messages (content) VALUES (:content)"
    db.session.execute(text(sql), {"content":content})
    db.session.commit()
    return redirect("/")

@app.route("/create_user", methods=["POST"])
def create():
    username = request.form["username"]
    password = request.form["password"]
    sql = "INSERT INTO users (username, password) VALUES (:username, :password) RETURNING id"
    result = db.session.execute(text(sql), {"username":username, "password":password})
    user_id = result.fetchone()[0]
    db.session.commit()
    return redirect("/")
