# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Flask modules
from flask   import render_template, request, redirect, url_for, flash, session
from jinja2  import TemplateNotFound

# App modules
from app import app, db
from app.models import Member, Membership
import datetime

# App main route + generic routing
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/challenges_init')
def challenges_init():
    members = Member.query.all()
    return render_template('challenges_init.html', members=members)

@app.route('/challenges_sent')
def challenges_sent():
    return render_template('challenges_sent.html')

@app.route('/challenges_inbox')
def challenges_inbox():
    return render_template('challenges_inbox.html')

@app.route('/challenges_form')
def challenges_form():
    return render_template('challenges_form.html')

@app.route('/membership_registration')
def membership_registration():
    return render_template('membership_registration.html')

@app.route('/registration_success')
def registration_success():
    return render_template('reg_success')

@app.route('/submit_membership_registration', methods=["GET", "POST"])
def submit_membership_registration():
    # Get the variable and form validation
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    meid = request.form.get('meid')
    msid = request.form.get('msid')
    plan = request.form.get('plan')

    # Form validation
    error = False
    
    if not meid :
        flash('Please enter your memberid')
        error = True
        
    if not fname:
        flash('Please enter your FirstName')
        error = True
        
    if not plan:
        flash('Please select your Membership Plans')
        error = True
        
    if not error:
        if not msid:
            meid = int(meid)
            plan = int(plan)
            year = datetime.datetime.now().year
            month = datetime.datetime.now().month
            day = datetime.datetime.now().day
            dueday = day + 7
            endyear = year + plan
            startdate = f"{year}-{month}-{day}"
            enddate = f"{endyear}-{month}-{day}"
            duedate = f"{year}-{month}-{dueday}"
            amount = float(plan * 100)
            membership = Membership(
                MEID = meid,
                StartDate = startdate,
                EndDate = enddate,
                InvoiceDate = startdate,
                DueDate = duedate,
                Amount = amount         
            )
            payamount = 100 * plan
            tax = payamount * 0.1
            totalpay = payamount + tax
            db.session.add(membership)
            db.session.commit()
            db.session.refresh(membership)
            session['msid'] = msid
            flash(f'Your membership ID #{membership.MSID} is added')
            return render_template('reg_success.html', membership = membership, tax = tax, totalpay = totalpay, plan = plan)
        else:
            plan = int(plan)
            enddate = db.session.query(Membership.EndDate).filter(Membership.MSID == msid).scalar()
            endyear = enddate.year + plan
            month = enddate.month
            day = enddate.day
            enddate = f"{endyear}-{month}-{day}"
            membership = Membership.query.get(msid)
            membership.EndDate = enddate
            db.session.commit()
            payamount = 100 * plan
            tax = payamount * 0.1
            totalpay = payamount + tax
            session['msid'] = msid
            flash(f"Your Membership ID #{msid}'s EndDate has been extended to {enddate}")
            return render_template('reg_success.html', membership = membership, tax = tax, totalpay = totalpay, plan = plan)
            
    return render_template('membership_registration.html', fname=fname, lname=lname, meid=meid, msid=msid, plan=plan)

@app.route('/payment_success', methods=['GET','POST'])
def payment_success():
    msid = request.form.get('msid')
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    startdate = f"{year}-{month}-{day}"
    membership = Membership.query.get(msid)
    membership.PaidDate = startdate
    db.session.commit()
    return render_template('payment_success.html')