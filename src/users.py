from db import db
from flask import session, redirect 
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import text
import secrets

def login(username, password):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()    
    if not user:
        return False 
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            #correct username and password
            session["username"] = username
            session["user_id"] = user.id
            session["csrf_token"] = secrets.token_hex(16)
            return True 
        else:
            #invalid password
            return False 

def logout():
    del session["username"]
    del session["user_id"]
    return True 

def username_free(username):
    print("Checking if username_free")
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()    
    if user:
        return False 
    return True


def register(username, password):
    print("Checking if username_free in register")
    if not username_free(username):
        return False
    hash_value = generate_password_hash(password)
    print("GENERATED HASH VALUE")

    try:
        sql = "INSERT INTO users (username,password) VALUES (:username,:password)"
        db.session.execute(text(sql), {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)

def user_id():
    return session.get("user_id",0)

def user_session():
    return session.get("csrf_token",0)
