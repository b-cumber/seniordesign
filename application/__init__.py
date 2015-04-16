from flask import Flask

app = Flask(__name__)
from application import views
from application.imap_gmail_script import main
from application.gen_gauge import gauge_maker
