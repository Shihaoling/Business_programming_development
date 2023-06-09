# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from app import db

class member(db.Model):
    MEID = db.Column(db.Integer, primary_key=True)
    Age = db.Column(db.Integer, nullable=False)
    FirstName = db.Column(db.String(50), nullable=False)
    LastName = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(50), nullable=False)
    MPassword = db.Column(db.String(30), nullable=False)
    Phone = db.Column(db.String(20), nullable=False)
    Gender = db.Column(db.String(10), nullable=False)
    UTR = db.Column(db.Numeric, nullable=False)
    DateOfCreation = db.Column(db.DateTime, nullable=False)

class Match(db.Model):
    MAID = db.Column(db.Integer, primary_key=True)

class Challenge(db.Model):
    CID = db.Column(db.Integer, primary_key=True)
    ChallengerMEID = db.Column(db.Integer, nullable=False)
    ChallengedMEID = db.Column(db.Integer, nullable=False)
    DateOfChallenge = db.Column(db.Date, nullable=False)
    Status = db.Column(db.Integer, nullable=False)
    Notes = db.Column(db.String(100))

class Membership(db.Model):
    MSID = db.Column(db.Integer, primary_key=True)
    MEID = db.Column(db.Integer, nullable=False)
    StartDate = db.Column(db.Date, nullable=False)
    EndDate = db.Column(db.Date, nullable=False)
    InvoiceDate = db.Column(db.Date, nullable=False)
    DueDate = db.Column(db.Date, nullable=False)
    Amount = db.Column(db.Float, nullable=False)
    PaidDate = db.Column(db.Date, nullable=False)

# class Stats(db.Model):

#     id          = db.Column(db.Integer,   primary_key=True )
#     month       = db.Column(db.String(64),    unique=True  )
#     sold_units  = db.Column(db.Integer                     )
#     total_sales = db.Column(db.Integer                     )

#     def __init__(self, id, month, sold_units, total_sales):
#         self.id          = id
#         self.month       = month
#         self.sold_units  = sold_units
#         self.total_sales = total_sales

#     def __repr__(self):
#         return self.month + ' = ' + str(self.sold_units) + '/ ' + str(self.total_sales)

#     # Optional helper
#     def save(self):

#         # inject self into db session    
#         db.session.add ( self )

#         # commit change and save the object
#         db.session.commit( )

#         return self 
