from db import db
import users
from flask import session, redirect 
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import text
from app import app, ALLOWED_EXTENSIONS
import os
from PyPDF2 import PdfReader
import json

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def process_pdf(file, title, author, language, isbn):
    filename = file.filename
    if file and allowed_file(file.filename):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        reader = PdfReader("../uploads/"+filename)
        number_of_pages = len(reader.pages)
        page = reader.pages[0]
        text_from_pdf = page.extract_text()
        sentences = text_from_pdf.split(". ")
        json_array = json.dumps(sentences)
        print(json_array)
        print( f'Number of pages: {number_of_pages}, text: {text}')
        try:
            easy_json_array = {"title": "example glossary"}
            sql = "INSERT INTO books (title, user_id, filename, language, author, isbn, json) VALUES (:title, :user_id, :filename, :language, :author, :isbn, :json);"
            db.session.execute(text(sql), {"title":title, "user_id":users.user_id(), "filename":filename, "language":language, "author":author, "isbn":isbn, "json":json_array})
            db.session.commit()
        except Exception as e:
            print(f"Error processing PDF: {e}")
            print("SQL insert query into books failed!")
            return True 
        return True
    return False 


def fetch_all_for_user_id(user_id):
    sql = f"SELECT id, title, user_id, filename, language, author, isbn, json FROM books WHERE user_id=:user_id"
    result = db.session.execute(text(sql), {"user_id":user_id})
    return result.fetchall()    

def fetch_book_by_id(id):
    sql = f"SELECT id, title, user_id, filename, language, author, isbn, json FROM books WHERE id=:id"
    result = db.session.execute(text(sql), {"id":id})
    return result.fetchone()    

def logout():
    del session["username"]
    del session["user_id"]
    return True 

def register(username, password):
    hash_value = generate_password_hash(password)
    print("GENERATED HASH VALUE")
    try:
        sql = "INSERT INTO users (username,password) VALUES (:username,:password)"
        db.session.execute(text(sql), {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)

'''
def register():
    username = request.form["username"]
    password = request.form["password"]
    hash_value = generate_password_hash(password)
    sql = "INSERT INTO users (username, password) VALUES (:username, :password) RETURNING id"
    result = db.session.execute(text(sql), {"username":username, "password":hash_value})
    user_id = result.fetchone()[0]
    db.session.commit()
    return redirect("/")
'''
def user_id():
    print("session id "+session["username"])
    return session.get("user_id",0)
