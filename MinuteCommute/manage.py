
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

from flask_nav.elements import Navbar, View, Subgroup, Link, Text, Separator
from markupsafe import escape
from nav import nav
import dominate
from dominate.tags import img

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('default_settings')
app.config.from_pyfile('local_settings.py', silent=True)


Bootstrap(app)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
nav.init_app(app)

input_path = 'position3.txt'

app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))

branding = img(src='static/img/logo.png')

nav.register_element('frontend_top', Navbar(
    branding,
    View('Home', '.index'),
    View('Github', 'https://github.com/pzeng123/MinuteCommute'),
    View('Google Slides', 'https://www.google.com'),
    View('About', '.about'),
    Text("Don't waste time commuting")
))




class AddressForm(Form):
    name = StringField('What is your working location?', validators=[Required()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = AddressForm()
    # creating a map in the view
    mymap = []
    mytime = []
    with open('position3.txt', "r") as inputfile:
        for current_appartment in inputfile:
            current_appartment = current_appartment.strip().split('|')
            location = [float(current_appartment[0].split(',')[0]), float(current_appartment[0].split(',')[1])]
            time = float(current_appartment[1])
            mymap.append(location)
            mytime.append(time)
			

    if form.validate_on_submit():
        return render_template('map.html', maymap=mymap, mytime=mytime)
    return render_template('index.html', name=name, form=form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
	
@app.route("/map")
def map():
    mymap = []
    mytime = []
    with open('position3.txt', "r") as inputfile:
        for current_appartment in inputfile:
            current_appartment = current_appartment.strip().split('|')
            location = [float(current_appartment[0].split(',')[0]), float(current_appartment[0].split(',')[1])]
            time = float(current_appartment[1])
            mymap.append(location)
            mytime.append(time)
    return render_template('map.html', maymap=mymap, mytime=mytime)

@app.route("/about")
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0',port = 8000, debug=True)

