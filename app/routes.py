from app import app, nav, db
from flask import render_template, request, redirect, url_for, session
from flask_nav.elements import Navbar, View
from app.forms import RunTrafficForm, AddPlatformUrlForm, AddPlatformForm
from app.models import IntegrationPlatform, Url
from app.browser_bot import BrowserBot
import sys, gc

nav.register_element('demo_traffic', Navbar(
    View('Home', '.index'),
    View('Add Integration Partner', '.add_integration'),
    View('Edit Integration Partner', '.edit_integration'),

))




@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    bb_list = []
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
                bb =BrowserBot(url=url.address)
                print(sys.getsizeof(bb) / 1024.0)
                bb_list.append(bb)
        # print(sys.getsizeof(bb_list) / 1024.0)
        return render_template('index.html', form=form, window_urls=window_urls)

    return render_template('index.html', form=form)


@app.route('/add_integration', methods=['GET', 'POST'])
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
            new_url = Url(address=url, num_headless=num_headless, num_windows=num_windows)
            db.session.add(new_url)
            platform.urls.append(new_url)
            db.session.commit()
        return (redirect(url_for('add_integration')))

    return render_template('add_integration.html', platform_form=platform_form, url_form=url_form)


@app.route('/edit_integration', methods=['GET', 'POST'])
def edit_integration():
    return('<h1>Something Wicked This Way Comes</h1>')


@app.route('/_free_mem')
def _free_mem():
    print(sys.getsizeof(session['bb_list']) / 1024.0)
    bb_session['bb_list'] = []
    print(sys.getsizeof(session['bb_list']) / 1024.0)
    return redirect(url_for('index'))
