from flask import render_template, request, redirect, url_for
import users
import books
import pairs
import bookmarks
from app import app

def prevent_csrf():
    if users.user_session() != request.form["csrf_token"]:
        # pylint: disable=undefined-variable
        abort(403)

def fetch_quick_bookmarks():
    return bookmarks.fetch_quick_bookmarks(users.user_id())

@app.route("/")
def index():
    quick_bookmarks = fetch_quick_bookmarks()
    return render_template("index.html", quick_bookmarks=quick_bookmarks)

@app.route("/create_new_pair",methods=["GET","POST"])
def create_new_pair():
    quick_bookmarks = fetch_quick_bookmarks()
    errors = []
    if request.method == "GET":
        if users.user_id()!=0:
            return render_template("create_new_pair.html",
                books = books.fetch_all_for_user_id(users.user_id()),
                quick_bookmarks=quick_bookmarks)
        return redirect("/")
    if request.method == "POST":
        prevent_csrf()
        quick_bookmarks = fetch_quick_bookmarks()
        name = request.form["name"]
        book1_id = request.form["book1_id"]
        book2_id = request.form["book2_id"]
        if pairs.create_new_pair(name, users.user_id(), book1_id, book2_id):
            pair_id = pairs.find_id_of_pair_by_user_id_and_name(users.user_id(),name)
            if pair_id:
                return redirect("/read_pair/"+str(pair_id))
            errors.append("Couldn't create or view the pair")
            return render_template("view_pairs.html", errors=errors,
                quick_bookmarks=quick_bookmarks)

    return render_template("view_pairs.html", errors=errors, quick_bookmarks=quick_bookmarks)

@app.route("/view_pairs",methods=["GET"])
def view_pairs():
    quick_bookmarks = fetch_quick_bookmarks()
    if users.user_id()!=0:
        return render_template("view_pairs.html",
            pairs = pairs.fetch_all_for_user_id(users.user_id()),
            quick_bookmarks=quick_bookmarks)
    return redirect("/")

@app.route("/login",methods=["GET","POST"])
def login():
    if users.user_id():
        return redirect(url_for("index"))
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        errors = []
        if len(password) == 0:
            errors.append("No password given")
        if len(username) == 0:
            errors.append("No username given")
        if users.login(username, password):
            return redirect("/")
    errors.append("Failed to log in. Perhaps wrong username?")
    return render_template("login.html", errors=errors, username=username,password=password)

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if users.user_id():
        return redirect(url_for("index"))
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        errors = []
        if len(username) > 15:
            errors.append("Too long username")
        if len(password) > 50:
            errors.append("Too long password")
        if len(password) == 0:
            errors.append("No password given")
        if len(username) == 0:
            errors.append("No username given")
        if errors:
            return render_template("register.html", errors=errors,
                username=username,password=password)
        if users.register(username, password):
            return redirect("/")
    errors.append("Registration failed. Possibly the username is already taken.")
    return render_template("register.html", errors=errors,
        username=username,password=password)

@app.route("/view_uploads")
def view_uploads():
    quick_bookmarks = fetch_quick_bookmarks()
    return render_template("view_uploads.html",
        books = books.fetch_all_for_user_id(users.user_id()),
        quick_bookmarks=quick_bookmarks)

@app.route("/delete_book/<int:book_id>", methods=['GET', 'POST'])
def delete_book(book_id):
    quick_bookmarks = fetch_quick_bookmarks()
    errors = []
    if request.method == 'GET':
        return redirect(url_for("view_uploads"))
    if request.method == 'POST':
        if books.delete_book_by_id(book_id):
            return redirect(url_for("view_uploads"))
        pair = pairs.find_pair_that_references_book_id(book_id)
        if pair:
            return render_template("delete_entity.html", entity=pair, name="pair",
                message ="To delete this book you also need to delete this pair.",
                quick_bookmarks=quick_bookmarks)
    errors.append(f"Failed to delete book {book_id}, sorry.")
    return render_template("view_pairs.html",
        pairs = pairs.fetch_all_for_user_id(users.user_id()),  errors=errors,
        quick_bookmarks=quick_bookmarks)

@app.route("/delete_pair/<int:pair_id>", methods=['GET', 'POST'])
def delete_pair(pair_id):
    quick_bookmarks = fetch_quick_bookmarks()
    messages = []
    errors = []
    if request.method == 'GET':
        return redirect(url_for("view_pairs"))
    if request.method == 'POST':
        bookmarks.delete_all_bookmarks_of_pair_by_pair_id(pair_id)
        if pairs.delete_pair_by_id(pair_id):
            messages.append(f"Successfully deleted pair of id {pair_id}.")
            return render_template("view_pairs.html",
                pairs = pairs.fetch_all_for_user_id(users.user_id()),
                messages=messages, quick_bookmarks=quick_bookmarks)
    errors.append(f"Couldn't delete pair of id {pair_id}.")
    return render_template("view_pairs.html",
        pairs = pairs.fetch_all_for_user_id(users.user_id()))

@app.route("/delete_bookmark/<int:bookmark_id>", methods=['GET', 'POST'])
def delete_bookmark(bookmark_id):
    errors = []
    bookmark = bookmarks.fetch_bookmark_by_id(bookmark_id)
    pair_id = bookmark[1]

    if request.method == 'GET':
        return redirect(url_for("read_pair", pair_id=pair_id))
    if request.method == 'POST':
        if not bookmarks.delete_bookmark_by_id(bookmark_id):
            errors.append(f"Failed to delete bookmark {id}")
    return redirect(url_for("read_pair", pair_id=pair_id, errors=errors))

@app.route("/delete_all_bookmarks_of_pair/<int:pair_id>", methods=['GET', 'POST'])
def delete_all_bookmarks_of_pair(pair_id):
    errors = []
    if request.method == 'GET':
        return redirect(url_for("read_pair", pair_id=pair_id))
    if request.method == 'POST':
        if bookmarks.delete_all_bookmarks_of_pair_by_pair_id(pair_id):
            return redirect(url_for("read_pair", pair_id=pair_id))
    errors.append(f"Failed to delete bookmark {pair_id}")
    return redirect(url_for("read_pair", pair_id=pair_id, errors=errors))

@app.route("/process_pdf", methods=['GET', 'POST'])
def process_pdf():
    errors = []
    if request.method == 'POST':
        if 'pdf-file' not in request.files:
            errors.append("No file attached")
        file = request.files['pdf-file']
        if file.filename == '':
            errors.append("File doesn't have a name")
        title = request.form["title"]
        author = request.form["author"]
        language = request.form["language"]
        isbn = request.form["isbn"]
        if not title:
            errors.append("No title")
        if errors:
            return redirect(url_for("view_uploads", errors=errors))
        if books.process_pdf(file, title, author, language, isbn):
            return redirect("/view_uploads")
    errors.append("Error in processing your file, sorry!")
    return redirect(url_for("view_uploads", errors=errors))

# pylint: disable=unreachable
@app.route("/read_pair/<int:pair_id>",methods=["GET","POST"])
def read_pair(pair_id):
    errors = []
    if request.method == "GET":
        if not pairs.check_id_validity(pair_id,users.user_id()):
            errors.append("Pair not available")
            return redirect(url_for("view_uploads", errors=errors))
        pair = pairs.fetch_pair_by_id(pair_id)
        book1 = books.fetch_book_by_id(pair.book1_id)
        book2 = books.fetch_book_by_id(pair.book2_id)

        counter1=0
        counter2=0

        bookmarks_of_pair = bookmarks.fetch_bookmarks_by_pair_id(pair_id)
        #list could be produced by pair
        sentences1 = pairs.produce_sentences(book1, counter1)
        sentences2 = pairs.produce_sentences(book2, counter2)
        return render_template("read_pair.html",
            pair=pair, book1=book1, book2=book2,
            sentences1=sentences1,sentences2=sentences2, counter1=counter1,
            counter2=counter2, bookmarks_of_pair=bookmarks_of_pair)

    if request.method == "POST":
        prevent_csrf()
        if not pairs.check_id_validity(pair_id,users.user_id()):
            errors.append("Pair not available")
            return redirect(url_for("view_pairs", errors=errors))

        counter = int(request.form["counter"])
        counter1 = int(request.form["counter1"])
        counter2 = int(request.form["counter2"])

        pair = pairs.fetch_pair_by_id(pair_id)
        book1 = books.fetch_book_by_id(pair.book1_id)
        book2 = books.fetch_book_by_id(pair.book2_id)

        counter1 = pairs.validate_and_fix_counter(counter1, book1)
        counter2 = pairs.validate_and_fix_counter(counter2, book2)

        if request.form["form_purpose"] == "save_bookmark":
            print("saving bookmark success:",bookmarks.save_bookmark(pair_id, counter1, counter2))
            return redirect("/read_pair/"+str(pair_id))

        if request.form["form_purpose"] == "load_bookmark":
            print("bookmark selected")
            selected_bookmark_id = request.form["bookmark_id"]
            selected_bookmark = bookmarks.fetch_bookmark_by_id(selected_bookmark_id)
            if selected_bookmark:
                counter1 = selected_bookmark.counter1
                counter2 = selected_bookmark.counter2

        bookmarks_of_pair = bookmarks.fetch_bookmarks_by_pair_id(pair_id)

        sentences1 = pairs.produce_sentences(book1, counter1)
        sentences2 = pairs.produce_sentences(book2, counter2)

        return render_template("read_pair.html", pair=pair, book1=book1,
            book2=book2, counter=counter,
            sentences1=sentences1,sentences2=sentences2, counter1=counter1,
            counter2=counter2, bookmarks_of_pair=bookmarks_of_pair)

    return redirect(url_for("view_pairs", errors=errors))
