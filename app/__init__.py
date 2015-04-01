from flask import Flask

app = Flask(__name__)
from app import views
from app.imap_gmail_script import main