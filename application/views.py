from application import app
from flask import render_template
from application.imap_gmail_script import main

@app.route('/')
@app.route('/index')
def index():
    data = main()
    return render_template('index.html',
                            time = data['Time'],
                            alt = data['Altitude'],
                            latitude = data['Latitude'],
                            longitude = data['Longitude']
                            )
                            