#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import app
from app.my_form import Question, Regform, question_one, question_four, question_tree, question_two, Submit, Resform

from flask import render_template, flash, redirect, url_for, request, session
import re # Библиотека, необходимая для извлечения вопросов из файла tasks.txt
import random
import os # Библиотека, которая позволяет использовать функции из операционной системы (mkdir, mknod, ls, cd, ...)
import time
import sys

UPLOAD_FOLDER = os.path.abspath(os.curdir).decode('utf-8')
reload(sys)
sys.setdefaultencoding('utf8')

questions = []

# Массив из классов вопросов. База данных вопросов
# которые представлены в удобном, для системы виде
class_questions = []
max_questions=0
list_of_sessions = []

# Переменнвя, в которой хранится количество вопросов в тесте
questions_in_test = 20

# Количество вопросов в системе
questions_all = 0

def genetate_question():
    global questions_all
    # Открываем файл, в котором расположены все вопросы
    # sed $'s/\r$//' tasks-2.txt > tasks-3.txt используй эту команду для
    # конвертации файла с заданиями из DOS (tasks-2.txt) в UNIX (tasks-3.txt) кодировку
    f = open(UPLOAD_FOLDER+"/tasks-4.txt","r")

    # Считываем в переменную extract_file весь файл tasks.txt
    extract_file = f.read()

    # Просим библотеку re (regex) извлечь в отдельный массив (raw_questions) вопросы из extract_file
    # которые разделены ***
    # NB: split - это функция библотеки re, которая разделяет строку на массив
    # по определённому разделителю (пример - пробел)
    raw_questions = re.split("\*\*\*\n",extract_file)

    # Каждый элемент из массива raw_questions помещаем в quest
    # и проводим одни и те же операции
    for quest in raw_questions:

        # Если элемент пустой, то рассматриваем следующий элемент
        if quest == '':
            continue

        tmp = re.split("---\n",quest)

        # Заменяем символ переноса строки (\n) на пустой символ (для красивого вывода)
        tmp[0] = tmp[0].replace('\n','')
        tmp[1] = tmp[1].replace('\n','')
        # Разделяем варианты ответа по отдельным строкам
        tmp[2] = re.split("\n", tmp[2])

        # Удаляем из массива tmp[2] пустой ('') элемент
        tmp[2].remove('')

        tmp[3] = re.split(",",tmp[3].replace('\n',''))

        # Инициализация вопросов в нашей системе
        class_questions.append(
            Question(question_text=tmp[1].decode('utf-8'), question_type=tmp[0], true_answer=tmp[3],
                     choice_of_answer=tmp[2]))

        questions_all = questions_all + 1

# Генерация вопросов из файла
genetate_question()

# Функция для проверки правильности ответа клиента
def check(type, true_answer):
    print type, true_answer
    if type == "string":
        try:
            test_form = request.form["string"]
            print test_form
            if test_form == str(true_answer):
                return 1
            else:
                return 0
        except:
            print "string Error"
            return 0
    if type == "radio":
        try:
            test_form = request.form["radio_1"]
            print test_form
            if test_form in true_answer:
                return 1
            else:
                return 0
        except:
            print "radio Error"
            return 0
    if type == "checkbox":
        false_answer = ['1','2','3','4','5','6']
        for i in true_answer:
            false_answer.remove(i)
        test_form_box = []
        try:
            for i in true_answer:
                test_form_box.append(request.form["check_box_" + i])
            for i in false_answer:
                try:
                   request.form["check_box_" + i]
                   print "Have a false choice "+i
                   return 0
                except:
                    continue
            return 1
        except:
            print "checkbox Error"
            return 0

@app.route('/test', methods = ['GET', 'POST'])
def test():
    # Кнопка выхода
    common = Submit()

    test_form = []

    # Вывод правильных ответов на web-страницу
    res = []

    res.append(questions_in_test)

    if request.method == 'POST':
        # Обработка предыдущего вопроса
        # [session["current_index"] - 1] - это индекс элемента,
        # относительно вопросов клиента (session["questions"]),
        # в которых написаны ID вопросов в системе (class_questions)
        last_question = class_questions[session["questions"][session["current_index"] - 1]]
        session["true_answer"] = session["true_answer"] + check(last_question.question_type,
                                                                last_question.true_answer)
        res.append(session["true_answer"])
    else:
        res.append(0)

    # Условие завершение теста
    if session["current_index"] >= questions_in_test: # questions_in_test - is max questions in session
        return redirect(url_for('result'))

    # Обработка кнопки выхода
    if common.button.data:
        token = session["name"]+session["group"]
        # Если пользователь есть в системе
        if token in list_of_sessions:
            flash("User "+session["name"]+" exited successful")
            list_of_sessions.remove(token)
        else:
            flash("No such user: " + session["name"])
        return redirect(url_for('login'))

    question_nubmer = session["questions"][session["current_index"]]
    session["current_index"] = session["current_index"] + 1
    current_ques = class_questions[question_nubmer]

    if current_ques.question_type == "radio":
        test_form = question_one()
        test_form.radio_1.choices = current_ques.choices

    if current_ques.question_type == "checkbox":
        test_form = question_two()

    if current_ques.question_type == "string":
        test_form = question_tree()

    if current_ques.question_type == "select":
        test_form = question_four()

    return render_template("test.html",
                           form=test_form,
                           question = class_questions[question_nubmer],
                           common=common,
                           res = res)

@app.route('/', methods = ['GET', 'POST'])
@app.route('/login',methods = ['GET', 'POST'])
def login():
    # Инициализация форм в переменную form
    form = Regform()

    # Проверка на корректность вводимых данных, после нажатия кнопки
    if form.validate_on_submit():
        session["name"] = form.name.data.lower()
        session["group"] = form.group.data.lower()

        token = session["name"]+session["group"]

        # В поле сессии одного пользователя присваиваются идентификаторы вопросов,
        # которые находятся в нашей системе. Они не повторяются (random.sample)
        session["questions"] = random.sample(range(0,questions_all),questions_in_test) # 3 - is max questions in session
        session["current_index"] = 0
        session["true_answer"] = 0

        # Пытаемся узнать, есть ли данный пользователь в системе
        if token in list_of_sessions:
            # Выводим сообщение об ошибке
            flash("This user already in system")
            # И просим заново ввести Имя и Группу
            return redirect(url_for('login'))
        else:
            # Если пользователя нет в системе, то добавляем его в список
            list_of_sessions.append(token)
            # И перенаправляем в Тест
        return redirect(url_for('test'))
    else:
        print form.errors
    return render_template("autentification.html",
                            form=form)

@app.route('/result',methods = ['GET', 'POST'])
def result():
    form = Resform()
    res = []
    res.append(session["true_answer"])

    if res[0] >= 17 and res[0] <=20:
        res.append(5)
    elif res[0] >= 14 and res[0] <=16:
        res.append(4)
    elif res[0] >= 10 and res[0] <= 13:
        res.append(3)
    else:
        res.append(2)

    # Флаг, который необходим для обозначения существования директории
    have_directory = 0

    # os.listdir - прозволяет увидеть все файлы, которые находятся по пути UPLOAD_FOLDER+"/tmp/"
    # Имя каждого файла из директории UPLOAD_FOLDER+"/tmp/" помещаем в i
    for i in os.listdir(UPLOAD_FOLDER+"/tmp/"):

        # Если есть диретория с именем группы
        if i == session["group"]:
            have_directory = 1
            # Make work with file in function

            f = open(UPLOAD_FOLDER+"/tmp/" + i + "/" + session["name"],"a")
            f.write("Result: " + str(res[0]) + "\n")
            f.write("Score: " + str(res[1]) + "\n")
            f.write(str(time.time())+"\n\n")
            f.close()

    if have_directory == 0:

        os.mkdir(UPLOAD_FOLDER+"/tmp/"+str(session['group']))
        # Записать результат в файл
        f = open(UPLOAD_FOLDER+"/tmp/" + session['group'] +"/"+ session["name"], "a")
        f.write("Result: " + str(res[0]) + "\n")
        f.write("Score: " + str(res[1]) + "\n")
        f.write(str(time.time()) + "\n\n")
        f.close()

    # Если нажата кнопка "повторить", то заново генерируем вопросы и очищаем предыдущий результат
    if form.repeat.data:
        session["questions"] = random.sample(range(0, questions_all), questions_in_test)  # questions_in_test - is max questions in session
        session["current_index"] = 0
        session["true_answer"] = 0
        return redirect(url_for('test'))
    # Если нажата кнопка "выход", то выходим из системы
    if form.exit.data:
        token = session["name"]+session["group"]
        if token in list_of_sessions:
            flash("User "+session["name"]+" exited successful")
            list_of_sessions.remove(token)
        else:
            flash("No such user: " + session["name"])
        return redirect(url_for('login'))

    return render_template("exit.html",
                           form = form,
                           res = res)

@app.route('/exit',methods = ['GET', 'POST'])
def exit_func():
    form = Submit()
    if form.button.data:
        token = session["name"]+session["group"]
        if token in list_of_sessions:
            flash("User "+session["name"]+" exited successful")
            list_of_sessions.remove(token)
        else:
            flash("No such user: " + session["name"])
        return redirect(url_for('login'))
    return render_template("exit.html",
                           title="Sign In",
                           form=form)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STATIC_FOLDER'] = 'tmp'

app.run(host="127.0.0.1",port=5000,debug = True)


