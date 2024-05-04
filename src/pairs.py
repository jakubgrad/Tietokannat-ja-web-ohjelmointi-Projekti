from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from db import db

def check_id_validity(pair_id, user_id):
    try:
        print(pair_id, type(pair_id))
        print(user_id, type(user_id))
        sql = "SELECT id FROM pairs WHERE id=:pair_id AND user_id=:user_id;"
        result = db.session.execute(text(sql), {"pair_id":pair_id, "user_id":user_id})
        db.session.commit()
        pair = result.fetchone()
        print(pair)
        return pair
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return False
    return True

def create_new_pair(name, user_id, book1_id, book2_id):
    try:
        sql = """INSERT INTO pairs (name, user_id, book1_id, book2_id)
                 VALUES (:name, :user_id, :book1_id, :book2_id);"""
        db.session.execute(text(sql), {"name":name, "user_id":user_id,
            "book1_id":book1_id,"book2_id":book2_id})
        db.session.commit()
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return False
    return True

def find_id_of_pair_by_user_id_and_name(user_id,name):
    try:
        print(f"user_id:{user_id}")
        print(f"name:{name}")
        sql = "SELECT id FROM pairs WHERE user_id=:user_id AND name=:name;"
        result = db.session.execute(text(sql), {"user_id":user_id,"name":name})
        pair = result.fetchone()
        print(f"pair:{pair}")
        return pair[0]
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        print("Query failed!")
    return False

def find_pair_that_references_book_id(book_id):
    print(f"book_id:{book_id}")
    try:
        db.session.commit()
        sql = """SELECT id, user_id, name, book1_id, book2_id FROM pairs
                 WHERE book1_id=:book1_id OR book2_id=:book2_id;"""
        result = db.session.execute(text(sql), {"book1_id":int(book_id),"book2_id":int(book_id)})
        db.session.commit()
        pair = result.fetchone()
        print(f"pair:{pair}")
        return pair
    except SQLAlchemyError as e:
        print(f"Finding pair that references book id failed because: {e}")
    return False

def fetch_pair_by_id(pair_id):
    sql = """SELECT id, name, book1_id, book2_id FROM pairs WHERE id=:id"""
    result = db.session.execute(text(sql), {"id":pair_id})
    return result.fetchone()

def fetch_all_for_user_id(user_id):
    sql = """SELECT id, name, book1_id, book2_id FROM pairs WHERE user_id=:user_id"""
    result = db.session.execute(text(sql), {"user_id":user_id})
    return result.fetchall()

def delete_pair_by_id(pair_id):
    sql = "DELETE FROM pairs WHERE id=:id;"
    try:
        db.session.execute(text(sql), {"id":pair_id})
        db.session.commit()
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return False

    if fetch_pair_by_id(id):
        return False
    return True

def produce_sentences(book, counter):
    words = book.json[counter] + ["."]+ book.json[counter+1] + ["."]+book.json[counter+2]+["."]
    sentences = " ".join(words)
    return sentences

def validate_and_fix_counter(counter, book):
    sentence_length = 3
    max_counter = len(book.json)-sentence_length
    counter = min(counter, max_counter)
    counter = min(counter, 0)
    return counter
