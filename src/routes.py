import db
import json
import books
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

@app.route("/create_pair",methods=["GET","POST"])
def pair(): 
    if request.method == "GET":
        print("user id " + str(users.user_id()))
        if users.user_id()!=0:
            return render_template("pair.html")
        else:
            return redirect("/")
    if request.method == "POST":
        return "TBD"
    
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

#def allowed_file(filename):
#    return '.' in filename and \
#           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/process_pdf", methods=['GET', 'POST'])
def process_pdf():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'pdf-file' not in request.files:
            return redirect("/upload")
        file = request.files['pdf-file']
        if file.filename == '':
            return redirect(request.url)
        #return books.process_pdf(file)
        if books.process_pdf(file):
            return redirect("/upload")
        else:
            #implement logic for bad pdfs/other files
            return redirect("/")
            

@app.route("/upload_success")
def upload_success():
    length = request.args('length')
    text = request.args('text')
    return render_template("upload_success.html", length=request.form["length"])
