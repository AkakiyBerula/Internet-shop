from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, FloatField, BooleanField, TextAreaField, FileField, HiddenField
from wtforms.fields import DateField 
from wtforms.validators import Length, DataRequired, InputRequired, Regexp
from flask_wtf.file import FileField, FileAllowed

class ProductForm(FlaskForm):
    code = StringField("Введіть код продукту",validators=[
                        InputRequired(message="Це поле обов'язкове"),
                        Regexp(r'^[0-9]{8}$', 0,
                        message="Код товару має складатись з 8 цифр")], )
    name = StringField('Назва товару', 
                        validators=[InputRequired(message="Це поле обов'язкове"), 
                        Length(max=120, message="Поле має мати не більше 120 символів")])
    is_on_storage = BooleanField("Чи є продукт в наявності")
    variety = StringField("Кількість товару", validators=[
                        Regexp(r'[0-9]{0,6}', 0,
                        message="Неправильно введене значення товару")])
    price = StringField('Вартість товару, що продається', 
                    validators=[
                    DataRequired(message="Це поле обов'язкове"),
                    Regexp(r'[0-9]*\.[0-9]{2}$', 0,
                    message="Сума повинна мати дробове значення дві цифри після коми")])
    info = TextAreaField('Введіть опис товару: ', validators=[Length(max=2500)])
    image_file = FileField('Зображення поста', validators=[FileAllowed(['jpg', 'png'])]) 
    type = SelectField('Оберіть тип товару:', coerce = int)
    submit = SubmitField('Оновити інформацію протовар')


class ProductTypeForm(FlaskForm):
    type = StringField('Ввести тип товару', validators=[DataRequired(message="Це поле обов'язкове"), Length(min=0, max=40)])
    submit = SubmitField('Виконати')

class RatingForm(FlaskForm):
    rate = SelectField(u'Оцініть товар', 
                        coerce=float, 
                        choices=[(-1.0, "-"), (10.0, "10"), (9.0, "9"), (8.0, "8"), (7.0, "7"), (6.0, "6"), 
                        (5.0, "5"), (4.0, "4"), (3.0, "3"), (2.0, "2"), (1.0, "1"), (0.0, "0")])
    comment = TextAreaField("Напишіть ваш відгук")
    submit = SubmitField('Залишити відгук')

class BuyForm(FlaskForm):
    counter = StringField(u'Введіть кількість товару для покупки', validators=[
                        Regexp(r'[0-9]{0,8}', 0,
                        message="Неправильно введене значення товару")])
    address = StringField('Введіть адресу')
    submit = SubmitField('Придбати товар')




class SortForm(FlaskForm):
    sort_field = SelectField(u'Відсортувати товари за:', 
                        coerce=int, choices=[
                            (1, "За назвою товару в алфавітному порядку"), 
                            (2, "За датою в порядку зростання"), 
                            (3, "За датою в порядку спадання"), 
                            (4, "За вартістю в порядку зростання"), 
                            (5, "За вартістю в порядку спадання")
                        ])
    submit = SubmitField("Відсортувати")
    