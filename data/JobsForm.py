from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class JobsForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    description = StringField('Описание', validators=[DataRequired()])
    cost = IntegerField("Цена", validators=[DataRequired()])
    submit = SubmitField("Продолжить")
