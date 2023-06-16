# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Flask modules
from flask import render_template, request, redirect, url_for, flash, session, json
from jinja2 import TemplateNotFound
from sqlalchemy import func

# App modules
from app import app, db
from app.models import Suppliers, Products
import datetime


# App main route + generic routing
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/supplier")
def supplier():
    return render_template("supplier.html")


@app.route("/form")
def form():
    suppliers = Suppliers.query.all()
    products = Products.query.all()

    suppliersids = sorted(set([supplier.SupplierID for supplier in suppliers]))
    productcategories = sorted(set([product.CategoryID for product in products]))
    return render_template(
        "HW6Q1.html", suppliersid=suppliersids, productcategories=productcategories
    )


@app.route("/login")
def login():
    return render_template("HW6Q2.html")


@app.route("/ProductFormSubmmit", methods=["GET", "POST"])
def ProductFormSubmit():
    # get user input values
    pid = request.form.get("ProductID")
    pname = request.form.get("ProductName")
    pprice = request.form.get("ProductPrice")
    sid = request.form.get("SupplierID")
    cid = request.form.get("CategoryID")
    stock = request.form.get("stock")

    # get sid and cid from data base
    suppliers = Suppliers.query.all()
    products = Products.query.all()

    suppliersids = sorted(set([supplier.SupplierID for supplier in suppliers]))
    productcategories = sorted(set([product.CategoryID for product in products]))

    # error checking
    error = False
    if not sid:
        flash("Supplier ID is required")
        error = True
    else:
        sid = int(float(sid))
        if sid < 0:
            flash("Supplier ID must be greater than 0")
            error = True

    if not pname:
        flash("Product name is required")
        error = True

    if not pprice:
        flash("Product price is required")
        error = True
    else:
        pprice = float(pprice)
        if pprice < 0:
            flash("Product price must be greater than 0")
            error = True

    if not cid:
        flash("Category ID is required")
        error = True
    else:
        cid = int(cid)
        
    if pid:
        pid = int(float(pid))
        if pid < 0 or pid not in db.session.query(Products.ProductID).all():
            flash("Pleash enter a valid product ID")
            error = True

    if not stock:
        flash("Units in Stock is required")
        error = True
    else:
        stock = int(float(stock))
        if stock < 0:
            flash("Units in product must be greater than 0")
            error = True

    # database operation
    if not error:
        product = ""
        if not pid:
            # add a new product record
            product = Products(
                ProductName=pname,
                SupplierID=sid,
                UnitPrice=pprice,
                CategoryID=cid,
                UnitsInStock=stock,
            )
            db.session.add(product)
            db.session.commit()
            db.session.refresh(product)
            flash("A new product with ID= " + str(product.ProductID) + " is added")
        else:
            session["pid"] = pid
            product = Products.query.get(pid)
            product.ProductName = pname
            product.SupplierID = sid
            product.UnitPrice = pprice
            product.CategoryID = cid
            product.UnitStock = stock
            db.session.commit()
            flash("The product's with productid=" + str(pid) + " has been updated")
        return render_template("HW6Q1.2.html", updatedProducts=product)
    return render_template(
        "HW6Q1.html",
        sid=sid,
        cid=cid,
        pprice=pprice,
        stock=stock,
        pname=pname,
        pid=pid,
        suppliersid=suppliersids,
        productcategories=productcategories,
    )


@app.route("/q2submit", methods=['GET', 'POST'])
def q2submit():
    # get the user input values
    sid = request.form.get('sid')
    cname = request.form.get('cname')
    # error checking
    error = False
    if not sid:
        flash('SupplierID required')
        error = True
    if not cname:
        flash('Company Name required')
        error = True
    # if no error, compare
    if not error:
        supplier = Suppliers.query.get(sid)
        if supplier is not None and cname == supplier.CompanyName:
            currentHour = datetime.datetime.now().hour
            greeting = ""
            if currentHour < 12:
                greeting = "morning"
            else:
                greeting = "afternoon"
            session['sid'] = sid
            session['cname'] = cname
            return render_template("HW6Q2_greeting.html", greeting=greeting)
        else:
            flash('Supplierid or Company Name is wrong, please try again')
    return render_template("HW6Q2.html")


@app.route("/HW7Q1")
def HW7Q1():
    suppliers = Suppliers.query.all()
    suppliersids = sorted(set([supplier.SupplierID for supplier in suppliers]))
    return render_template("HW7Q1.html", suppliersid=suppliersids)


@app.route('/chart', methods=['GET', 'POST'])
def productChart():
    result = db.session.query(Products.ProductName.label('label'), Products.UnitsInStock.label('value')).filter(Products.SupplierID==2)
    chartData = [row._asdict() for row in result]
    chartData = json.dumps(chartData)
    return render_template('graph.html', chartData=chartData)
    

@app.route("/SupplierFormSubmmit", methods=["GET", "POST"])
def SupplierFormSubmit():
    error = False

    # get user input values from the form data
    sid = request.form.get("SupplierID")
    cname = request.form.get("CompanyName")

    # error checking
    if not cname:
        flash("The company name is required")
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
            flash(
                "A new supplier with supplierID="
                + str(new_supplier.SupplierID)
                + " has been added."
            )
        else:  # modify a supplier's record with the matching supplier id
            sid = int(sid)
            existing_supplier = Suppliers.query.get(sid)
            existing_supplier.CompanyName = cname
            existing_supplier.verified = True
            db.session.commit()
            flash("The supplier's with supplierid=" + str(sid) + " has been updated")

    return render_template("supplier.html")
