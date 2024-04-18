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



