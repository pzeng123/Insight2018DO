from flask import Flask, render_template, redirect, url_for, request
from app import app, db
from models import Listing
from forms import Addressform
import scraper
import commutetime


#scraper.do_scrape()
print('scraper finish')

@app.route('/')
def index():
    # form = Addressform()
	
    # if form.validate_on_submit():
        # return redirect('/map', form=form)
    return render_template('index.html')
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
	
@app.route('/map', methods=['GET', 'POST'])
def map():
    work_location = request.form['address']
    print(work_location)
    # tabledata = commutetime.comtime(work_location)

    return render_template('map.html', tabledata=tabledata)

@app.route("/about")
def about():
    return render_template('about.html')
	
	
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)