from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy

UPLOAD_FOLDER = '../uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

import routes
