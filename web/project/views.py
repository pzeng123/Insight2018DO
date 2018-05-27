#import sys
#sys.path.append("/home/peng/Insight2018DO/web/")
#print(sys.path)
from flask import Flask, render_template, redirect, url_for, request

import scraper
import commutetime
import json

from project import app, db

from models import Listing, Commutetime


db.create_all()

scraper.do_scrape()

print('scraper finish')

@app.route('/')
def index():

    return render_template('index.html')
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
	
@app.route('/map', methods=['GET', 'POST'])
def map():
    userinput = request.form['address'].split('|')
    print('userinput = {}'.format(userinput))
    lowprice, highprice = userinput[-2], userinput[-1]
    print(work_address, lowprice, highprice)
    
    records = commutetime.comtime(work_address, lowprice, highprice)
    print(records)
    if records == -1:
        return redirect('index.html')
    house_locations = [[record[5], record[6]] for record in records]
    print(house_locations)
    work_location = [records[0][2], records[0][3]]

    return render_template('map.html', work_location=work_location, house_locations=house_locations, rows=records)

@app.route("/about")
def about():
    return render_template('about.html')
	
	
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
