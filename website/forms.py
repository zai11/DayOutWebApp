
from inspect import CO_NESTED
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField,SubmitField, StringField, PasswordField, BooleanField
from wtforms.fields.core import DateField, RadioField, SelectField, TimeField
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
class EventForm(FlaskForm):
    image = FileField('Image Header', validators=[FileRequired(message='Image can not be empty'),
                                        FileAllowed(ALLOWED_FILE, message='Only support png, jpg, JPG, PNG, bmp')])
    title = StringField('Title', validators=[InputRequired()])
    host = StringField('Host', validators=[InputRequired()])
    type = SelectField('Type', validators=[InputRequired()],
                                        choices=[('N/A', '-'), ('1', 'One'), ('2', 'Two'), ('3', 'Three')])
    venue = StringField('Venue', validators=[InputRequired()])
    category = SelectField('Category', validators=[InputRequired()],
                                        choices=[('N/A', '-'), ('1', 'One'), ('2', 'Two'), ('3', 'Three')])
    frequency = RadioField('Frequency', validators=[InputRequired()],
                                        choices=[('Once'), ('Weekly'), ('Monthly'), ('Yearly')])
    start_date = DateField('Start Date', validators=[InputRequired()], format='%d-%m-%Y')
    end_date = DateField('End Date', validators=[InputRequired()], format='%d-%m-%Y')
    start_time = TimeField('Start Time', validators=[InputRequired()], format='%H:%M')
    end_time = TimeField('End Time', validators=[InputRequired()], format='%H:%M')
    timezone = SelectField('Timezone', validators=[InputRequired()],
                                        choices=[('N/A', '-'), 
                                            ('1', '(UTC+8:00) Perth'), 
                                            ('2', '(UTC+9:30) Adelaide, Darwin'), 
                                            ('3', '(UTC+10:00) Brisbane'),
                                            ('4', '(UTC+10:00) Hobart, Canberra, Melbourne, Sydney')])
    description = TextAreaField('Description', validators=[InputRequired()])
    featured_headline = TextAreaField('Featured Headline', validators=[InputRequired()])
    price = StringField('Price (AUD)', validators=[InputRequired()])
    quantity = StringField('Quantity (AUD)', validators=[InputRequired()])
    status = RadioField('Event Status', validators=[InputRequired()],
                                        choices=[('0', 'Upcoming'), ('1', 'Inactive'), ('2', 'Booked'), ('3', 'Cancelled')])
    submit=SubmitField("Submit")
