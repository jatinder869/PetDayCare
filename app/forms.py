from flask_wtf import FlaskForm
from wtforms import StringField, TimeField, SelectField, DateField, PasswordField, SubmitField, BooleanField, \
    IntegerField, TextAreaField,HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import phonenumbers
import datetime
"""The file contains forms of type FlaskForm which are basically implemented as html forms when rendered in front end.
They help us to define validations for a  field in a particular form and also raise errors which are caught by jinja module
"""

"""
This is a class for the registration form which is used when we need to register a new customer
Implemented in /register route
"""
class RegistrationForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])

    full_name = StringField('Full Name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    address = StringField('Address',
                          validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    # Function for validating phone number
    def validate_phone(form, field):
        if len(field.data) < 9 :
            raise ValidationError('Invalid phone number.')
        try:
            input_number = phonenumbers.parse(field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')
        except:
            input_number = phonenumbers.parse("+1" + field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')

    # Function for validating password
    def validate_password(self,field):
        if len(field.data) < 8 :
            raise ValidationError('Please atleast 8 characters.')
        one_upper = False
        for i in field.data:
            if str(i).isalpha():
                if str(i).isupper():
                    one_upper = True
        if not one_upper:
            raise ValidationError('The password should have atleast one upper case letter')

"""
This is a class to containing user update form which is used when user needs to update his personal info
like name , address and phone

Implemented in /profile/dashboard route
"""
class UserUpdateForm(FlaskForm):
    full_name = StringField('Full Name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    address = StringField('Address',
                          validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    submit = SubmitField('Update')

    # Function for validating phone number
    def validate_phone(form, field):
        if len(field.data) < 9 :
            raise ValidationError('Invalid phone number.')
        try:
            input_number = phonenumbers.parse(field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')
        except:
            input_number = phonenumbers.parse("+1" + field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')

"""
This is a class for the Login form which is used to login a customer
Implemented in /login route
"""
class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

"""
This is a class for the Add pet form which is used to register a new pet for the user
Implemented in /profile/addpets route
"""
class PetForm(FlaskForm):
    name = StringField('name',
                       validators=[DataRequired(), Length(min=2, max=20)])

    type = SelectField('Type',choices=["Dog","Cat"],
                       validators=[DataRequired(), Length(min=2, max=20)])

    instruction = TextAreaField('instruction',
                                validators=[DataRequired(), Length(min=2, max=200)])
    submit = SubmitField('Add Pet')

"""
This is a class for the Add Card form which is used to register a new card for the user
Implemented in /profile/addcard route
"""
class CardForm(FlaskForm):
    cardnum = StringField('Card Number',
                           validators=[DataRequired()])
    expiry = StringField('Expiry(MM/YY)',
                          validators=[DataRequired()])
    name = StringField('Cardholder Name',
                       validators=[DataRequired(), Length(max=40)])
    submit=SubmitField("Add Card")

    def validate_cardnum(self, field):

        if len(field.data) != 16:
            raise ValidationError("Card number should have exactly 16 digits")

    def validate_expiry(self, field):

        if len(field.data) != 4:
            raise ValidationError("Enter in format MMYY form")
        month = int(field.data[:2])
        if month<1 or month>12:
            raise ValidationError("Please enter a valid month")
        year = int(field.data[2:])
        curyear = int(datetime.datetime.now().strftime("%y"))
        if year < curyear or year > 30 or (year == curyear) and month < int(datetime.datetime.now().strftime("%m")):
            raise ValidationError("Please enter a valid year")


"""
This is a class for the Booking form which is used by user to book a new appointment for his/her pet
Implemented in /bookform route
"""
class BookingForm(FlaskForm):
    timeValues=[(1100,"11:00 AM"),(1130,"11:30 AM"),(1200,"12:00 PM"),(1230,"12:30 PM"),(1300,"1:00 PM"),
                (1330,"1:30 PM"),(1400,"2:00 PM"),(1430,"2:30 PM"),(1500,"3:00 PM"),(1530,"3:30 PM"),
                (1600,"4:00 PM"),(1630,"4:30 PM"),(1700,"5:00 PM"),(1730,"5:30 PM"),(1800,"6:00 PM")]
    name = StringField('Name',
                       validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])

    city=SelectField("Select City",validators=[DataRequired()])

    phone = StringField('Phone Number', validators=[DataRequired()])

    startTime = SelectField(u'From: ', choices=timeValues,validators=[DataRequired()])
    endtime = SelectField('Till: ', choices=timeValues[1:], validators=[DataRequired()])
    bookingDate = DateField('date', validators=[DataRequired()])
    pet = SelectField("Choose Pets", validators=[DataRequired()])

    instruction = TextAreaField('instruction',
                                validators=[DataRequired(), Length(min=2, max=200)])
    submit = SubmitField('Done, Book Now')

    # for validating endtime of the appoinment
    def validate_endtime(self,field):
        if int(field.data)<int(self.startTime.data):
                raise ValidationError("Please choose valid start time and end time.")

"""
This is a class for the Add Subscription form which is used to set a subscription for the user
Implemented in /profile/addsubscription route
"""
class AddSubForm(FlaskForm):
    creditcard = SelectField("Credit Card: ",  validators=[DataRequired()])
    sub_id=HiddenField("Sub",validators=[DataRequired()])
    submit = SubmitField('Add Subscription')





