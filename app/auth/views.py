from .. import db, SQLAlchemy, Message
from .. import mail
from .models import User
from .forms import RegistrationForm, LoginForm, AuthorizationForm
from .forms import UpdateAccountForm, ResetPasswordForm, RestoreAccountForm, RestorePasswordForm
from ..product.models import Products, Ratings
from flask import render_template, redirect, url_for, flash, request, current_app, make_response, session
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash
import os
import secrets
from PIL import Image
from datetime import datetime
from random import randint
from http import cookies
from captcha.image import ImageCaptcha

from . import auth_blueprint

def generate_code():
    return str(randint(10 ** 7, 10 ** 8 - 1))

def generate_captcha_text():
    text = ""
    length_gen = randint(5, 7)
    for i in range(length_gen):
        choose_gen = randint(1, 2)
        if choose_gen == 1:
            text += chr(randint(97, 122))
        elif choose_gen == 2:
            text += str(randint(0, 9))
    return text

@auth_blueprint.route("/users")
def users():
    all_users = User.query.all()
    flag = True
    if len(all_users) == 0:
        flash("Користувачі відсутні у базі даних.", category= "warning")
        flag = False
    resp = make_response(render_template('users.html', all_users = all_users, title = "Users", flag = flag))
    resp.set_cookie('used_attempts', '0')
    return resp
    

@auth_blueprint.route("/register", methods = ['GET', 'POST'])
def register():
    if session.get("captcha_text") == None:
        session["captcha_text"] = ""
    if current_user.is_authenticated:
        return redirect(url_for('auth.account'))
    form = RegistrationForm()
    image = ImageCaptcha(width = 280, height = 90)
    captcha_text = generate_captcha_text()
    image.write(captcha_text, 'app/static/img/CAPTCHA.png')
    counter = int(request.cookies.get('used_attempts', 0))
    if counter >= 6:
        return render_template('failed.html', title='Register')
    form.captcha_hidden.data = session["captcha_text"]
    if form.validate_on_submit():
        session['username'] = form.username.data
        session['name'] = form.name.data
        session['lastname'] = form.lastname.data
        session['email'] = form.email.data
        session['password'] = form.password.data,
        session['number_phone'] = form.number_phone.data
        session['code'] = generate_code()
        return redirect(url_for('auth.double_auth'))
    else:
        counter += 1
    session["captcha_text"] = captcha_text
    resp = make_response(render_template('register.html', form=form, captcha_image = 'CAPTCHA.png', title = 'Register'))
    resp.set_cookie('used_attempts', str(counter))
    print(counter)
    return resp
    

@auth_blueprint.route("/login", methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.account_info', id = current_user.id))
    form = LoginForm()
    if form.validate_on_submit(): 
        email = form.email.data
        password = form.password.data
        dataEmail = User.query.filter_by(email = email).first()
        if dataEmail is None or dataEmail.verify_password(password) == False:
            flash('Відсутній обліковий запис. Зареєструйте свій аккаунт.', 
            category ='warning') 
            return redirect(url_for('auth.login'))   
        else:
            login_user(dataEmail, remember=form.remember.data)
            flash("Авторизація пройшла успішно!", category = 'success')
            return redirect(url_for('auth.login'))
    resp = make_response(render_template('login.html', form=form, title='Login'))
    resp.set_cookie('used_attempts', '0')
    return resp

@auth_blueprint.route("/restore_account", methods=['GET', 'POST'])
def restore_account():
    form = RestoreAccountForm()
    if form.validate_on_submit():
        session["restore_email"] = form.email.data
        session["restore_code"] = generate_code()
        print("Joe Hendry")
        return redirect(url_for('auth.restore_auth'))
    return render_template('restore_account.html', form=form, title='Відновлення облікового запису')

@auth_blueprint.route("/restore_auth", methods=['GET', 'POST'])
def restore_auth():
    form = AuthorizationForm()
    code = session["restore_code"]
    msg = Message('Akakiy-Berula exotic product shop!', 
                sender = 'vlad5dyakun@gmail.com', 
                recipients = [session["restore_email"]])
    msg.subject = "Akakiy Berula exotic product shop!"
    msg.body = f"""Ви отримали код для відновлення сторінки. 
                Якщо це ваш аккаунт, то введіть код для підтвердження авторизації
                \nКод підтвердження: {code}"""
    mail.send(msg)
    print(code)
    if form.validate_on_submit():
        my_code = form.code.data
        if my_code == code:
            return redirect(url_for('auth.restore_password'))
    return render_template('restore_auth.html', form=form, title='Відновлення облікового запису')
    

@auth_blueprint.route("/restore_password", methods=['GET', 'POST'])
def restore_password():
    form = RestorePasswordForm()
    user = User.query.filter_by(email = session["restore_email"]).first()
    if form.validate_on_submit():
        user.password = generate_password_hash(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Пароль вашого облікового запису змінено!', category='access')
        return redirect(url_for('auth.login', title="Login"))
    return render_template('restore_password.html', form=form, title='Відновлення облікового запису')


@auth_blueprint.route("/double_auth", methods = ['GET', 'POST'])
def double_auth():
    form = AuthorizationForm()
    username = session['username']
    name = session['name']
    lastname = session['lastname']
    email = session['email']
    password = session['password']
    number_phone = session['number_phone']
    code = session['code']
    msg = Message('Akakiy-Berula exotic product shop!', 
                sender = 'vlad5dyakun@gmail.com', 
                recipients = [email])
    msg.subject = "Akakiy Berula exotic product shop!"
    msg.body = f"""Ви отримали код для реєстрації. 
                Якщо це ваш аккаунт, то введіть код для підтвердження авторизації
                \nКод підтвердження: {code}"""
    mail.send(msg)

    print(session['code'])
    if form.validate_on_submit():
        my_code = form.code.data
        print(my_code)
        print(code)
        if my_code == code:
            user = User(
                username = username, 
                name = name,
                lastname = lastname,
                email = email, 
                password = password[0],
                number_phone = number_phone,
            )
            db.session.add(user)
            db.session.commit()
            flash(f'Створено аккаунт для користувача {username}!', category = 'success')
            return redirect(url_for('auth.login'))
        else:
            flash(f'Код не підтверджено! Надіслано інший код!!!', category = 'warning')
            session['code'] = generate_code()
            return redirect(url_for('auth.double_auth'))
    return render_template('double_auth.html', form=form, title='Login')

@auth_blueprint.route("/logout")
def logout():
    logout_user()
    flash("Ви вийшли зі своєї сторінки!", category = "success")
    return redirect(url_for('auth.login'))

@auth_blueprint.route("/account", methods = ['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Дані вашого профілю оновлені!', category='success')
        return redirect(url_for('auth.account_info', id = current_user.id))
    form.username.data = current_user.username
    form.email.data = current_user.email
    form.about_me.data = current_user.about_me  
    image_file = url_for("static", filename = "profile_pics/" + current_user.image_file)
    return render_template("account.html", title="Account", image_file = image_file, form = form)

@auth_blueprint.route("/<id>/account_info", methods = ['GET', 'POST'])
@login_required
def account_info(id):
    user = User.query.get_or_404(id)
    ratings_list = db.session.query(Ratings, Products).\
        join(Products, Products.id == Ratings.product_id).\
            filter(Ratings.user_id == id).order_by(Ratings.date.desc()).all()
    print(ratings_list)
    return render_template('account_info.html',
                            title = "Сторінка" + user.username,
                            user = user,
                            ratings_list = ratings_list)        

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    output_size = (250, 250)

    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@auth_blueprint.route("/reset_password", methods=['GET', 'POST'])
@login_required
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        current_user.password = generate_password_hash(form.new_password.data)
        db.session.commit()
        flash('Пароль змінено', category='success')
        return redirect(url_for('auth.account_info', id = current_user.id))
    return render_template('reset_password.html', form = form)


@auth_blueprint.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_date = datetime.utcnow()
        db.session.commit()