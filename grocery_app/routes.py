from ast import Store
from cgi import print_exception
from ctypes import addressof
from dataclasses import dataclass
from unicodedata import category
from venv import create
from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from grocery_app.models import GroceryStore, GroceryItem, User, UserMixin, shopping_list_table
from grocery_app.forms import GroceryStoreForm, GroceryItemForm, SignUpForm, LoginForm
# Import app and db from events_app package so that we can run app
from grocery_app.extensions import app, db
from flask_login import login_user, logout_user, current_user, login_required
from grocery_app import bcrypt

main = Blueprint("main", __name__)
auth = Blueprint("auth", __name__)

##########################################
#           Routes                       #
##########################################

@main.route('/')
def homepage():
    all_stores = GroceryStore.query.all()
    return render_template('home.html', all_stores=all_stores)

@main.route('/new_store', methods=['GET', 'POST'])
@login_required
def new_store():

    form = GroceryStoreForm()
    if form.validate_on_submit():
        create_new_store = GroceryStore(
            title = form.title.data,
            address = form.address.data,
            created_by = current_user
        )
        db.session.add(create_new_store)
        db.session.commit()
        flash("You have created a new Store")
        return redirect(url_for("main.store_detail", store_id=create_new_store.id))

    return render_template('new_store.html', form=form)

@main.route('/new_item', methods=['GET', 'POST'])
@login_required
def new_item():

    form = GroceryItemForm()
    if form.validate_on_submit():
        create_new_item = GroceryItem(
            name = form.name.data,
            price = form.price.data,
            category = form.category.data,
            photo_url = form.photo_url.data,
            store = form.store.data,
            created_by = current_user
            )
        db.session.add(create_new_item)
        db.session.commit()
        flash("You have created a new Item")
        return redirect(url_for("main.store_detail", store_id=create_new_item.store_id))

    return render_template('new_item.html', form=form)

@main.route('/store/<store_id>', methods=['GET', 'POST'])
def store_detail(store_id):
    store = GroceryStore.query.get(store_id)

    form = GroceryStoreForm(obj=store)
    
    if form.validate_on_submit():
        store.title = form.title.data
        store.address = form.address.data
        db.session.add(store)
        db.session.commit()
        flash("Grocery Store Updated.")
        return redirect(url_for('main.store_detail', store_id=store.id))

    return render_template('store_detail.html', store=store, form=form)

@main.route('/item/<item_id>', methods=['GET', 'POST'])
def item_detail(item_id):
    item = GroceryItem.query.get(item_id)

    form = GroceryItemForm(obj=item)
    if form.validate_on_submit():
        item.name = form.name.data
        item.price = form.price.data
        item.category = form.category.data
        item.photo_url = form.photo_url.data
        item.store = form.store.data

        db.session.add(item)
        db.session.commit()
        flash("You have successfully added the item to the store.")
        return redirect(url_for('main.item_detail', item_id=item.id))        

    return render_template('item_detail.html', item=item, form=form)

@main.route('/add_to_shopping_list/<item_id>', methods=['POST'])
@login_required
def add_to_shopping_list(item_id):
    item = GroceryItem.query.get(item_id)
    current_user.shopping_list_users.append(item)
    db.session.add(current_user)
    db.session.commit()
    flash("Added item to cart")
    return redirect(url_for('main.shopping_list', item_id=item.id)) 

@main.route('/shopping_list')
@login_required
def shopping_list():
    shopping_list = current_user.shopping_list_users
    return render_template("shopping_list.html", shopping_list=shopping_list)

@main.route('/delete_to_shopping_list/<item_id>', methods=['POST'])
@login_required
def delete_to_shopping_list(item_id):
    db.session.query(shopping_list_table).filter_by(item_id=item_id).delete()
    # item = GroceryItem.query.get(item_id)
    # current_user.shopping_list_users.pop(item)
    # db.session.add(current_user)
    db.session.commit()
    flash("Deleted item from cart")
    return redirect(url_for('main.shopping_list')) 

#STUDENTS DELETE
@main.route('/students/<student_id>/delete', methods=['POST'])
def students_delete(student_id):
    Student.query.filter_by(id=student_id).delete()
    db.session.commit()
    return redirect(url_for('main.home'))

# AUTH
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    print('in signup')
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash('Account Created.')
        print('created')
        return redirect(url_for('auth.login'))
    print(form.errors)
    return render_template('signup.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user, remember=True)
        next_page = request.args.get('next')
        return redirect(next_page if next_page else url_for('main.homepage'))
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.homepage'))


# source venv/bin/activate
# which python
# python3 app.py
# export FLASK_ENV=development
# export FLASK_DEBUG=1
# flask run
