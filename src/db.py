import os
from flask_sqlalchemy import SQLAlchemy
from app import app

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
print( os.getenv("DATABASE_URL"))
db = SQLAlchemy(app)
