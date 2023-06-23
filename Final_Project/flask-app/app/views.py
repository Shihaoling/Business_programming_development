# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Flask modules
from flask import render_template, request, redirect, url_for, flash, session, json
from jinja2 import TemplateNotFound

# App modules
from app import app, db
from app.models import member, Membership
import datetime

# App main route + generic routing


@app.route('/', methods=['POST', 'GET'])
def indexhome():
    # gender ratio
    members_num = member.query.count()
    member_f = member.query.filter(member.Gender == 'F').count()
    member_m = member.query.filter(member.Gender == 'M').count()
    f_ratio = (member_f/members_num)*100
    m_ratio = (member_m/members_num)*100
    gender_lay = [{'label': 'Female',
                   'value': f_ratio},
                  {'label': 'Male',
                   'value': m_ratio
                   }]
    gender_lay = json.dumps(gender_lay)
    # (member.query.group_by(member.Gender).count())/(member.query.all().count())

    # gender_layout = db.session.query(member.Gender.label('label'),
    #                                  (((func.count(member.MEID)).group_by(member.Gender))/((member.MEID).all().count())).label('value'))
    # gender_lay = [row._asdict() for row in gender_layout]

    # top utr members
    order_member = member.query.order_by((member.UTR).desc()).all()
    l = []
    for i in range(10):
        # for i in order_member:
        utr = order_member[i].UTR
        mid = order_member[i].MEID
        utr_rank = {'label': str(mid), 'value': utr}
        l.append(utr_rank)
    l = json.dumps(l)
    # age group
    all_age = db.session.query(member.Age).all()
    age10 = []
    age20 = []
    age30 = []
    age40 = []
    age50 = []
    age60 = []
    age_group = []
    for i in all_age:
        if (i[0] > 10) & (i[0] < 20):
            age10.append(i)
            lb = '10+'
            age_group1 = {'label': lb, 'value': len(age10)}
        elif (i[0] >= 20) & (i[0] < 30):
            age20.append(i)
            lb = '20+'
            age_group2 = {'label': lb, 'value': len(age20)}
        elif (i[0] >= 30) & (i[0] < 40):
            age30.append(i)
            lb = '30+'
            age_group3 = {'label': lb, 'value': len(age30)}
        elif (i[0] >= 40) & (i[0] < 50):
            age40.append(i)
            lb = '40+'
            age_group4 = {'label': lb, 'value': len(age40)}
        elif (i[0] >= 50) & (i[0] < 60):
            age50.append(i)
            lb = '50+'
            age_group5 = {'label': lb, 'value': len(age50)}
        else:
            age60.append(i)
            lb = '60+'
            age_group6 = {'label': lb, 'value': len(age60)}
    age_group.append(age_group1)
    age_group.append(age_group2)
    age_group.append(age_group3)
    age_group.append(age_group4)
    age_group.append(age_group5)
    age_group.append(age_group6)
    age_group = json.dumps(age_group)
    # age_group = {'label':}
    if request.method == 'POST':
        d_user = member.query.get(int(session.get('mid')))
        db.session.delete(d_user)
        db.session.commit()
    return render_template('index.html', chartdata1=gender_lay, data2=l, data3=age_group)


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
    return render_template('membership_reg_success')


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

    if not meid:
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
                MEID=meid,
                StartDate=startdate,
                EndDate=enddate,
                InvoiceDate=startdate,
                DueDate=duedate,
                Amount=amount
            )
            payamount = 100 * plan
            tax = payamount * 0.1
            totalpay = payamount + tax
            db.session.add(membership)
            db.session.commit()
            db.session.refresh(membership)
            session['msid'] = msid
            flash(f'Your membership ID #{membership.MSID} is added')
            return render_template('membership_reg_success.html', membership=membership, tax=tax, totalpay=totalpay, plan=plan)
        else:
            plan = int(plan)
            enddate = db.session.query(Membership.EndDate).filter(
                Membership.MSID == msid).scalar()
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
            flash(
                f"Your Membership ID #{msid}'s EndDate has been extended to {enddate}")
            return render_template('membership_reg_success.html', membership=membership, tax=tax, totalpay=totalpay, plan=plan)

    return render_template('membership_registration.html', fname=fname, lname=lname, meid=meid, msid=msid, plan=plan)


@app.route('/payment_success', methods=['GET', 'POST'])
def payment_success():
    msid = request.form.get('msid')
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    startdate = f"{year}-{month}-{day}"
    membership = Membership.query.get(msid)
    membership.PaidDate = startdate
    db.session.commit()
    return render_template('membership_payment_success.html')


@app.route('/ask_for_chart')
def chartform():
    membership = Membership.query.all()
    year = sorted(set([m.EndDate.year for m in membership]))
    return render_template('membership_ask_for_chart.html', year=year)


@app.route('/chart', methods=["GET", "POST"])
def chart():
    membership = Membership.query.all()
    year = int(request.form.get('year'))
    paynum = 0
    unpaynum = 0
    # today = datetime.datetime.now().date()
    for m in membership:
        amount = int(m.Amount)
        plan = amount / 100
        EndDate = m.EndDate
        PaidDate = m.PaidDate
        PaidJudgeDate = EndDate - datetime.timedelta(days=plan*366)
        allyear = sorted(set([m.EndDate.year for m in membership]))

        if (m.PaidDate is None or PaidDate < PaidJudgeDate) and (m.EndDate.year == year):
            unpaynum += 1
        elif m.EndDate.year == year:
            paynum += 1
    structure1 = {
        "label": "not pay",
        "value": str(unpaynum)}
    structure2 = {
        "label": "paid",
        "value": str(paynum)
    }
    structure = [structure1, structure2]
    chartData = json.dumps(structure)
    return render_template('membership_chart.html', chartData=chartData, year=year, allyear=allyear)


@app.route('/extention', methods = ['GET', 'POST'])
def extend():
    meid = session.get('mid')
    plan = request.form.get('plan')
    plan = int(plan)
    meid = int(meid)
    memberships = db.session.query(Membership).filter(Membership.MEID == meid).all()
    for m in memberships:
        year = int(m.EndDate.year)
        month = int(m.EndDate.month)
        day = int(m.EndDate.day)
        membership = m
    extended_EndDate = f'{year+plan}-{month}-{day}'
    amount = plan * 100
    paidyear = datetime.datetime.now().year
    paidmonth = datetime.datetime.now().month
    paidday = datetime.datetime.now().day
    paidDate = f'{paidyear}-{paidmonth}-{paidday}'
    membership.EndDate = extended_EndDate
    membership.PaidDate = paidDate
    membership.InvoiceDate = paidDate
    membership.Amount = amount
    db.session.commit()
    payamount = 100 * plan
    tax = payamount * 0.1
    totalpay = payamount + tax
    return render_template('membership_reg_success.html', membership=membership, tax=tax, totalpay=totalpay, plan=plan)


@app.route('/delete_ms/<int:ms_id>', methods=['POST', 'GET'])
def delete_ms(ms_id):
    membership = Membership.query.get(ms_id)
    if membership is not None:
        db.session.delete(membership)
        db.session.commit()
        flash(f"Membership ID #{ms_id} has been deleted successfully.")
    memberships = Membership.query.all()
    now = datetime.datetime.now()
    return render_template('membership_admin_view.html', memberships=memberships, now=now)


@app.route('/judge')
def judge_ms():
    meid = session.get('mid')
    membership = db.session.query(Membership).filter(
        Membership.MEID == meid).all()
    if not membership:
        members = member.query.get(meid)
        return render_template('membership_registration.html', fname=members.FirstName, lname=members.LastName, meid=meid)
    return render_template('membership_extend.html')


@app.route('/membership_list')
def membership_list():
    memberships = Membership.query.all()
    now = datetime.datetime.now()
    return render_template('membership_admin_view.html', memberships=memberships, now=now)

# Lv Lv Lv Lv Lv Lv


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register')
def register():
    return render_template('new_register.html')


@app.route('/signup', methods=['GET', 'POST'])
def successfullsignup():
    # get input value
    fname = request.form.get('firstname')
    lname = request.form.get('lastname')
    email = request.form.get('email')
    pword = request.form.get('password')
    phone = request.form.get('phone')
    gender = request.form.get('gender')
    age = request.form.get('age')
    utr = request.form.get('utr')
    # error checking
    error = False
    if len(pword) <= 8:
        flash('Please enter a password more than 8 words.')
        error = True
    # if phone.isdigit() == False:
    #     flash('Please enter the phone number with a correct format.')
    #     error = True
    if int(age) < 0:
        flash('Age must be greater than 0.')
        error = True
    if float(utr) > 16.5 or float(utr) < 1:
        flash('The UTR is between 1 and 16.5.')
        error = True
    if not error:
        user = ''
        user = member(FirstName=fname, LastName=lname, Email=email, MPassword=pword, Gender=gender,
                      Phone=phone, Age=age, UTR=utr, DateOfCreation=datetime.datetime.now())
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)

        return render_template('aftersignup.html', newuser=user)

    return render_template('new_register.html', password=pword, phone=phone, age=age, utr=utr, gender=gender,
                           firstname=fname, lastname=lname, email=email)


@app.route('/login')
def login():
    return render_template('new_login.html')


@app.route('/userhome')
def userhome():
    currentHour = datetime.datetime.now().hour
    greeting = ''
    if currentHour < 12:
        greeting = 'Good morning!'
    else:
        greeting = 'Good afternoon!'
    session['now'] = datetime.date.today()
    # top utr members
    order_member = member.query.order_by((member.UTR).desc()).all()
    l = []
    for i in range(10):
        # for i in order_member:
        utr = order_member[i].UTR
        mid = order_member[i].MEID
        utr_rank = {'label': str(mid), 'value': utr}
        l.append(utr_rank)
    l = json.dumps(l)

    return render_template('userhome.html', message=greeting, data2=l)


@app.route('/userhomepage', methods=['GET', 'POST'])
def informationSubmit():
    # get input
    username = request.form.get('mid')
    pword = request.form.get('password')
    # valid check
    userinfo = member.query.get(username)  # this users whole info
    existing_mid = db.session.query(member.MEID).all()
    existing_mid = [x[0] for x in existing_mid]
    if int(username) in existing_mid:
        if pword == userinfo.MPassword:
            session['mid'] = username  # MEID
            session['name'] = member.query.get(session['mid']).FirstName
            session['lname'] = member.query.get(session['mid']).LastName
            session['email'] = member.query.get(session['mid']).Email
            session['phone'] = member.query.get(session['mid']).Phone
            session['age'] = member.query.get(session['mid']).Age
            session['pword'] = member.query.get(session['mid']).MPassword
            session['gender'] = member.query.get(session['mid']).Gender
            session['utr'] = member.query.get(session['mid']).UTR
            currentHour = datetime.datetime.now().hour
            greeting = ''
            if currentHour < 12:
                greeting = 'Good morning!'
            else:
                greeting = 'Good afternoon!'
            # top utr members
            order_member = member.query.order_by((member.UTR).desc()).all()
            l = []
            for i in range(10):
                # for i in order_member:
                utr = order_member[i].UTR
                mid = order_member[i].MEID
                utr_rank = {'label': str(mid), 'value': utr}
                l.append(utr_rank)
            l = json.dumps(l)
            return render_template('userhome.html', message=greeting, data2=l)
        else:
            flash("Error! The password and user does not match! Please try again.")
    else:
        flash('This member dose not exist, please try again!')
    # error checking
    return render_template('new_login.html')


@app.route('/accountsetting')
def account():
    return render_template('account.html')


@app.route('/accountmodify', methods=['GET', 'POST'])
def accountchange():
    # get input
    fname = request.form.get('firstName')
    lname = request.form.get('lastName')
    email = request.form.get('email')
    phone = request.form.get('phoneNumber')
    gender = request.form.get('gender')
    age = request.form.get('age')
    pword = request.form.get('password')
    # error checking
    error = False
    if len(pword) <= 8:
        flash('Please enter a password more than 8 words.')
        error = True
    if phone.isdigit() == False:
        flash('Please enter the phone number with a correct format.')
        error = True
    if int(age) < 0:
        flash('Age must be greater than 0.')
        error = True
    if not error:
        existing_user = member.query.get(session['mid'])
        existing_user.FirstName = fname
        existing_user.LastName = lname
        existing_user.Email = email
        existing_user.Phone = phone
        existing_user.Gender = gender
        existing_user.Age = age
        existing_user.MPassword = pword
        existing_user.verified = True
        db.session.commit()
        session['name'] = fname
        session['lname'] = lname
        session['email'] = email
        session['phone'] = phone
        session['age'] = age
        session['pword'] = pword
        session['gender'] = gender
        flash('Your information has been updated successfully!')
    return render_template('account.html')


@app.route('/accountdelete')
def aboutdelete():
    return render_template('accountdelete.html')

