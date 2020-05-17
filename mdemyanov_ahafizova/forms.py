from flask_wtf import FlaskForm
from wtforms import DateTimeField
from wtforms import IntegerField
from wtforms import SelectField
from wtforms import SubmitField


class FilterForm(FlaskForm):
    count = IntegerField('Количество логов: ')
    mes_type = SelectField('Тип сообщения: ', choices=[
        ('ALL', 'ALL'), ('Info', 'Info'), ('Warning', 'Warning'), ('Error', 'Error')])
    submit = SubmitField('Отправить')


class DateFilterForm(FlaskForm):
    date_start = DateTimeField('От: ')
    date_end = DateTimeField('До: ')
    mes_type = SelectField('Тип сообщения: ', choices=[
        ('ALL', 'ALL'), ('Info', 'Info'), ('Warning', 'Warning'), ('Error', 'Error')])
    submit = SubmitField('Отправить')
