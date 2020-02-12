from app import app, nav, db
from flask import render_template, request, redirect, url_for, session, flash
from flask_nav.elements import Navbar, View
from app.forms import RunTrafficForm, AddPlatformUrlForm, AddPlatformForm, EditIntegrationForm, LoginForm, CreateUserForm
from app.models import IntegrationPlatform, Url, User
from app.browser_bot import BrowserBot
import sys
import gc
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

# if session['logged_in']:
#     nav.register_element('demo_traffic', Navbar(
#         View('Home', '.index'),
#         View('Add Integration Partner', '.add_integration'),
#         View('Edit Integration Partner', '.edit_integration'),
#         View('Logout', '.logout'),
#         ))
# else:
#     nav.register_element('demo_traffic', Navbar(
#         View('Home', '.index'),
#         View('Add Integration Partner', '.add_integration'),
#         View('Edit Integration Partner', '.edit_integration'),
#         View('Login', '.login'),
#         ))
nav.register_element('demo_traffic', Navbar(
    View('Home', '.index'),
    View('Add Integration Partner', '.add_integration'),
    View('Edit Integration Partner', '.edit_integration'),
    View('Logout', '.logout'),
))


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    print(sys.getsizeof(bb_list) / 1024.0)
    form = RunTrafficForm()
    if request.method == "POST" and form.validate_on_submit():
        platform = form.platform_select_field.data
        window_urls = []
        headless_urls = []
        for url in platform.urls:
            for num in range(url.num_windows):
                window_urls.append(url.address)
            for num in range(url.num_headless):
                # headless_urls.append(url.address)
                bb = BrowserBot(url=url.address)
                print(sys.getsizeof(bb) / 1024.0)
        for bb in bb_list:
            bb.browser.stop_client()
        return render_template('index.html', form=form, window_urls=window_urls)

    return render_template('index.html', form=form)


@app.route('/add_integration', methods=['GET', 'POST'])
@login_required
def add_integration():
    platform_form = AddPlatformForm()
    url_form = AddPlatformUrlForm()
    if request.method == 'POST' and platform_form.validate_on_submit():
        platform_name = platform_form.platform_name.data
        # print(platform_name)
        if len(IntegrationPlatform.query.filter_by(platform=platform_name).all()) == 0:
            new_platform = IntegrationPlatform(platform=platform_name)
            db.session.add(new_platform)
            db.session.commit()
        return (redirect(url_for('add_integration')))
    elif request.method == 'POST' and url_form.validate_on_submit():
        url = url_form.url_field.data
        if not url_form.num_headless:
            num_headless = 0
        else:
            num_headless = url_form.num_headless.data
        if not url_form.num_plain:
            num_windows = 0
        else:
            num_windows = url_form.num_plain.data
        platform = url_form.platform_select_field.data
        if len(Url.query.filter_by(address=url).all()) == 0:
            new_url = Url(address=url, num_headless=num_headless,
                          num_windows=num_windows)
            db.session.add(new_url)
            platform.urls.append(new_url)
            db.session.commit()
        return (redirect(url_for('add_integration')))

    return render_template('add_integration.html', platform_form=platform_form, url_form=url_form)


@app.route('/edit_integration', methods=['GET', 'POST'])
@login_required
def edit_integration():
    form = EditIntegrationForm()

    if request.method == 'POST' and form.validate_on_submit():
        sites_list = form.platform_select_field.data.urls
        return render_template('edit_integrations.html', form=form, sites_list=sites_list)
    return render_template('edit_integrations.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_name=form.user_name.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        session['logged_in'] = True
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    session['logged_in'] = False
    return redirect(url_for('index'))


@app.route('/_save_address_changes', methods=['GET', 'POST'])
def _save_address_changes():
    if request.method == "POST":
        result = request.form
        # print(result)
        url = Url.query.filter_by(address=result['disabled-address']).first()
        if url.address != result['address']:
            url.address = result['address']
        elif url.num_headless != int(result['headless']):
            url.num_headless = int(result['headless'])
        elif url.num_windows != int(result['windows']):
            url.num_windows = int(result['windows'])
        db.session.commit()
    return(redirect(url_for('edit_integration')))


@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    form = CreateUserForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_name=form.user_name.data).first()
        if user:
            flash('This User Name Already Exists, Please Choose Another')
        else:
            user = User(user_name=form.user_name.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)
            return(redirect(url_for('index')))
    return render_template('create_user.html', form=form)
