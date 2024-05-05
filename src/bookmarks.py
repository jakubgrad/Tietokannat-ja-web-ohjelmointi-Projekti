from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from db import db

def fetch_quick_bookmarks(user_id):
    db.session.commit()
    sql = """SELECT * FROM (
                 SELECT DISTINCT ON (pair_id) pair_id,bookmarks.id,counter1,counter2,last_read,name 
                 FROM bookmarks INNER JOIN pairs ON bookmarks.pair_id=pairs.id 
                 WHERE pair_id IN ( 
                     SELECT id FROM pairs WHERE user_id=2) 
                 ) AS subquery_alias
              ORDER BY last_read DESC;"""

    result = db.session.execute(text(sql), {"user_id":user_id})
    return result.fetchall()

def save_bookmark(pair_id,counter1, counter2):
    db.session.commit()
    sql = """INSERT INTO bookmarks (pair_id, counter1, counter2)
             VALUES (:pair_id,:counter1,:counter2);"""
    db.session.execute(text(sql), {"pair_id":pair_id,"counter1":counter1,
        "counter2":counter2 })
    db.session.commit()

def delete_bookmark_by_id(bookmark_id):
    sql = "DELETE FROM bookmarks WHERE id=:bookmark_id;"
    db.session.execute(text(sql), {"bookmark_id":bookmark_id })
    db.session.commit()

def delete_all_bookmarks_of_pair_by_pair_id(pair_id):
    sql = "DELETE FROM bookmarks WHERE pair_id=:pair_id;"
    db.session.execute(text(sql), {"pair_id":pair_id })
    db.session.commit()

def fetch_bookmarks_by_pair_id(pair_id):
    db.session.commit()
    sql = """SELECT id,pair_id,counter1,counter2,created_at,last_read
             FROM bookmarks WHERE pair_id=:pair_id"""
    result = db.session.execute(text(sql), {"pair_id":pair_id})
    return result.fetchall()

def fetch_bookmark_by_id(bookmark_id):
    db.session.commit()
    sql = """UPDATE bookmarks
             SET last_read = CURRENT_TIMESTAMP
             WHERE id=:bookmark_id;"""
    db.session.execute(text(sql), {"bookmark_id":bookmark_id})
    db.session.commit()

    sql = """SELECT id,pair_id,counter1,counter2,created_at,last_read
             FROM bookmarks WHERE id=:bookmark_id"""
    result = db.session.execute(text(sql), {"bookmark_id":bookmark_id})
    return result.fetchone()
