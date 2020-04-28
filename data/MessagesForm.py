from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class MessagesForm(FlaskForm):
    text = StringField(validators=[DataRequired()])
    submit = SubmitField("Продолжить")
