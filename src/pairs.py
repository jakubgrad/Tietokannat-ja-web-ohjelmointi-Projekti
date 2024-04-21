from db import db
from sqlalchemy import text
import json

def check_id_validity(pair_id, user_id):
    try:
        print(pair_id, type(pair_id))
        print(user_id, type(user_id))
        sql = "SELECT * FROM pairs WHERE id=:pair_id AND user_id=:user_id;"
        result = db.session.execute(text(sql), {"pair_id":pair_id, "user_id":user_id})
        db.session.commit()
        pair = result.fetchone() 
        print(pair)
        return pair
    except Exception as e:
        #print(f"Error for insert into pairs: {e}")
        return False 
    return True

def create_new_pair(name, user_id, book1_id, book2_id):
    try:
        sql = "INSERT INTO pairs (name, user_id, book1_id, book2_id) VALUES (:name, :user_id, :book1_id, :book2_id);"
        db.session.execute(text(sql), {"name":name, "user_id":user_id, "book1_id":book1_id,"book2_id":book2_id})
        db.session.commit()
    except Exception as e:
        #print(f"Error for insert into pairs: {e}")
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
    except Exception as e:
        #print(f"Error for insert into pairs: {e}")
        print("Query failed!")
    return False 

def find_pair_that_references_book_id(book_id):
    print(f"book_id:{book_id}")
    try:
        db.session.commit()
        sql = "SELECT id, user_id, name, book1_id, book2_id FROM pairs WHERE book1_id=:book1_id OR book2_id=:book2_id;"
        result = db.session.execute(text(sql), {"book1_id":int(book_id),"book2_id":int(book_id)})
        db.session.commit()
        pair = result.fetchone()    
        print(f"pair:{pair}")
        return pair
    except Exception as e:
        print(f"Finding pair that references book id failed because: {e}")
    return False 

def fetch_pair_by_id(id):
    sql = f"SELECT id, name, book1_id, book2_id FROM pairs WHERE id=:id"
    result = db.session.execute(text(sql), {"id":id})
    return result.fetchone()    

def fetch_all_for_user_id(user_id):
    sql = f"SELECT id, name, book1_id, book2_id FROM pairs WHERE user_id=:user_id"
    result = db.session.execute(text(sql), {"user_id":user_id})
    return result.fetchall()    

def delete_pair_by_id(id):
    sql = "DELETE FROM pairs WHERE id=:id;"
    try:
        db.session.execute(text(sql), {"id":id})
        db.session.commit()
    except:
        return False

    if fetch_pair_by_id(id):
        return False
    return True

def produce_sentences(book, counter):
    list = book.json[counter] + ["."]+ book.json[counter+1] + ["."]+book.json[counter+2]+["."]
    print("list: {list}")
    sentences = " ".join(list)
    print("sentences: {sentences}")
    return sentences

def validate_and_fix_counter(counter, book):
    SENTENCE_LENGTH = 3
    max_counter = len(book.json)-SENTENCE_LENGTH 
    if max_counter < counter:
        counter = max_counter
    if counter < 0:
        counter = 0
    return counter

