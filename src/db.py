from app import app
from flask_sqlalchemy import SQLAlchemy
import os

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
print( os.getenv("DATABASE_URL"))
db = SQLAlchemy(app)


