# forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateTimeField, DateField, SelectField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, AnyOf, InputRequired, NumberRange
from app.models import CertificationClass
from wtforms.fields.html5 import DateField
from wtforms import Form
    
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
