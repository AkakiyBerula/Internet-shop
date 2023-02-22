from flask import url_for, render_template, flash, request, redirect, abort, current_app, session
from .forms import ProductForm, ProductTypeForm, RatingForm, BuyForm, SortForm
from .models import Products, Producttypes, Ratings
from ..auth.models import User
from .. import db
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import func
from . import products_blueprint
from datetime import datetime
import os
import secrets
from PIL import Image

def save_product(form, product):
    form.code.data = product.code
    form.name.data = product.name
    form.is_on_storage.data = product.is_on_storage
    form.variety.data = product.variety
    form.variety.data = product.variety
    form.price.data = product.price
    form.info.data = product.info
    form.type.data = product.type
    return form

@products_blueprint.route('/', methods=['GET', 'POST'])
def product_view_info():
    form = SortForm()
    products = Products.query.order_by(Products.name).all()
    if form.validate_on_submit():
        if form.sort_field.data == 1:
            products = Products.query.order_by(Products.name).all()
        if form.sort_field.data == 2:
            products = Products.query.order_by(Products.date).all()
        if form.sort_field.data == 3:
            products = Products.query.order_by(Products.date.desc()).all()
        if form.sort_field.data == 4:
            products = Products.query.order_by(Products.price).all()
        if form.sort_field.data == 5:
            products = Products.query.order_by(Products.price.desc()).all()
    return render_template('product_list.html', products_list = products, form = form)

@products_blueprint.route('/', methods=['GET', 'POST'])
def category_search(id):
    product_type = Producttypes.query.get_or_404(id)
    products = Products.query.order_by(Products.name).filter(type_id = id).all()
    form = ProductForm()
    products = Products.query.order_by(Products.name).all()
    return render_template('product_list.html', products_list = products, form = form)


@products_blueprint.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    form = ProductForm()
    form.type.choices = [(type_c.type_id, type_c.type) for type_c in Producttypes.query.all()]
    if form.validate_on_submit():
        if form.image_file.data:
            picture_file = save_picture(form.image_file.data)
            image = picture_file
        else:
            image = "postdefault.png"
        product_data = Products(code = form.code.data, 
                            name = form.name.data,
                            is_on_storage = True if int(form.variety.data) > 0 else False,
                            variety = form.variety.data,
                            price = form.price.data,
                            info = form.info.data,
                            image_file = image,
                            type = form.type.data,
                            user_id = current_user.id)
        db.session.add(product_data)
        db.session.commit()
        return redirect(url_for('products.product_view_info'))
    products = Products.query.order_by(Products.code).all()
    return render_template('add_product.html', products_list = products, form = form)


def count_rating(id):
    avg_rating = db.session.query(func.avg(Ratings.rating).label('average')).filter(Ratings.product_id == id).first()
    return avg_rating.average



@products_blueprint.route('/<id>', methods=['GET', 'POST'])
def product_detail_info(id):
    product = Products.query.get_or_404(id)
    type = Producttypes.query.get_or_404(product.type)
    if current_user.is_authenticated:
        your_rating = Ratings.query.filter(Ratings.product_id == id, Ratings.user_id == current_user.id).first()
    else:
        your_rating = ""
    rateform = RatingForm()
    ratings_list = db.session.query(Ratings, User).\
        join(User, User.id == Ratings.user_id).\
            filter(Ratings.product_id == id).order_by(Ratings.date.desc()).all()
    res_rating = count_rating(id)
    if rateform.validate_on_submit():
        if your_rating == None:
            your_rating = Ratings(
            user_id = current_user.id,
            product_id = id,
            rating = rateform.rate.data,
            comment = rateform.comment.data
        )
        else:
            if rateform.rate.data != -1.0:
                your_rating.rating = rateform.rate.data
            else:
                your_rating.rating = None
            your_rating.comment = rateform.comment.data
            your_rating.date = db.func.now()

        db.session.add(your_rating)
        db.session.commit()
        flash('Ваш відгук був оновлений!', category='access')
        return redirect(url_for('products.product_detail_info', id=id)
                        )
    return render_template('product_details.html',
                            rateform = rateform, 
                            product = product, 
                            type = type, 
                            your_rating = your_rating,
                            ratings_list = ratings_list,
                            res_rating = res_rating)


@products_blueprint.route('/<id>/remove_product', methods=['GET', 'POST'])
def remove_product(id):
    product = Products.query.get_or_404(id)
    ratings = Ratings.query.filter_by(product_id = id).all()
    print(ratings)
    if current_user.usertype != "User":
        for rating in ratings:
            db.session.delete(rating)
        db.session.delete(product)
        db.session.commit()
        return redirect(url_for('products.product_view_info'))
    flash('Ви не маєте прав на вилучення продукту', category='warning')
    return redirect(url_for('products.product_detail_info', id = product.user_id))


@products_blueprint.route('/<id>/edit_product', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    product = Products.query.get_or_404(id)
    if current_user.usertype == "User":
        flash('Ви не можете редагувати товар!', category='warning')
        return redirect(url_for('products.product_detail_info', products = product, id = id))
    form = ProductForm()
    form.type.choices = [(product.type_id, product.type) for product in Producttypes.query.all()]
    print(form.variety.data)
    if form.validate_on_submit():

        product.code = form.code.data
        product.name = form.name.data
        product.is_on_storage = True if int(form.variety.data) > 0 else False
        product.variety = form.variety.data
        product.price = form.price.data
        product.info = form.info.data
        if form.image_file.data:
            picture_file = save_picture(form.image_file.data)
            product.image_file = picture_file
        else:
            product.image_file = "postdefault.png"
        product.type = form.type.data

        db.session.add(product)
        db.session.commit()

        flash('Дані продукту були оновлені', category='access')
        return redirect(url_for('products.product_detail_info', id=id))
    else:
        form = save_product(form, product)
    return render_template('add_product.html', form=form, products_list = product)

@products_blueprint.route('/product_types', methods=['GET', 'POST'])
@login_required
def type_info():
    form = ProductTypeForm()
    types = Producttypes.query.order_by(Producttypes.type_id).all()
    print(types)
    for type in types:
        print(type.type)
    return render_template('product_types.html', product_types = types, form = form, user_id = current_user.id)


@products_blueprint.route('/add_type', methods=['GET', 'POST'])
@login_required
def add_type():
    form = ProductTypeForm()
    if form.validate_on_submit():
        type = Producttypes(type = form.type.data)
        db.session.add(type)
        db.session.commit()
        flash('Новий тип товару добавлено')
        return redirect(url_for('products.type_info'))

    product_types = Producttypes.query.all()
    return render_template('add_type.html', product_types=product_types, form=form)


@products_blueprint.route('<id>/update_type/', methods=['GET', 'POST'])
@login_required
def update_type(id):
    type = Producttypes.query.get_or_404(id)
    form = ProductTypeForm()
    if form.validate_on_submit():
        type.type = form.type.data

        db.session.add(type)
        db.session.commit()
        flash('Тип договору оновлений')
        return redirect(url_for('products.type_info'))

    form.type.data = type.type
    product_types = Producttypes.query.all()
    return render_template('add_type.html', product_types = product_types, form=form)


@products_blueprint.route('/<id>/delete_type', methods=['GET'])
@login_required
def delete_type(id):
    type = Producttypes.query.get_or_404(id)
    db.session.delete(type)
    db.session.commit()
    flash('Тип товарів вилучено', category='access')
    return redirect(url_for('products.type_info'))


@products_blueprint.route('/<id>/product', methods=['GET'])
@login_required
def delete_rate(id):
    comment = Ratings.query.filter_by(user_id = current_user.id, product_id = id).first()
    db.session.delete(comment)
    db.session.commit()
    flash('Ваш відгук був видалений!', category='access')
    return redirect(url_for('products.product_detail_info', id = id))

@products_blueprint.route('/<id>/buy', methods=['POST', 'GET'])
@login_required
def make_order(id):
    form = BuyForm()
    product = Products.query.get_or_404(id)
    type = Producttypes.query.get_or_404(product.type)
    if form.validate_on_submit():
        if int(form.counter.data) >= product.variety:
            flash('Занадто велика покупка! Перевірте дані!', category = "warning")
        else:
            session["form_counter"] = form.counter.data
            session["form_address"] = form.address.data
            return redirect(url_for('products.buy_product', id = product.id))
    return render_template('buy_product.html', 
                            title = "Купівля товару",
                            form = form, 
                            product = product, 
                            product_id = id)

@products_blueprint.route('/conf_buy/<id>', methods=['POST', 'GET'])
@login_required
def buy_product(id):
    forms = BuyForm()
    product = Products.query.get(id)
    forms.counter.data = session["form_counter"]
    forms.address.data = session["form_address"]
    print(product)
    amount = int(forms.counter.data) * product.price
    if forms.validate_on_submit():
        product.variety -= product.variety - amount
        print(product.variety)
        db.session.add(product)
        db.session.commit()
        flash("Покупка успішно виконана", category = "")
        return redirect(url_for('products.product_detail_info', id = product.id))
    return render_template('place_order.html', form = forms, product = product, amount = amount)
    


@products_blueprint.route('/comments', methods=['GET'])
@login_required
def comments_view():
    ratings_list = db.session.query(Ratings, User, Products).\
        join(User, User.id == Ratings.user_id).\
        join(Products, Products.id == Ratings.product_id).\
        order_by(Ratings.date.desc()).all()
    return render_template('comments.html',
                            title = "Відгуки",
                            ratings_list = ratings_list)


@products_blueprint.route('/products/<type>', methods=['GET', 'POST'])
def product_info_type(type):
    form = SortForm()
    products = Products.query.filter_by(type = type).order_by(Products.name).all()
    if form.validate_on_submit():
        if form.sort_field.data == 1:
            products = Products.query.filter_by(type = type).order_by(Products.name).all()
        if form.sort_field.data == 2:
            products = Products.query.filter_by(type = type).order_by(Products.date).all()
        if form.sort_field.data == 3:
            products = Products.query.filter_by(type = type).order_by(Products.date.desc()).all()
        if form.sort_field.data == 4:
            products = Products.query.filter_by(type = type).order_by(Products.price).all()
        if form.sort_field.data == 5:
            products = Products.query.filter_by(type = type).order_by(Products.price.desc()).all()
    return render_template('pr_list_by_type.html', products_list = products, form = form, type_id = type)  

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    name, ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + ext
    path_of_picture = os.path.join(current_app.root_path, 'static/product_pics', picture_fn)
    output_size = (250, 250)
    image = Image.open(form_picture)
    image.thumbnail(output_size)
    image.save(path_of_picture)
    return picture_fn