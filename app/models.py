# models.py 

from datetime import datetime 
from time import time
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import select, func, Column, extract 
from sqlalchemy.orm import column_property
from sqlalchemy.ext.hybrid import hybrid_property
from app import login
from flask_login import UserMixin
#import jwt
from app import app

# @login.user_loader
# def load_user(id):
#     return User.query.get(int(id))

    
# class User(UserMixin, db.Model):
#     __tablename__ = 'user'
#     __table_args__ = {"schema": "dbo"}
#     id = db.Column(db.Integer, primary_key=True)
#     userID = db.Column(db.String(6),index=True, unique=True)
#     userName = db.Column(db.String(30), index=True, unique=True)
#     passwordHash = db.Column(db.String(255))
#     email = db.Column(db.String(128))
#     applications = db.Column(db.String(128))
#     lastSeen = db.Column(db.DateTime, default=datetime.utcnow)

#     def __repr__(self):
#         return '<User {}>'.format(self.username)

    # def set_password(self, password):
    #     self.password_hash = generate_password_hash(password)

    # def check_password(self, password):
    #     return check_password_hash(self.password_hash, password)


    # def get_reset_password_token(self, expires_in=600):
    #     return jwt.encode(
    #         {'reset_password': self.id, 'exp': time() + expires_in},
    #         app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

# @staticmethod
# def verify_reset_password_token(token):
#     try:
#         id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
#     except:
#         return
#     return User.query.get(id)

        
# class Person(db.Model):
#     __tablename__ = 'person'
#     id = db.Column(db.Integer, primary_key=True)
#     villageID = db.Column(db.String(6), index=True, unique=True)
#     lastName = db.Column(db.String(30))
#     firstName = db.Column(db.String(30))
#     nickName = db.Column(db.String(30))
#     dateJoined = db.Column(db.DateTime)
#     #monthJoined = db.Column(db.Integer)
#     #yearJoined=db.Column(db.String(4))
#     certifiedShop1 = db.Column(db.Boolean)
#     certTrainingShop1 = db.Column(db.DateTime)
#     certifiedShop2 = db.Column(db.Boolean)
#     certTrainingShop2 = db.Column(db.DateTime)
#     homePhone = db.Column(db.String(14))
#     mobilePhone = db.Column(db.String(14))
#     emailAddress = db.Column(db.String(255))
#     duesPaid=db.Column(db.Boolean)
#     fullName = column_property(firstName + " " + lastName)
    
#     @hybrid_property
#     def wholeName(self):
#         return self.lastName + ", " + self.firstName 
#     def __repr__(self):
#         return '<Person {}>'.format(self.villageID)

class Member(db.Model):
    __tablename__ = 'tblMember_Data'
    __table_args__ = {"schema": "dbo"}
    id = db.Column(db.Integer, primary_key=True)
    Member_ID = db.Column(db.String(6), index=True, unique=True)
    Last_Name = db.Column(db.String(30))
    First_Name = db.Column(db.String(30))
    NickName = db.Column(db.String(30))
    Date_Joined = db.Column(db.DateTime)
    Certified = db.Column(db.Boolean)
    Certification_Training_Date = db.Column(db.DateTime)
    Certified_2 = db.Column(db.Boolean)
    Certification_Training_Date_2 = db.Column(db.DateTime)
    Home_Phone = db.Column(db.String(14))
    Cell_Phone = db.Column(db.String(14))
    eMail = db.Column('E-Mail',db.String(255))
    Dues_Paid=db.Column(db.Boolean)
    NonMember_Volunteer=db.Column(db.Boolean)
    Emerg_Name = db.Column(db.String(30))
    Emerg_Phone = db.Column(db.String(14))
    fullName = column_property(First_Name + " " + Last_Name)
  
# class AuthorizedUser(db.Model):
#     __tablename__ = 'authorizedUser'
#     villageID = db.Column(db.String(6), primary_key=True)
#     application = db.Column(db.String(30), primary_key=True)

class MonthList(db.Model):
    __tablename__ = 'monthList'
    id = db.Column(db.Integer,primary_key=True)
    monthNumber = db.Column(db.Integer)
    monthName = db.Column(db.String(12))
    monthAbbr = db.Column(db.String(3))

class CertificationClass(db.Model):
    __tablename__ = 'tblTrainingDates'
    __table_args__ = {"schema": "dbo"}
    id = db.Column(db.Integer, primary_key=True)
    trainingDate = db.Column(db.DateTime)
    classLimit = db.Column(db.String(30))
    shopNumber = db.Column(db.Integer)
    #purpose = db.column(db.String(30))

    def __repr__(self):
        return '<CertificationClass {}>'.format(self.trainingDate)

class ShopName(db.Model):
    __tablename__ = 'tblShop_Names'
    __table_args__ = {"schema": "dbo"}
    Shop_Number = db.Column(db.Integer, primary_key=True)
    Shop_Name = db.Column(db.String(30))

class MemberTransactions(db.Model):
    __tablename__="tblMember_Data_Transactions"
    __table_args__={"schema":"dbo"}
    ID = db.Column(db.Integer, primary_key=True)
    Transaction_Date = db.Column(db.DateTime)
    Member_ID = db.Column(db.String(6))
    Staff_ID = db.Column(db.String(6))
    Original_Data = db.Column(db.String(50))
    Current_Data = db.Column(db.String(50))
    Data_Item = db.Column(db.String(30))
    Action = db.Column(db.String(6))
