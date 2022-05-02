from tokenize import String
from flask_wtf import FlaskForm
from sqlalchemy import Float
from wtforms import StringField, DateField, SelectField, SubmitField, FloatField
# from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from grocery_app.models import GroceryStore, ItemCategory
from wtforms.validators import DataRequired, Length, URL

class GroceryStoreForm(FlaskForm):
    """Form for adding/updating a GroceryStore."""
    # TODO: Add the following fields to the form class:
    # - title - StringField
    title = StringField('Name Of Store', validators=[DataRequired(), Length(min=2, max=100)])
    # - address - StringField
    address = StringField("Address of Store")
    # - submit button
    submit = SubmitField("Create New Store")
    

class GroceryItemForm(FlaskForm):
    """Form for adding/updating a GroceryItem."""

    # TODO: Add the following fields to the form class:
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max = 100)])
    # - name - StringField
    price = FloatField("Price")
    # - price - FloatField
    category = SelectField("Category", choices=ItemCategory.choices())
    # - category - SelectField (specify the 'choices' param)
    photo_url = StringField("Photo of Product URL")
    # - photo_url - StringField
    store = QuerySelectField("Store", query_factory=lambda: GroceryStore.query, allow_blank=False)
    # - store - QuerySelectField (specify the `query_factory` param)
    submit = SubmitField("Create New Product")
    # - submit button
    
