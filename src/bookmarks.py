from db import db
from sqlalchemy import text

def fetch_bookmarks_by_pair_id(pair_id):
    try:
        print(pair_id, type(pair_id))
        sql = "SELECT * FROM bookmarks WHERE pair_id=:pair_id"
        result = db.session.execute(text(sql), {"pair_id":pair_id})
        db.session.commit()
        bookmarks = result.fetchall() 
        print("bookmarks:{bookmarks}")
        return bookmarks
    except Exception as e:
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
    except Exception as e:
        print(f"Error for fetch bookmark by id: {e}")
        return False 
    return True

