import db
import json
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

@app.route("/pair",methods=["GET","POST"])
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

'''
@app.route("/send", methods=["POST"])
def send():
    content = request.form["content"]
    sql = "INSERT INTO messages (content) VALUES (:content)"
    db.session.execute(text(sql), {"content":content})
    db.session.commit()
    return redirect("/")
'''

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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/process_pdf", methods=['GET', 'POST'])
def process_pdf():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'pdf-file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['pdf-file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            #filename = secure_filename(file.filename)
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #would be nice to inform the user that it went through
            reader = PdfReader("../uploads/"+filename)
            number_of_pages = len(reader.pages)
            page = reader.pages[0]
            text = page.extract_text()
            sentences = text.split(". ")
            json_array = json.dumps(sentences)
            return json_array
            return f'Number of pages: {number_of_pages}, text: {text}'
            #return redirect(url_for('upload_success', length=number_of_pages, text='text'))
            #return redirect("/")
    return redirect("/")

@app.route("/upload_success")
def upload_success():
    length = request.args('length')
    text = request.args('text')
    return render_template("upload_success.html", length=request.form["length"])
