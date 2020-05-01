from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length


class JobsForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[Length(min=0, max=140), DataRequired()])
    category = SelectField("Категория", choices=[("prog", "Программирование"), ("des", "Дизайн"), ("av", "аудио/видео"),
                                                 ("mrk", "Маркетинг"), ("tw", "Работа с текстом")],
                           validators=[DataRequired()])
    category_2 = SelectField("Дополнительная категория", choices=[('None', 'Нет'), ("prog", "Программирование"), ("des", "Дизайн"), ("av", "аудио/видео"),
                                                 ("mrk", "Маркетинг"), ("tw", "Работа с текстом")])
    cost = IntegerField("Цена", validators=[DataRequired()])
    submit = SubmitField("Продолжить")