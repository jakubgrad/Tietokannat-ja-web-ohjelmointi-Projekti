from flask import redirect, render_template, request, session, Flask, flash, url_for
import json
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from PyPDF2 import PdfReader

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

import routes
