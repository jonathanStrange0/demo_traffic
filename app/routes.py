from app import app, nav
from flask import render_template
from flask_nav.elements import Navbar, View


nav.register_element('demo_traffic', Navbar(
    View('Home', '.index'),
    View('Add Integration Partner', '.index'),
    View('Edit Integration Partner', '.index'),

))


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/add_integration')
def add_integration():
    pass

