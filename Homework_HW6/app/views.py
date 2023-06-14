# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Flask modules
from flask   import render_template, request, redirect, url_for, flash
from jinja2  import TemplateNotFound
from sqlalchemy import func

# App modules
from app import app, db
from app.models import Suppliers, Products

# App main route + generic routing
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/supplier')
def supplier():
    return render_template('supplier.html')

@app.route('/form')
def form():
    suppliers = Suppliers.query.all()
    products = Products.query.all()

    suppliersids = sorted(set([supplier.SupplierID for supplier in suppliers]))
    productcategories = sorted(set([product.CategoryID for product in products]))
    return render_template('HW6Q1.html',suppliersid = suppliersids, productcategories = productcategories)


@app.route('/ProductFormSubmmit', methods=['GET', 'POST'])
def ProductFormSubmit():
    pid = request.form.get('ProductID')
    pname = request.form.get('ProductName')
    pprice = request.form.get('ProductPrice')
    sid = request.form.get('SupplierID')
    cid = request.form.get('CategoryID')

@app.route('/SupplierFormSubmmit',methods=['GET','POST'])
def SupplierFormSubmit():
    error = False

    # get user input values from the form data
    sid = request.form.get('SupplierID')
    cname = request.form.get('CompanyName')

    # error checking
    if not cname:
        flash('The company name is required')
        error = True

    # if sid:
    #     sid = float(sid) # the float function converts a string value to a numeric value
    #     if sid>0:

    # update the database

    if not error:
        if not sid:
            new_supplier = Suppliers(CompanyName=cname)
            db.session.add(new_supplier)
            db.session.commit()
            db.session.refresh(new_supplier)
            flash("A new supplier with supplierID=" + str(new_supplier.SupplierID) + ' has been added.')
        else: # modify a supplier's record with the matching supplier id
            sid = int(sid)
            existing_supplier = Suppliers.query.get(sid)
            existing_supplier.CompanyName = cname
            existing_supplier.verified = True
            db.session.commit()
            flash("The supplier's with supplierid=" + str(sid) +" has been updated")

    return render_template('supplier.html')