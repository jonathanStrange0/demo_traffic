from app import app, nav
from flask import render_template
from flask_nav.elements import Navbar, View
from app.forms import RunTrafficForm, AddPlatformUrlForm, AddPlatformForm

nav.register_element('demo_traffic', Navbar(
    View('Home', '.index'),
    View('Add Integration Partner', '.add_integration'),
    View('Edit Integration Partner', '.index'),

))


@app.route('/')
@app.route('/index')
def index():
    form = RunTrafficForm()
    return render_template('index.html', form=form)

@app.route('/add_integration')
def add_integration():
    platform_form = AddPlatformForm()
    url_form = AddPlatformUrlForm()


    return render_template('add_integration.html', platform_form=platform_form, url_form = url_form)

