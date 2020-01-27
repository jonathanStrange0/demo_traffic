from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, PasswordField, BooleanField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired
from app import db
from app.models import IntegrationPlatform, Url


class RunTrafficForm(FlaskForm):
    platform_select_field = QuerySelectField(query_factory=lambda: IntegrationPlatform.query.order_by('platform'),
                                             allow_blank=False,
                                             get_label='platform',
                                             validators=[DataRequired()])
    submit_button = SubmitField(label='Generate Synthetic Traffic Data')
    # kill_button = SubmitField(label='Stop Headless Background Browsers')


class AddPlatformForm(FlaskForm):
    platform_name = StringField(_name='Platform to Add', validators=[DataRequired()])
    submit_button = SubmitField(label='Add New Platform')


class AddPlatformUrlForm(FlaskForm):
    platform_select_field = QuerySelectField(query_factory=lambda: IntegrationPlatform.query.order_by('platform'),
                                             allow_blank=False,
                                             get_label='platform',
                                             validators=[DataRequired()])
    url_field = StringField(_name='Add URL', validators=[DataRequired()])
    num_headless = IntegerField("Number of headless browsers to open", )
    num_plain = IntegerField("Number of standard browser windows to open", )
    submit_button = SubmitField(label='Save New URL To Platform')


class EditIntegrationForm(FlaskForm):
    platform_select_field = QuerySelectField(query_factory=lambda: IntegrationPlatform.query.order_by('platform'),
                                             allow_blank=False,
                                             get_label='platform',
                                             validators=[DataRequired()])
    submit_button = SubmitField(label='Edit this parner')


class LoginForm(FlaskForm):
    user_name = StringField(_name='Username', validators=[DataRequired()])
    password = PasswordField(_name='Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit_button = SubmitField(label='Login')
