import json
import os
from PyPDF2 import PdfReader
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app import app, ALLOWED_EXTENSIONS
import users
from db import db


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def process_pdf(file, title, author, language, isbn):
    if file and allowed_file(file.filename):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        reader = PdfReader("../uploads/"+file.filename)
        # pylint: disable=no-member
        text_from_pdf = reader.pages[0].extract_text()
        print(f"text_from_pdf {text_from_pdf}")
        sentences = text_from_pdf.split(".")
        print(f"sentences {sentences}")
        result = []
        for sentence in sentences:
            words = sentence.split("\n")
            print(f"words: {words}")
            clean_words = [word.replace(" ", "") for word in words]
            print(f"clean words: {clean_words}")
            result.append(clean_words)
        print(f"result:{result}")
        json_array = json.dumps(result)
        print(f"json_array {json_array}")
        print(f'text: {text}')
        try:
            sql = """INSERT INTO books
                     (title, user_id, filename, language, author, isbn, json)
                     VALUES (:title, :user_id, :filename, :language, :author,
                     :isbn, :json);"""
            db.session.execute(text(sql), {"title": title, "user_id": users.user_id(),
                "filename": file.filename, "language": language, "author": author, "isbn": isbn,
                "json": json_array})
            db.session.commit()
        except SQLAlchemyError as e:
            print(f"Error processing PDF: {e}")
            print("SQL insert query into books failed!")
            return True
        return True
    return False


def fetch_all_for_user_id(user_id):
    sql = """SELECT id, title, user_id, filename, language, author, isbn, json
            FROM books WHERE user_id=:user_id"""
    result = db.session.execute(text(sql), {"user_id": user_id})
    return result.fetchall()

def fetch_book_by_id(book_id):
    sql = """SELECT id, title, user_id, filename, language, author, isbn, json
            FROM books WHERE id=:id"""
    result = db.session.execute(text(sql), {"id": book_id})
    if result:
        return result.fetchone()
    return False


def delete_book_by_id(book_id):
    sql = "DELETE FROM books WHERE id=:id;"
    try:
        db.session.execute(text(sql), {"id": book_id})
        db.session.commit()
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return False

    if fetch_book_by_id(id):
        return False
    return True
