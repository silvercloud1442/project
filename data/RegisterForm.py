from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = StringField('Пароль', validators=[DataRequired()])
    password_again = StringField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    age = StringField('Возраст', validators=[DataRequired()])
    description = StringField('Обо мне:')

    submit = SubmitField('Продолжить')