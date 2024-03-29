import db
import json
import books
import pairs
from PyPDF2 import PdfReader
import os
from app import app, ALLOWED_EXTENSIONS
from flask import render_template, request, redirect
import messages, users

@app.route("/")
def index():
    list = messages.get_list()
    return render_template("index.html", count=len(list), messages=list)

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/login/<int:id>")
def login_with_id(id):
    return render_template("login.html", message_id=id)

@app.route("/read_pair/<int:pair_id>",methods=["GET","POST"])
def read_pair(pair_id): 
    if request.method == "GET":
        if not pairs.check_id_validity(pair_id,users.user_id()):
            return "Pair not available"
        pair = pairs.fetch_pair_by_id(pair_id)
        book1 = books.fetch_book_by_id(pair.book1_id)
        book2 = books.fetch_book_by_id(pair.book2_id)
        return render_template("read_pair.html", pair=pair, book1=book1, book2=book2)

@app.route("/create_new_pair",methods=["GET","POST"])
def create_new_pair(): 
    if request.method == "GET":
        if users.user_id()!=0:
            return render_template("create_new_pair.html", books = books.fetch_all_for_user_id(users.user_id()))
        else:
            return redirect("/")
    if request.method == "POST":
        name = request.form["name"]
        book1_id = request.form["book1_id"]
        book2_id = request.form["book2_id"]
        if pairs.create_new_pair(name, users.user_id(), book1_id, book2_id):
            return redirect("/")
        else:
            return "Failed to create the pair"
    
@app.route("/view_pairs",methods=["GET","POST"])
def view_pairs(): 
    if request.method == "GET":
        if users.user_id()!=0:
            return render_template("view_pairs.html", pairs = pairs.fetch_all_for_user_id(users.user_id()))
        else:
            return redirect("/")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", message_id=0)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("login.html", message_id=1)

@app.route("/logout")
def logout():
    if users.logout():
        return redirect("/")

@app.route("/result", methods=["POST"])
def result():
    return render_template("result.html", name=request.form["name"])

@app.route("/send", methods=["POST"])
def send():
    content = request.form["content"]
    if messages.send(content):
        return redirect("/")
    else:
        return render_template("error.html", message="Viestin lähetys ei onnistunut")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        print("routes register begins")
        if users.register(username, password):
            return redirect("/")
        else:
            return redirect("/register")

@app.route("/upload")
def upload():
    return render_template("upload.html")

@app.route("/view_uploads")
def view_uploads():
    return render_template("view_uploads.html", books = books.fetch_all_for_user_id(users.user_id()))

@app.route("/process_pdf", methods=['GET', 'POST'])
def process_pdf():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'pdf-file' not in request.files:
            return redirect("/upload")
        file = request.files['pdf-file']
        if file.filename == '':
            return redirect(request.url)
        title = request.form["title"]
        author = request.form["author"]
        language = request.form["language"]
        isbn = request.form["isbn"]
        if books.process_pdf(file, title, author, language, isbn):
            return redirect("/")
        else:
           return "Error in processing the PDF" 
    return redirect("/")
            

@app.route("/upload_success")
def upload_success():
    length = request.args('length')
    text = request.args('text')
    return render_template("upload_success.html", length=request.form["length"])
