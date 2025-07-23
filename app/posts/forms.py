from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, RadioField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    content = TextAreaField('Content', validators=[DataRequired()])
    visibility = RadioField('Visibility', choices=[
        ('public', 'Public'),
        ('private', 'Private')
    ])
    submit = SubmitField('Submit')