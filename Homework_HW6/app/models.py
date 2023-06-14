# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from app import db

class Suppliers(db.Model):
    SupplierID = db.Column(db.Integer, primary_key=True)
    CompanyName = db.Column(db.String(40), nullable=False)
    City = db.Column(db.String(15), nullable=True)

class Products(db.Model):
    ProductID = db.Column(db.Integer, primary_key=True)
    SupplierID = db.Column(db.Integer, foreign_key='Suppliers.SupplierID')
    ProductName = db.Column(db.String(40), nullable=False)
    UnitPrice = db.Column(db.Float(19, 4), nullable=True)
    CategoryID = db.Column(db.Integer, nullable=True)

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
