from ast import Store
from cgi import print_exception
from ctypes import addressof
from dataclasses import dataclass
from unicodedata import category
from venv import create
from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from grocery_app.models import GroceryStore, GroceryItem
from grocery_app.forms import GroceryStoreForm, GroceryItemForm
# Import app and db from events_app package so that we can run app
from grocery_app.extensions import app, db

main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################

@main.route('/')
def homepage():
    all_stores = GroceryStore.query.all()
    print(all_stores)
    return render_template('home.html', all_stores=all_stores)

@main.route('/new_store', methods=['GET', 'POST'])
def new_store():
    # TODO: Create a GroceryStoreForm

    # TODO: If form was submitted and was valid:
    # - create a new GroceryStore object and save it to the database,
    # - flash a success message, and
    # - redirect the user to the store detail page.
    form = GroceryStoreForm()
    if form.validate_on_submit():
        create_new_store = GroceryStore(
            title = form.title.data,
            address = form.address.data
        )
        db.session.add(create_new_store)
        db.session.commit()
        flash("You have created a new Store")
        return redirect(url_for("main.store_detail", store_id=create_new_store.id))
    
    # TODO: Send the form to the template and use it to render the form fields
    return render_template('new_store.html', form=form)

@main.route('/new_item', methods=['GET', 'POST'])
def new_item():
    # TODO: Create a GroceryItemForm
    form = GroceryItemForm()
    if form.validate_on_submit():
        create_new_item = GroceryItem(
            name = form.name.data,
            price = form.price.data,
            category = form.category.data,
            photo_url = form.photo_url.data,
            store = form.store.data
            )
        db.session.add(create_new_item)
        db.session.commit()
        flash("You have created a new Item")
        return redirect(url_for("main.store_detail", store_id=create_new_item.store_id))
    
    # TODO: If form was submitted and was valid:
    # - create a new GroceryItem object and save it to the database,
    # - flash a success message, and
    # - redirect the user to the item detail page.

    # TODO: Send the form to the template and use it to render the form fields
    return render_template('new_item.html', form=form)

@main.route('/store/<store_id>', methods=['GET', 'POST'])
def store_detail(store_id):
    store = GroceryStore.query.get(store_id)
    # TODO: Create a GroceryStoreForm and pass in `obj=store`
    form = GroceryStoreForm(obj=store)
    
    if form.validate_on_submit():
        store.title = form.title.data
        store.address = form.address.data
        db.session.add(store)
        db.session.commit()
        flash("Grocery Store Updated.")
        return redirect(url_for('main.store_detail', store_id=store.id))

    # TODO: If form was submitted and was valid:
    # - update the GroceryStore object and save it to the database,
    # - flash a success message, and
    # - redirect the user to the store detail page.

    # TODO: Send the form to the template and use it to render the form fields
    # store = GroceryStore.query.get(store_id)
    return render_template('store_detail.html', store=store, form=form)

@main.route('/item/<item_id>', methods=['GET', 'POST'])
def item_detail(item_id):
    item = GroceryItem.query.get(item_id)
    # TODO: Create a GroceryItemForm and pass in `obj=item`
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
    # TODO: If form was submitted and was valid:
    # - update the GroceryItem object and save it to the database,
    # - flash a success message, and
    # - redirect the user to the item detail page.

    # TODO: Send the form to the template and use it to render the form fields
    # item = GroceryItem.query.get(item_id)
    return render_template('item_detail.html', item=item, form=form)


# source venv/bin/activate
# which python
# python3 app.py
# export FLASK_ENV=development
# export FLASK_DEBUG=1
# flask run
