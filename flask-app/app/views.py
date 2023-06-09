# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Flask modules
from flask   import render_template, request, redirect, url_for, flash
from jinja2  import TemplateNotFound

# App modules
from app import app, db
from app.models import Suppliers

# App main route + generic routing
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/suppliers')
def supplier():
    return render_template('suppliers.html')
