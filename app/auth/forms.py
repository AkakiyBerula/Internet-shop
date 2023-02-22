from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SelectField, PasswordField, BooleanField 
from wtforms import SubmitField, ValidationError, TextAreaField, HiddenField
from wtforms.validators import Length, DataRequired, Email, EqualTo, Regexp
from flask_login import current_user
from werkzeug.security import check_password_hash

from .models import User
import enum

class PostType(enum.Enum):
    User = 1
    Moderator = 2
    Admin = 3

class RegistrationForm(FlaskForm):
    username = StringField('Нікнейм користувача', validators=[
                            Length(min=3, max=25, 
                            message = 'Це поле має бути довжиною між 4 та 25 символів.'), 
                            DataRequired(message ="Це поле обов'язкове."),
                            Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                            "Нікнейм користувача може мати тільки Великі і малі латинські літери, цифри,"
                            "крапки і нижнє підкреслення.")])
    name = StringField('Ім\'я користувача', validators=[
                            Length(min=2, max=30, 
                            message = 'Це поле має бути довжиною між 4 та 25 символів.'), 
                            DataRequired(message ="Це поле обов'язкове.")])
    lastname = StringField('Прізвище користувача', validators=[
                            Length(min=2, max=50, 
                            message = 'Це поле має бути довжиною між 4 та 25 символів.'), 
                            DataRequired(message ="Це поле обов'язкове.")])
    email = StringField('Email', validators=[
                        Email(message="Неправильно вказана електронна пошта."), 
                        DataRequired(message = "Це поле обов'язкове.")])
    password = PasswordField('Password', 
                            validators=[Length(min=6, 
                            message = 'Це поле має бути більше 6 символів.'), 
                            DataRequired(message = "Це поле обов'язкове."),
                            Regexp('(?=.*[0-9])(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z!@#$%^&*]{8,}', 0,
                            "Пароль повинен включати великі і малі літери, цифру і символ (!@#$%^&*).")
                            ])
    confirm_password = PasswordField('Confirm Password', 
                validators=[DataRequired(message = "Це поле обов'язкове."), 
                EqualTo('password', message = "Паролі не співпадають!")])
    number_phone = StringField('Номер телефону', validators=[ 
                            DataRequired(message = "Це поле обов'язкове."),
                            Regexp('[+380][0-9]{9}', 0,
                            "Пароль повинен включати великі і малі літери, цифру і символ (!@#$%^&*).")
                            ])
    
    captcha_user = StringField('Captcha', validators=[ 
                                    DataRequired(message = "Це поле обов'язкове."),
                                    EqualTo("captcha_hidden", message = "Captcha validation failed!")])
    captcha_hidden = HiddenField('')
    submit = SubmitField('Sign up')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Електронна пошта уже зареєстрована.")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Ім'я користувача уже використовується.")

class AuthorizationForm(FlaskForm):
    code = StringField('Verification', validators=[
                                            DataRequired(message = "Це поле обов'язкове")]) 
    submit = SubmitField('Confirm')  


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
                                DataRequired(message = "Це поле обов'язкове"), 
                                Email(message="Неправильно вказана електронна пошта")])
    password = PasswordField('Password', validators=[
                                        DataRequired(message = "Це поле обов'язкове")])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Нікнейм користувача', validators=[
                            Length(min=3, max=25, 
                            message = 'Це поле має бути довжиною між 4 та 25 символів.'), 
                            DataRequired(message ="Це поле обов'язкове."),
                            Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                            "Нікнейм користувача може мати тільки Великі і малі латинські літери, цифри,"
                            "крапки і нижнє підкреслення.")])
    name = StringField('Ім\'я користувача', validators=[
                            Length(min=2, max=30, 
                            message = 'Це поле має бути довжиною між 4 та 25 символів.'), 
                            DataRequired(message ="Це поле обов'язкове.")])
    lastname = StringField('Прізвище користувача', validators=[
                            Length(min=2, max=50, 
                            message = 'Це поле має бути довжиною між 4 та 25 символів.'), 
                            DataRequired(message ="Це поле обов'язкове.")])
    email = StringField('Email', validators=[
                        DataRequired(message = "Це поле обов'язкове"),
                        Email(message="Неправильно вказана електронна пошта."),])
    number_phone = StringField('Номер телефону', validators=[ 
                            DataRequired(message = "Це поле обов'язкове."),
                            Regexp('[+380][0-9]{9}', 0,
                            "Пароль повинен включати великі і малі літери, цифру і символ (!@#$%^&*).")
                            ])
    picture = FileField('Оновити аватар профілю', validators=[FileAllowed(['jpg', 'png'])])  
    about_me = TextAreaField('Про мене', validators=[DataRequired(), Length(max=500)], render_kw={'rows': 5})
    submit = SubmitField('Оновити інформацію')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Це ім'я користувача використовується. Будь ласка введіть інше.")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Цей email використовується. Будь ласка виберіть іншу')

class ResetPasswordForm(FlaskForm):
    old_password = PasswordField('Старий пароль', validators=[DataRequired(message = "Це поле обов'язкове")])

    new_password = PasswordField('Новий пароль', 
                        validators=[Length(min=6, 
                            message = 'Це поле має бути більше 6 символів.'), 
                            DataRequired(message = "Це поле обов'язкове."),
                            Regexp('(?=.*[0-9])(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z!@#$%^&*]{8,}', 0,
                            "Пароль повинен включати великі і малі літери, цифру і символ (!@#$%^&*).")
                            ])

    repeat_new_password = PasswordField('Повторіть пароль', 
                                validators=[DataRequired(message = "Це поле обов'язкове"),
                                        Length(min=6, message='Пароль мусить мати не менше 6 символів'),
                                        EqualTo('new_password')])
    
    def validate_old_password(self, field):
        if not check_password_hash(current_user.password, field.data):
            raise ValidationError('Це не ваш пароль')

class RestoreAccountForm(FlaskForm):
    email = StringField('Введіть Email', validators=[
                        DataRequired(message = "Це поле обов'язкове"),
                        Email(message="Неправильно вказана електронна пошта.")])
    submit = SubmitField('Confirm') 
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('Цей email відсутній в базі даних!')

class RestorePasswordForm(FlaskForm):
    password = PasswordField('Password', 
                            validators=[Length(min=6, 
                            message = 'Це поле має бути більше 6 символів.'), 
                            DataRequired(message = "Це поле обов'язкове."),
                            Regexp('(?=.*[0-9])(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z!@#$%^&*]{8,}', 0,
                            "Пароль повинен включати великі і малі літери, цифру і символ (!@#$%^&*).")
                            ])
    confirm_password = PasswordField('Confirm Password', 
                validators=[DataRequired(message = "Це поле обов'язкове."), 
                EqualTo('password', message = "Паролі не співпадають!")])
    submit = SubmitField('Confirm') 
    