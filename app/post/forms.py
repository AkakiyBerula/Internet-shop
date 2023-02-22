from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, BooleanField
from wtforms.validators import Length, DataRequired, InputRequired
from flask_wtf.file import FileField, FileAllowed


class PostsForm(FlaskForm):
    title = StringField('Введіть заголовок поста', validators=[InputRequired(), Length(min=2, max=80)])
    text = TextAreaField('Введіть текст поста', validators=[Length(max=2500)])
    picture = FileField('Зображення поста', validators=[FileAllowed(['jpg', 'png'])])
    type = SelectField('Оберіть тип публікації', choices=[('News', 'News'), ('Publication', 'Publication'), ('Other', 'Other')])
    category = SelectField(u'Оберіть категорію', coerce=int)
    enabled = BooleanField('Enabled')
    submit = SubmitField('Підтвердити')

class CategoryPostForm(FlaskForm):
    category_name = StringField('Ввести тип категорії', validators=[DataRequired(message="Це поле обов'язкове"), Length(min=0, max=40)])
    submit = SubmitField('Виконати')

class SortPostsForm(FlaskForm):
    sort_posts = SelectField(u'Відсортувати товари за:', 
                        coerce=int, choices=[
                            (1, "За назвою поста"), 
                            (2, "За датою в порядку зростання"), 
                            (3, "За датою в порядку спадання"), 
                            (4, "За нікнеймом користувача")
                        ])
    submit = SubmitField("Відсортувати")
    