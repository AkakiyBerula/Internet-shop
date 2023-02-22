from flask import Flask, render_template, request, flash, Blueprint
from flask_bootstrap import Bootstrap
from datetime import datetime
from platform import platform
from sys import version

from . import main_blueprint

def get_footer():
    footer_data = {
        "platform": platform(),
        "request": request.user_agent,
        "python_version": version,
        "datetime": datetime.now().strftime('%d/%m/%Y %H:%M')
    }
    return footer_data

@main_blueprint.route('/')
def index():
    data = "Main Page"
    title = "Головна сторінка"
    subtitle = "Опис навігаційного меню"
    footer_form = get_footer()
    return render_template('index.html', 
        data = data, 
        title = title,
        subtitle = subtitle,
        footer_form = footer_form
    )
def get_forms():
    forms = [
        {
            "name": "Vladyslav",
            "surname": "Diakun",
            "dateborn": datetime(2000, 12, 14, 0, 0).strftime('%d/%m/%Y'),
            "group": "IPZ-31",
            "email": "vlad5dyakun@gmail.com",
            "coorp_email": "vladyslav.diakun.19@pnu.edu.ua"
        },
        {
            "name": "Danilo",
            "surname": "Golub",
            "dateborn": datetime(2001, 8, 31, 0, 0).strftime('%d/%m/%Y'),
            "group": "IPZ-41",
            "email": "getreadytofly4l@gmail.com",
            "coorp_email": "danilo.golub.18@pnu.edu.ua"
        },
        {
            "name": "Yaroslav",
            "surname": "Osadchiy",
            "dateborn": datetime(2000, 4, 11, 0, 0).strftime('%d/%m/%Y'),
            "group": "M-41",
            "email": "hatsunismov_forever@gmail.com",
            "coorp_email": "yaroslav.osadchiy.19@pnu.edu.ua"
        }
    ]
    return forms

def get_numbers():
    numbers = [9, -3, 12, -7, -2, -13, 27, 4, 0, 54]
    return numbers

def get_footer():
    footer_data = {
        "platform": platform(),
        "request": request.user_agent,
        "python_version": version,
        "datetime": datetime.now().strftime('%d/%m/%Y %H:%M')
    }
    return footer_data

@main_blueprint.route('/if')
def if_statement():
    data = "If Statements"
    title = "Оператори If, elif, else"
    footer_form = get_footer()
    numbers = get_numbers()
    return render_template('if.html', 
        data = data,
        title = title,
        footer_form = footer_form,
        numbers = numbers
    )

@main_blueprint.route('/for')
def for_cycle():
    data = "For cycle"
    title = "Оператор циклу for"
    footer_form = get_footer()
    forms = get_forms()
    return render_template('for.html', 
        data = data,
        title = title, 
        footer_form = footer_form,
        forms = forms
    )

@main_blueprint.errorhandler(404)
def not_found(error):
    return render_template("404.html", title = "Error 404")