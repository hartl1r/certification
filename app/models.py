# models.py 

from datetime import datetime 
from time import time
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import select, func, Column, extract 
from sqlalchemy.orm import column_property
from sqlalchemy.ext.hybrid import hybrid_property
from app import app

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
    Inactive = db.Column(db.Boolean)
    NonMember_Volunteer=db.Column(db.Boolean)
    Emerg_Name = db.Column(db.String(30))
    Emerg_Phone = db.Column(db.String(14))
    fullName = column_property(First_Name + " " + Last_Name)
  
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
