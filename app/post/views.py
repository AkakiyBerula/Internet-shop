from flask import url_for, render_template, flash, request, redirect, abort, current_app
from .forms import PostsForm, CategoryPostForm, SortPostsForm
from .models import Posts, Category
from .. import db
from ..auth.models import User
from flask_login import login_user, current_user, logout_user, login_required
from . import posts_blueprint
from sqlalchemy import func
import os
import secrets
from PIL import Image
from datetime import datetime


@posts_blueprint.route('/', methods=['GET', 'POST'])
def view_posts():
    form = SortPostsForm()
    posts = db.session.query(Posts, User.username).\
        join(User, User.id == Posts.user_id).order_by(Posts.title).all()
    if form.validate_on_submit():
        if form.sort_posts.data == 1:
            posts = db.session.query(Posts, User.username).\
                join(User, User.id == Posts.user_id).order_by(Posts.title).all()
        if form.sort_posts.data == 2:
            posts = db.session.query(Posts, User.username).\
                join(User, User.id == Posts.user_id).order_by(Posts.created).all()
        if form.sort_posts.data == 3:
            posts = db.session.query(Posts, User.username).\
                join(User, User.id == Posts.user_id).order_by(Posts.title).all()
        if form.sort_posts.data == 4:
            posts = db.session.query(Posts, User.username).\
                join(User, User.id == Posts.user_id).order_by(User.username).all()
    return render_template('posts_crud.html', posts_list = posts, form = form)


@posts_blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostsForm()
    form.category.choices = [(category.id, category.name) for category in Category.query.all()]
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            image = picture_file
        else:
            image = "postdefault.jpg"
            
        new_post = Posts(title = form.title.data, 
                        text = form.text.data,
                        image_file = image,
                        type = form.type.data,
                        user_id = current_user.id,
                        category_id=form.category.data)

        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('posts.view_posts'))
    posts = Posts.query.all()
    return render_template('create_post.html', posts = posts, form = form)


@posts_blueprint.route('/<id>', methods=['GET', 'POST'])
@login_required
def show_post(id):
    print(id)
    post = Posts.query.get_or_404(id)
    category_name = Category.query.get_or_404(post.category_id)
    username = User.query.get_or_404(post.user_id)
    return render_template('post_details.html', category_name = category_name, post = post, username = username)


@posts_blueprint.route('/<id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(id):
    post = Posts.query.get_or_404(id)
    if current_user.id == post.user_id:
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('posts.view_posts'))
    flash('Це не ваш пост', category='warning')
    return redirect(url_for('posts.show_post', id = post.user_id))


@posts_blueprint.route('/<id>/edit', methods=['GET', 'POST'])
def edit_post(id):
    post = Posts.query.get_or_404(id)
    if current_user.id != post.user_id:
        flash('Це пост не є вашим!', category='warning')
        return redirect(url_for('posts.show_post', posts = post, id = id))
    form = PostsForm()
    form.category.choices = [(category.id, category.name) for category in Category.query.all()]
    if form.validate_on_submit():
        post.title = form.title.data
        post.text = form.text.data
        post.type = form.type.data
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            post.image_file = picture_file
        else:
            post.image_file = "postdefault.jpg"
        post.enabled = form.enabled.data
        post.category_id = form.category.data

        db.session.add(post)
        db.session.commit()

        flash('Пост був оновлений', category='access')
        return redirect(url_for('posts.view_posts', id = id))
    form.title.data = post.title 
    form.text.data = post.text
    form.type.data = post.type
    form.enabled.data = post.enabled
    form.category.data = post.category_id

    image_file = url_for("static", filename = "posts_pics/" + post.image_file)
    return render_template('create_post.html', form = form, posts_list = post, image_file = image_file)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    name, ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + ext
    path_of_picture = os.path.join(current_app.root_path, 'static/posts_pics', picture_fn)
    output_size = (250, 250)
    image = Image.open(form_picture)
    image.thumbnail(output_size)
    image.save(path_of_picture)
    return picture_fn

@posts_blueprint.route('/categories', methods=['GET', 'POST'])
@login_required
def categories_list():
    form = CategoryPostForm()
    categories = Category.query.order_by(Category.id).all()
    return render_template('categories.html', categories = categories, form = form, user_id = current_user.id)


@posts_blueprint.route('/create_category', methods=['GET', 'POST'])
@login_required
def create_category():
    form = CategoryPostForm()

    if form.validate_on_submit():
        category = Category(name = form.category_name.data)
        db.session.add(category)
        db.session.commit()
        flash('Нова категорія добавлена в таблицю')
        return redirect(url_for('posts.categories_list'))

    categories = Category.query.all()
    return render_template('add_category.html', categories = categories, form = form)


@posts_blueprint.route('<id>/update_category', methods=['GET', 'POST'])
@login_required
def update_category(id):
    category = Category.query.get_or_404(id)
    form = CategoryPostForm()
    if form.validate_on_submit():
        category.name = form.category_name.data

        db.session.add(category)
        db.session.commit()
        flash('Назва категорії була оновлена')
        return redirect(url_for('posts.categories_list'))

    form.category_name.data = category.name
    categories = Category.query.all()
    return render_template('add_category.html', categories = categories, form=form)


@posts_blueprint.route('/<id>/delete_category', methods=['GET'])
@login_required
def delete_category(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    flash('Категорія була вилучена', category='access')
    return redirect(url_for('posts.categories_list'))