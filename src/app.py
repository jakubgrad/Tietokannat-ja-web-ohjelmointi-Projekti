import os
from flask import Flask

UPLOAD_FOLDER = '../uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# pylint: disable=unused-import
# pylint: disable=wrong-import-position
import routes
