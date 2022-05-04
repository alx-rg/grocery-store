from tokenize import String
from flask_wtf import FlaskForm
from sqlalchemy import Float
from wtforms import StringField, DateField, SelectField, SubmitField, FloatField, PasswordField
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from grocery_app.models import GroceryStore, ItemCategory, User
from wtforms.validators import DataRequired, Length, URL, ValidationError
# from grocery_app import bcrypt
from grocery_app import bcrypt

class GroceryStoreForm(FlaskForm):
    """Form for adding/updating a GroceryStore."""
    title = StringField('Name Of Store', validators=[DataRequired(), Length(min=2, max=100)])
    address = StringField("Address of Store")
    submit = SubmitField("Create New Store")
    
class GroceryItemForm(FlaskForm):
    """Form for adding/updating a GroceryItem."""
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max = 100)])
    price = FloatField("Price")
    category = SelectField("Category", choices=ItemCategory.choices())
    photo_url = StringField("Photo of Product URL")
    store = QuerySelectField("Store", query_factory=lambda: GroceryStore.query, allow_blank=False)
    submit = SubmitField("Create New Product")

# SIGN UP BELOW ++++++++++++++++++++++++++++++++++++++++++++++

class SignUpForm(FlaskForm):
    username = StringField('User Name',
        validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('User Name',
        validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError('No user with that username. Please try again.')

    def validate_password(self, password):
        user = User.query.filter_by(username=self.username.data).first()
        if user and not bcrypt.check_password_hash(
                user.password, password.data):
            raise ValidationError('Password doesn\'t match. Please try again.')