from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class ProjectForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[Length(min=0, max=140), DataRequired()])
    img = StringField("Изображение")
    submit = SubmitField("Продолжить")
