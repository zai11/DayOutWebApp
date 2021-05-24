
from inspect import CO_NESTED
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField,SubmitField, StringField, PasswordField, BooleanField
from wtforms.fields.core import DateTimeField, IntegerField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from flask_wtf.file import FileRequired, FileField, FileAllowed


ALLOWED_FILE = {'png', 'jpg', 'PNG', 'JPG'}


#creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    phone_number = StringField("Phone Number", validators=[InputRequired()])
    address = StringField("Address", validators=[InputRequired()])
    is_admin = BooleanField("Is Admin", validators=[])
    #add buyer/seller - check if it is a buyer or seller hint : Use RequiredIf field

    #linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(), EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")

    #submit button
    submit = SubmitField("Register")

# this is the event form
""" class EventForm(FlaskForm):
    eventname = StringField('Event Name', validators=[InputRequired('Please enter a event name')])
    headline = StringField('Headliner', validators=[InputRequired('What is the featured act?')])
    description = TextAreaField('Description', validators=[InputRequired()])
    date = DateTimeField('Date and Time', validators=[InputRequired()])
    price = IntegerField('Cost per ticket', [validators.NumberRange(min=0, max=100)], widget=NumberInput())
    image = FileField('Cover Image', validators=[FileRequired(message='Image can not be empty'), FileAllowed(ALLOWED_FILE, message='Only supports png, jpg, JPG, PNG')])
    submit = SubmitField("Create") """
