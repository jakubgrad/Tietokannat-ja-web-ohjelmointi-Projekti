from db import db
from flask import session, redirect 
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import text

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
            return True 
        else:
            #invalid password
            return False 

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
