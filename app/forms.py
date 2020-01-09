from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired
from app import db
from app.models import IntegrationPlatform, Url

class RunTrafficForm(FlaskForm):
    platform_select_field = QuerySelectField(query_factory=lambda: IntegrationPlatform.query.order_by('platform'))
    submit_button = SubmitField(label='Generate Synthetic Traffic Data')
    kill_button = SubmitField(label='Stop Headless Background Browsers')

class AddPlatformForm(FlaskForm):
    platform_name = StringField(_name='Platform to Add',validators=[DataRequired()])
    submit_button = SubmitField(label='Add New Platform')

class AddPlatformUrlForm(FlaskForm):
    platform_select_field = QuerySelectField(query_factory=lambda: IntegrationPlatform.query.order_by('platform'))
    url_field = StringField(_name='Add URL', validators=[DataRequired()])
    submit_button = SubmitField(label='Save New URL To Platform')