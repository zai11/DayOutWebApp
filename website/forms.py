
from inspect import CO_NESTED
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField,SubmitField, StringField, PasswordField, BooleanField, IntegerField, DecimalField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.fields.core import RadioField, SelectField
from wtforms.validators import InputRequired, Length, Email, EqualTo, NumberRange
from flask_wtf.file import FileRequired, FileField, FileAllowed
from wtforms import HiddenField


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
class EventForm(FlaskForm):
    image = FileField('Image Header', validators=[FileRequired(message='Image can not be empty'),
                                        FileAllowed(ALLOWED_FILE, message='Only support png, jpg, JPG, PNG, bmp')])
    title = StringField('Title', validators=[InputRequired()])
    host = StringField('Host', validators=[InputRequired()])
    venue = StringField('Venue', validators=[InputRequired()])
    category = SelectField('Category', validators=[InputRequired()],
                                        choices=[('N/A', '-'), ('Jazz', 'Jazz'), ('Country', 'Country'), ('Classical', 'Classical'), ('Hip-Hop', 'Hip-Hop'), ('Electronic', 'Electronic')])
    start_date = DateTimeLocalField('Start Time', validators=[InputRequired()], format='%Y-%m-%d %H:%M:%S')
    end_date = DateTimeLocalField('End Time', validators=[InputRequired()], format='%Y-%m-%d %H:%M:%S')
    timezone = SelectField('Timezone', validators=[InputRequired()],
                                        choices=[('N/A', '-'), 
                                            ('Perth', '(UTC+8:00) Perth'), 
                                            ('Adelaide, Darwin', '(UTC+9:30) Adelaide, Darwin'), 
                                            ('Brisbane', '(UTC+10:00) Brisbane'),
                                            ('Hobart, Canberra, Melbourne, Sydney', '(UTC+10:00) Hobart, Canberra, Melbourne, Sydney')])
    description = TextAreaField('Description', validators=[InputRequired()])
    featured_headline = TextAreaField('Featured Headline', validators=[InputRequired()])
    price = DecimalField('Price (AUD)', validators=[InputRequired(), NumberRange(min=0, message="Please enter a valid price")])
    quantity = IntegerField('Quantity (AUD)', validators=[InputRequired(), NumberRange(min=0, message="Please enter a valid quantity")])
    status = RadioField('Event Status', validators=[InputRequired()],
                                        choices=[('Upcoming', 'Upcoming'), ('Inactive', 'Inactive'), ('Booked', 'Booked'), ('Cancelled', 'Cancelled')])
    submit=SubmitField("Submit")

class CommentForm(FlaskForm):
    text = TextAreaField('Comment', validators=[InputRequired()])  
    submit = SubmitField('Comment')

class BookingForm(FlaskForm):
    tickets_booked = IntegerField('Quantity of Tickets', validators=[InputRequired()])
    user = HiddenField('')
    event = HiddenField('')
    submit=SubmitField("Submit")
    



