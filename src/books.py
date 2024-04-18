from db import db
import users
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
        print(f"text_from_pdf {text_from_pdf}" )
        sentences = text_from_pdf.split(".")
        print(f"sentences {sentences}" )
        result = []
        for sentence in sentences:
            words = sentence.split("\n")
            print(f"words: {words}")
            clean_words = [word.replace(" ", "") for word in words]
            print(f"clean words: {clean_words}")
            result.append(clean_words)
        print(f"result:{result}")
        json_array = json.dumps(result)
        print(f"json_array {json_array}" )
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
    if result:
        return result.fetchone()    
    return False

def delete_book_by_id(id):
    sql = "DELETE FROM books WHERE id=:id;"
    try:
        db.session.execute(text(sql), {"id":id})
        db.session.commit()
    except:
        return False

    if fetch_book_by_id(id):
        return False
    return True




