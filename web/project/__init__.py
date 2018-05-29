#################
##        imports 

import os
import json
import time
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

################
##        config 


app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('local_settings.py', silent=True)
app.secret_key = 'SECRET_KEY'

Bootstrap(app)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)





@app.route('/')
def index():
    return render_template("index.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/map', methods=['GET', 'POST'])
def map():
    
    userinput = request.form['address'].split('|')
    print('userinput = {}'.format(userinput))
    
    work_address = userinput[0]
    lowprice, highprice = userinput[-2], userinput[-1]
    print(work_address, lowprice, highprice)


    records = commutetime.comtime(work_address, lowprice, highprice)
    print(records)
    if records == -1:
        flash('invalid input!', 'warning')
        return redirect(url_for('index'))
    house_locations = [[record[5], record[6]] for record in records]
    print(house_locations)
    work_location = [records[0][2], records[0][3]]

    return render_template('map.html', work_location=work_location, house_locations=house_locations, rows=records)

@app.route("/about")
def about():
    return render_template('about.html')
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)