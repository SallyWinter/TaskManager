from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

class EventForm(FlaskForm):
    id = HiddenField('id', validators=[DataRequired()])
    eventname = StringField('Event Name', validators=[DataRequired()])
    description = TextAreaField('Event Description', validators=[DataRequired()])
    startDate = StringField('Start Date')
    endDate = StringField('End date')
    createEvent = SubmitField('Create event')
    status = StringField('Status')
    removeEvent = HiddenField('remove Task')
