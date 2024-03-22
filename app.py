from flask import Flask, flash, url_for
import json
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import os 
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.secret_key = os.getenv("SECRET_KEY")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
    return render_template("login.html", message_id=0)

@app.route("/login/<int:id>")
def login_with_id(id):
    return render_template("login.html", message_id=id)

@app.route("/pair")
def pair():
    if "username" in session:
    #if session["username"]:
        return render_template("pair.html", message_id=id)
    else:
        return redirect("/")

@app.route("/login_user",methods=["POST"])
def login_user():
    username = request.form["username"]
    password = request.form["password"]
    # TODO: check username and password
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()    
    if not user:
        # invalid username
        return redirect("/login/1")
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            #correct username and password
            session["username"] = username
            return redirect("/")
        else:
            return redirect("/login/2")
                #invalid password
        return redirect("/login")
    session["username"] = username
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
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
    hash_value = generate_password_hash(password)
    sql = "INSERT INTO users (username, password) VALUES (:username, :password) RETURNING id"
    result = db.session.execute(text(sql), {"username":username, "password":hash_value})
    user_id = result.fetchone()[0]
    db.session.commit()
    return redirect("/")

@app.route("/upload")
def upload():
    return render_template("upload.html")

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
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #would be nice to inform the user that it went through
            reader = PdfReader("uploads/"+filename)
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

    '''
    if 'pdf-file' not in request.files:
        return redirect("/")  # No file uploaded
    file=request.files["pdf-file"]
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('download_file', name=filename))
    return redirect("/")
    '''

