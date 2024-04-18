import db
import json
import books
import pairs
from PyPDF2 import PdfReader
import os
from app import app, ALLOWED_EXTENSIONS
from flask import render_template, request, redirect
import users

@app.route("/")
def index():
    books_of_user = books.fetch_all_for_user_id(users.user_id())
    if books_of_user:
        dimmed_pair_options = False
    else:
        dimmed_pair_options = True
    return render_template("index.html",dimmed_pair_options=dimmed_pair_options)


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
            return render_template("error.html", message="Pair not available")
        pair = pairs.fetch_pair_by_id(pair_id)
        book1 = books.fetch_book_by_id(pair.book1_id)
        book2 = books.fetch_book_by_id(pair.book2_id)

        counter1=0
        counter2=0

        SENTENCE_LENGTH = 3
        max_counter1 = len(book1.json)-SENTENCE_LENGTH 
        max_counter2 = len(book2.json)-SENTENCE_LENGTH 

        if max_counter1 < counter1:
            counter1 = max_counter1
        if max_counter2 < counter2:
            counter2 = max_counter2

        if counter1 < 0:
            counter1 = 0
        if counter2 < 0:
            counter2 = 0

        list1 = book1.json[counter1] + ["."]+ book1.json[counter1+1] + ["."]+book1.json[counter1+2]+["."]
        print("list1: {list1}")
        sentences1 = " ".join(list1)
        print("sentences1: {sentences1}")

        list2 = book2.json[counter2] + ["."]+ book2.json[counter2+1] + ["."]+book2.json[counter2+2]+["."]
        print("list2: {list2}")
        sentences2 = " ".join(list2)
        print("sentences2: {sentences2}")
        #counters = (counter1, counter2)

        return render_template("read_pair.html", pair=pair, book1=book1, book2=book2, result=result,
            sentences1=sentences1,sentences2=sentences2, counter1=counter1, counter2=counter2)
        return render_template("read_pair.html", pair=pair, book1=book1, book2=book2, counter1=0,counter2=0)
    if request.method == "POST":
        if not pairs.check_id_validity(pair_id,users.user_id()):
            return render_template("error.html", message="Pair not available")
        counter = int(request.form["counter"])
        counter1 = int(request.form["counter1"])
        counter2 = int(request.form["counter2"])

        print(f"counter1:{counter1}")
        print(f"counter2:{counter2}")
        pair = pairs.fetch_pair_by_id(pair_id)
        book1 = books.fetch_book_by_id(pair.book1_id)
        book2 = books.fetch_book_by_id(pair.book2_id)

        SENTENCE_LENGTH = 3
        max_counter1 = len(book1.json)-SENTENCE_LENGTH 
        max_counter2 = len(book2.json)-SENTENCE_LENGTH 

        if max_counter1 < counter1:
            counter1 = max_counter1
        if max_counter2 < counter2:
            counter2 = max_counter2

        if counter1 < 0:
            counter1 = 0
        if counter2 < 0:
            counter2 = 0

        list1 = book1.json[counter1] + ["."]+ book1.json[counter1+1] + ["."]+book1.json[counter1+2]+["."]
        print("list1: {list1}")
        sentences1 = " ".join(list1)
        print("sentences1: {sentences1}")

        list2 = book2.json[counter2] + ["."]+ book2.json[counter2+1] + ["."]+book2.json[counter2+2]+["."]
        print("list2: {list2}")
        sentences2 = " ".join(list2)
        print("sentences2: {sentences2}")
        #counters = (counter1, counter2)

        return render_template("read_pair.html", pair=pair, book1=book1, book2=book2, counter=counter, result=result,
            sentences1=sentences1,sentences2=sentences2, counter1=counter1, counter2=counter2)

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
            id = pairs.find_id_of_pair_by_user_id_and_name(users.user_id(),name)
            if id:
                return redirect("/read_pair/"+str(id))
            else:
                return render_template("error.html", message="Couldn't view the pair immediately")
    
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
        if len(username) > 100:
            return render_template("error.html", error="Too long username")
        if len(password) > 5000:
            return render_template("error.html", error="Too long password")

        if users.register(username, password):
            return redirect("/")
        else:
            return render_template("error.html", error="Registration failed. Possibly the username is already taken.")

@app.route("/upload")
def upload():
    return render_template("upload.html")

@app.route("/view_uploads")
def view_uploads():
    return render_template("view_uploads.html", books = books.fetch_all_for_user_id(users.user_id()))

@app.route("/delete_book/<int:id>", methods=['GET', 'POST'])
def delete_book(id):
    if request.method == 'GET':
        return render_template("error.html", message="Delete API")
    if request.method == 'POST':
        if books.delete_book_by_id(id):
            return render_template("error.html", message ="Successfully deleted")
        return render_template("error.html", message =f"Failed to delete book {id}. Perhaps it's included in a pair.") 

@app.route("/delete_pair/<int:id>", methods=['GET', 'POST'])
def delete_pair(id):
    if request.method == 'GET':
        return render_template("error.html", message="Delete API")
    if request.method == 'POST':
        if pairs.delete_pair_by_id(id):
            return render_template("error.html", message ="Successfully deleted")
        return render_template("error.html", message =f"Failed to delete pair {id}") 

@app.route("/process_pdf", methods=['GET', 'POST'])
def process_pdf():
    if request.method == 'POST':
        if users.user_session() != request.form["csrf_token"]:
            return render_template("error.html", message="CSRF attack detected")
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
            return redirect("/view_uploads")
        else:
            return render_template("error.html", message="Error in processing the PDF")

    return redirect("/")
            

@app.route("/upload_success")
def upload_success():
    length = request.args('length')
    text = request.args('text')
    return render_template("upload_success.html", length=request.form["length"])
