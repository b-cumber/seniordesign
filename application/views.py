from application import app
from flask import render_template
from flask import jsonify
from application.imap_gmail_script import main

@app.route('/')
@app.route('/index')
def index():
    #data = main()
    # return render_template('index.html', time = data['Time'], alt = data['Altitude'], latitude = data['Latitude'], longitude = data['Longitude'], sats = data['Satellites'], )
    return render_template('index.html')
                            
@app.route('/update/<int:msg>')
def update(msg):
    return jsonify(main(msg=msg))
    
                            