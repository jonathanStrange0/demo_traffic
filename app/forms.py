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

