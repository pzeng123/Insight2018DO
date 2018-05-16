# This contains our frontend; since it is a bit messy to use the @app.route
# decorator style when using application factories, all of our routes are
# inside blueprints. This is the front-facing blueprint.
#
# You can find out more about blueprints at
# http://flask.pocoo.org/docs/blueprints/

from flask import Blueprint, render_template, flash, redirect, url_for, send_from_directory
from flask_bootstrap import __version__ as FLASK_BOOTSTRAP_VERSION
from flask_nav.elements import Navbar, View, Subgroup, Link, Text, Separator
from markupsafe import escape

from .forms import SignupForm
from .nav import nav
import dominate
from dominate.tags import img
import os

frontend = Blueprint('frontend', __name__)

# We're adding a navbar as well through flask-navbar. In our example, the
# navbar has an usual amount of Link-Elements, more commonly you will have a
# lot more View instances.
# branding = img(src='/static/img/logo.png')

# nav.register_element('frontend_top', Navbar(
    # branding,

    # View('Flask-Bootstrap', '.index'),
    # View('Home', '.index'),
    # View('Forms Example', '.example_form'),
    # View('Debug-Info', 'debug.debug_root'),
    # Subgroup(
        # 'Docs',
        # Link('Flask-Bootstrap', 'http://pythonhosted.org/Flask-Bootstrap'),
        # Link('Flask-AppConfig', 'https://github.com/mbr/flask-appconfig'),
        # Link('Flask-Debug', 'https://github.com/mbr/flask-debug'),
        # Separator(),
        # Text('Bootstrap'),
        # Link('Getting started', 'http://getbootstrap.com/getting-started/'),
        # Link('CSS', 'http://getbootstrap.com/css/'),
        # Link('Components', 'http://getbootstrap.com/components/'),
        # Link('Javascript', 'http://getbootstrap.com/javascript/'),
        # Link('Customize', 'http://getbootstrap.com/customize/'), ),
    # Text('Using Flask-Bootstrap {}'.format(FLASK_BOOTSTRAP_VERSION)), ))


# Our index-page just shows a quick explanation. Check out the template
# "templates/index.html" documentation for more details.


@frontend.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(frontend.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
	
@frontend.route('/', methods=('GET', 'POST'))
def index():
    form = SignupForm()

    if form.validate_on_submit():
        
        return redirect(url_for('.index'))

    return render_template('index.html', form=form)
