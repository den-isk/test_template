#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired

class question_one(FlaskForm):
    radio_1 = RadioField('radio_1')

class question_two(FlaskForm):
    check_box_1 = BooleanField('check_box_1', default=False)
    check_box_2 = BooleanField('check_box_2', default=False)
    check_box_3 = BooleanField('check_box_3', default=False)
    check_box_4 = BooleanField('check_box_4', default=False)
    check_box_5 = BooleanField('check_box_5', default=False)
    check_box_6 = BooleanField('check_box_6', default=False)

class question_tree(FlaskForm):
    string = StringField('string', validators = [DataRequired()])

class question_four(FlaskForm):
    select_1 = SelectField('select')
    select_2 = SelectField('select')
    select_3 = SelectField('select')
    select_4 = SelectField('select')

# Класс Question хранит в себе информацию о параметрах вопроса
# Это текст вопроса, тип вопроса, правильные(-й) вариант(-ы) ответа(-ов) и
# вариант(-ы) ответов, если они есть
class Question():

    # Функция инициализации, при первом обращении к классу
    def __init__(self, question_text, question_type, true_answer, choice_of_answer):
        if "radio" in question_type:
            self.choices = []

            # Элеименту i присваивается поочереди числа в диапазоне (range)
            # от 0 до количества ответов (len)
            for i in range(0,len(choice_of_answer)):
                # Переменной choices поочереди присваиваем кордеж из
                # индекса и значения, для удобной передачи на web-форму
                # Пример: ('1':'Вопрос 1') -> RadioField.choices = [('1':'Вопрос 1'), ('2':'Вопрос 2'),('3':'Вопрос 3')]
                self.choices.append((str(i+1), choice_of_answer[i].decode('utf-8')))

        if "checkbox" in question_type:
            self.choices = []
            for i in range(0, len(choice_of_answer)):
                self.choices.append((str(i + 1), choice_of_answer[i].decode('utf-8')))

        if "string" in question_type:
            self.true_answer = true_answer

        if "select" in question_type:
            self.choices = []
            for i in range(0, len(choice_of_answer)):
                self.choices.append((str(i + 1), choice_of_answer[i].decode('utf-8')))

        self.true_answer = true_answer
        self.question_text = question_text
        self.question_type = question_type


class Regform(FlaskForm):
    name = StringField('name', validators = [DataRequired()])
    group = StringField('group', validators=[DataRequired()])

class Submit(FlaskForm):
    button = SubmitField('exit', validators = [DataRequired()])

class Resform(FlaskForm):
    repeat = SubmitField("repeat")
    exit = SubmitField("exit")