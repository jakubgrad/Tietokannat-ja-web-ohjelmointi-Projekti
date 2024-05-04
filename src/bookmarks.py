from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from db import db

def save_bookmark(pair_id,counter1, counter2):
    try:
        db.session.commit()
        sql = """INSERT INTO bookmarks (pair_id, counter1, counter2)
              VALUES (:pair_id,:counter1,:counter2);"""
        db.session.execute(text(sql), {"pair_id":pair_id,"counter1":counter1,
            "counter2":counter2 })
        db.session.commit()
    except SQLAlchemyError as e:
        print(f"Error for inserting new bookmark into bookmarks: {e}")
        return False
    return True

def delete_bookmark_by_id(bookmark_id):
    try:
        sql = "DELETE FROM bookmarks WHERE id=:bookmark_id;"
        db.session.execute(text(sql), {"bookmark_id":bookmark_id })
        db.session.commit()
    except SQLAlchemyError as e:
        print(f"Error for deleting bookmark of id {bookmark_id}: {e}")
        return False
    return True

def delete_all_bookmarks_of_pair_by_pair_id(pair_id):
    try:
        sql = "DELETE FROM bookmarks WHERE pair_id=:pair_id;"
        db.session.execute(text(sql), {"pair_id":pair_id })
        db.session.commit()
    except SQLAlchemyError as e:
        print(f"Error for deleting all bookmark of pair_id {pair_id}: {e}")
        return False
    return True

def fetch_bookmarks_by_pair_id(pair_id):
    try:
        print(pair_id, type(pair_id))
        sql = "SELECT * FROM bookmarks WHERE pair_id=:pair_id"
        result = db.session.execute(text(sql), {"pair_id":pair_id})
        db.session.commit()
        bookmarks = result.fetchall()
        print("bookmarks:{bookmarks}")
        return bookmarks
    except SQLAlchemyError as e:
        print(f"Error for query into bookmarks: {e}")
        return False
    return True

def fetch_bookmark_by_id(bookmark_id):
    try:
        print(bookmark_id, type(bookmark_id))
        sql = "SELECT * FROM bookmarks WHERE id=:bookmark_id"
        result = db.session.execute(text(sql), {"bookmark_id":bookmark_id})
        db.session.commit()
        bookmark = result.fetchone()
        print(f"fetched bookmark:{bookmark}")
        return bookmark
    except SQLAlchemyError as e:
        print(f"Error for fetch bookmark by id: {e}")
        return False
    return True
