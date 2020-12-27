# forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateTimeField, DateField, SelectField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, AnyOf, InputRequired, NumberRange
from app.models import CertificationClass
from wtforms.fields.html5 import DateField
from wtforms import Form

class LoginForm(FlaskForm):
    userID= StringField('Village ID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    
class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')


# <!-- <form method='POST' action="{{ url_for('saveAddress') }}">
#                 {{ form.csrf_token }}
#                 {{ form.street.label }}
#                 {{ form.street }}
#                 {{ form.city.label }}
#                 {{ form.city }}
#                 {{ form.state.label }}
#                 {{ form.state }}
#                 {{ form.zip.label }}
#                 {{ form.zip }}
#                 {{ form.village.label }}
#                 {{ form.village }}
#                 <input type="submit" value='SAVE'>
#             </form> -->
    
# class RegistrationForm(FlaskForm):
#     userID = StringField('userID')
#     userName = StringField('userName', validators=[DataRequired()])
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     password2 = PasswordField(
#         'Repeat Password', validators=[DataRequired(), EqualTo('password')])
#     submit = SubmitField('Register')

#     def validate_userName(self, userName):
#         user = User.query.filter_by(userName=userName.data).first()
#         if user is not None:
#             raise ValidationError('Please use a different userName.')

#     def validate_email(self, email):
#         user = User.query.filter_by(email=email.data).first()
#         if user is not None:
#             raise ValidationError('Please use a different email address.')

class ChangeClassLimitForm(FlaskForm):
    id = IntegerField('id')
    shopNumber = SelectField ('Shop',choices=[(0,'Select one -'),(1,'Rolling Acres'),(2,'Brownwood')],coerce=int)
    trainingDate = DateField('Date', format='%Y-%m-%d', validators=[InputRequired('Training date is required.')])
    classLimit = IntegerField ('Class Limit', validators=[NumberRange(min=1,max=30,message='Limit must be from 1-30')])    
    submit = SubmitField('Submit')

class ReportForm(FlaskForm):
    shopNumber = SelectField('Shop',choices=[(0,'Select one -'),(1,'Rolling Acres'),(2,'Brownwood')],coerce=int)
    trainingDate = DateField('Date', format='%Y-%m-%d', validators=[InputRequired('Training date is required.')])
    reportNumber = SelectField('Report',choices=[(0,'Select one -'),(1,'Sign-In Sheet'),(2,'Certification List'),(3,'Certify A Class'),(4,'Members Not Certified')],coerce=int)
    submit = SubmitField('PRINT')


class NewSessionForm(FlaskForm):
    shopNumber = SelectField ('Shop',choices=[(0,'Select one -'),(1,'Rolling Acres'),(2,'Brownwood')],coerce=int)
    trainingDate = DateField('Date', format='%Y-%m-%d', validators=[InputRequired('Training date is required.')])
    classLimit = IntegerField ('Class Limit', validators=[NumberRange(min=1,max=30,message='Limit must be from 1-30')])    
    submit = SubmitField('Add Class')


class NotCertifiedForm(FlaskForm):
    villageID = StringField('Village ID', validators=[DataRequired()])
    fullName = StringField('Name')
    firstName = StringField('First name', validators=[DataRequired()])
    lastName = StringField('Last name', validators=[DataRequired()])
    nickName = StringField('Nickname')
    dateJoined = DateTimeField('Date joined')
    certified = BooleanField('Certified')
    dateForCertificationTraining = DateField('Training date')
    homePhone = StringField('Home phone')
    mobilePhone = StringField('Mobile phone')
    certified = BooleanField('Certified')
    submit = SubmitField('Submit')

    def validate_villageID(self, villageID):
        member = Person.query.filter_by(villageID=villageID.data).first()
        if member is not None:
            raise ValidationError('Please use a different Village ID.')


class MemberLookupForm(Form):
    searchByID = StringField('Village ID')
    searchByName = StringField('or enter a name')

class DisplayMemberForm(Form):
    Member_ID = StringField('Village ID')
    fullName = StringField('Name')
    Date_Joined = DateTimeField('Date joined')
    Certification_Training_Date = DateField('Rolling Acres Training')
    Certified = BooleanField('Certified for RA')
    Certification_Training_Date_2 = DateField('Brownwood Training')
    Certified_2 = BooleanField('Certified for BW')
    Home_Phone = StringField('Home phone')
    Cell_Phone = StringField('Mobile phone')
    Email = StringField('Email')
    submit = SubmitField('Submit')