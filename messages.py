from db import db
from sqlalchemy import text
import users

def get_list():
    #sql = "SELECT M.content, U.username, M.sent_at FROM messages M, users U WHERE M.user_id=U.id ORDER BY M.id"
    result = db.session.execute(text("SELECT content FROM messages"))
    return result.fetchall()

def send(content):
    sql = "INSERT INTO messages (content) VALUES (:content)"
    db.session.execute(text(sql), {"content":content})
    db.session.commit()
    return True 

