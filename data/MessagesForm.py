from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class MessagesForm(FlaskForm):
    text = TextAreaField('Описание', validators=[Length(min=0, max=140), DataRequired()])
    submit = SubmitField("Продолжить")
