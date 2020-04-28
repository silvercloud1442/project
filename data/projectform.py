from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ProjectForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    description = StringField('Описание', validators=[DataRequired()])
    img = StringField("Изображение")
    submit = SubmitField("Продолжить")
