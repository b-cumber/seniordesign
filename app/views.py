from app import app
from flask import render_template
from app.imap_gmail_script import main

@app.route('/')
@app.route('/index')
def index():
    data = main()
    return render_template('index.html',
                            alt = data['Altitude'],
                            latitude = data['Latitude'],
                            longitude = data['Longitude']
                            )
                            