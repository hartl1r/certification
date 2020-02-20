# routes.py

from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from flask_bootstrap import Bootstrap

from werkzeug.urls import url_parse
from app.forms import MemberLookupForm, LoginForm, RegistrationForm, DisplayMemberForm  ,NewSessionForm,\
ChangeClassLimitForm, ReportForm
from app.models import User, Person, MonthList, AuthorizedUser, CertificationClass, ShopName, Member
from app import app
from app import db
from sqlalchemy import func, case, desc, extract, select, update
from app.forms import ResetPasswordRequestForm, ResetPasswordForm, NotCertifiedForm
from app.email import send_password_reset_email
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date

#from flask_redis import FlaskRedis
#r=FlaskRedis()
def get_count(q):
    count_q = q.statement.with_only_columns([func.count()]).order_by(None)
    count = q.session.execute(count_q).scalar()
    return count

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.datetime.utcnow()
        db.session.commit()

@app.route('/')
@app.route('/home')
@login_required
def home():
    # PREPARE trainingDatesShop1 USING RAW SQL
    #sql = """SELECT id, shopNumber, format(trainingDate,'M/d/yyyy') as trainingDate, classLimit, (select count(*) from person where certTrainingShop1= trainingDate) AS seatsTaken 
    #FROM certificationClass Where shopNumber = 1 and trainingDate >= CAST (GETDATE() AS DATE) ORDER BY format(trainingDate,'yyyyMMdd') """
    sql = """SELECT id, shopNumber, format(trainingDate,'M/d/yyyy') as trainingDate, classLimit, (select count(*) from tblMember_Data where Certification_Training_Date = trainingDate) AS seatsTaken 
    FROM tblTrainingDates Where shopNumber = 1 and trainingDate >= CAST (GETDATE() AS DATE) ORDER BY format(trainingDate,'yyyyMMdd') """
    #print (sql)
    trainingDatesShop1 = db.engine.execute(sql)
    #for t1 in trainingDatesShop1:
    #    print (t1.trainingDate)


    sql = """SELECT id, shopNumber, format(trainingDate,'M/d/yyyy') as trainingDate, classLimit, (select count(*) from tblMember_Data where Certification_Training_Date_2= trainingDate) AS seatsTaken 
    FROM tblTrainingDates WHERE shopNumber = 2 and trainingDate >= CAST (getdate() as Date) ORDER BY format(trainingDate,'yyyyMMdd')"""
    trainingDatesShop2 = db.engine.execute(sql)
    #for t2 in trainingDatesShop2:
    #    print (t2.trainingDate)

    form = NewSessionForm(request.form)

    # CALCULATE STATISTICS
    newThisYear = db.session.query(func.count(Member.Member_ID)).filter(extract('year',Member.Date_Joined) == datetime.date.today().year).scalar()
    #notCertifiedLastYear = db.session.query(func.count(Member.Member_ID)).filter(extract('year',Member.Date_Joined) == datetime.date.today().year -1 and Member.Certified != True).scalar()
    #notCertifiedThisYear = db.session.query(func.count(Member.Member_ID)).filter(extract('year',Member.Date_Joined) == datetime.date.today().year and Member.Certified != True).scalar()
    
    currentPaidMembers = db.session.query(func.count(Member.Member_ID)).filter(Member.Dues_Paid == True).scalar()
    print ("Current paid members -", currentPaidMembers)

    certifiedShop1=db.session.query(func.count(Member.Member_ID)).filter((Member.Certified == True and Member.Dues_Paid == True)).scalar()
    print ("Number certified in shop 1 -",certifiedShop1)

    certifiedShop2=db.session.query(func.count(Member.Member_ID)).filter((Member.Certified_2 == True and Member.Dues_Paid == True)).scalar()
    certifiedForBothShops=db.session.query(func.count(Member.Member_ID)).filter((Member.Certified == True and Member.Certified_2 == True and Member.Dues_Paid == True)).scalar()
    #print ("Number Certified In Both Shops -",certifiedForBothShops)

    notCertifiedShop1=db.session.query(func.count(Member.Member_ID))\
        .filter((Member.Certified == False) | (Member.Certified == None))\
        .filter((Member.Dues_Paid == True)).scalar()
    #print ("Not certified shop 1 -",notCertifiedShop1)

    notCertifiedShop2=db.session.query(func.count(Member.Member_ID))\
        .filter((Member.Certified_2 == False) | (Member.Certified_2 == None))\
        .filter((Member.Dues_Paid == True)).scalar()
    #print ("Not certified shop 2 -",notCertifiedShop2)

    noCertification=db.session.query\
        (func.count(Member.Member_ID))\
        .filter((Member.Certified == False) | (Member.Certified == None))\
        .filter((Member.Certified_2 == False) | (Member.Certified_2 == None))\
        .filter((Member.Dues_Paid == True)).scalar()
    #print ("Not certified either shop -",noCertification)

    return render_template("home.html",trainingDatesShop1=trainingDatesShop1,trainingDatesShop2=trainingDatesShop2,\
        form=form,newThisYear=newThisYear,currentPaidMembers=currentPaidMembers,certifiedShop1=certifiedShop1,\
        certifiedShop2=certifiedShop2,certifiedForBothShops=certifiedForBothShops,notCertifiedShop1=notCertifiedShop1,\
        notCertifiedShop2=notCertifiedShop2,noCertification=noCertification)


@app.route('/index')
def index():
    # Get next earliest training date for shop 1
    selectedDate1 = db.session.query(func.min(CertificationClass.trainingDate)).filter(CertificationClass.shopNumber==1 and CertificationClass.trainingDate >= todays_date).scalar()
    #print("Date selected -", selectedDate1)
     # PREPARE trainingDatesShop1 USING RAW SQL
    sql = """SELECT id, shopNumber, format(trainingDate,'M/d/yy') as trainingDate, classLimit, (select count(*) from person where certTrainingShop1= trainingDate) AS seatsTaken 
    FROM certificationClass Where shopNumber = 1 and trainingDate >= CAST (GETDATE() AS DATE) ORDER BY format(trainingDate,'yyyyMMdd') """
    trainingDatesShop1 = db.engine.execute(sql)
    
    sql = """SELECT id, shopNumber, format(trainingDate,'M/d/yy') as trainingDate, classLimit, (select count(*) from person where certTrainingShop2= trainingDate) AS seatsTaken 
    FROM certificationClass WHERE shopNumber = 2 and trainingDate >= CAST (getdate() as Date) ORDER BY format(trainingDate,'yyyyMMdd')"""
    trainingDatesShop2 = db.engine.execute(sql)

    newThisYear = db.session.query(func.count(Member.Member_ID)).filter(extract('year',Person.Date_Joined) == datetime.date.today().year).scalar()
    notCertifiedLastYear = db.session.query(func.count(Member.Member_ID)).filter(extract('year',Person.Date_Joined) == datetime.date.today().year -1 and Person.Certified != True).scalar()
    notCertifiedThisYear = db.session.query(func.count(Member.Member_ID)).filter(extract('year',Person.Date_Joined) == datetime.date.today().year and Person.Certified != True).scalar()
    
    currentMembers = db.session.query(func.count(Member.Member_ID)).filter(Person.Dues_Paid == True).scalar()
    NotCertified=db.session.query(func.count(Member.Member_ID)).filter((Person.Certified == False) | (Person.Certified == None)).scalar()
    NotCertified_2=db.session.query(func.count(Member.Member_ID)).filter((Person.Certified_2 == False) | (Person.Certified_2 == None)).scalar()
    NoCertification=db.session.query\
        (func.count(Member.Member_ID))\
        .filter((Person.Certified == False) | (Person.Certified == None))\
        .filter((Person.Certified_2 == False) | (Person.Certified_2 == None)).scalar()

    form = NewSessionForm(request.form)
    return render_template("stats.html", NotCertified=NotCertified,NotCertified_2=NotCertified_2,currentMembers=currentMembers,newThisYear=newThisYear,notCertifiedThisYear=notCertifiedThisYear,notCertifiedLastYear=notCertifiedLastYear,trainingDatesShop1=trainingDatesShop1,trainingDatesShop2=trainingDatesShop2,NoCertification=NoCertification,form=form ,selectedDate1=selectedDate1)

@app.route("/newSession", methods=["GET","POST"])
@login_required
def newSession():
    # ADD NEW TRAINING DATE
    shopNumber=None
    trainingDate=None
    classLimit=None

    form = NewSessionForm(request.form)
    if form.validate_on_submit():
        trainingDate = form.trainingDate.data 
        c = CertificationClass.query.filter(CertificationClass.shopNumber == form.shopNumber.data).filter(CertificationClass.trainingDate == form.trainingDate.data).first()
        if c != None:
          # print("Training date found - ",c.trainingDate)
            flash("This session is already on file.","warning")
            return redirect(url_for('home'))

        if trainingDate < datetime.date.today():
            flash ("The training date may not be a past date.","warning")
            return redirect(url_for('home'))

        try:
            cert = CertificationClass(shopNumber=form.shopNumber.data ,trainingDate=form.trainingDate.data, classLimit=form.classLimit.data)
            db.session.add(cert)
            db.session.commit()
            flash("Session added successfully.","success")
            return redirect(url_for('home'))
        except Exception as e:
            db.session.rollback()
            flash("Session could not be added.","danger")
            return redirect(url_for('home'))
    return  redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    #user = User.query.filter_by(userID="604875").first()
    #print("User-",user.userName)

    #member = Member.query.filter_by(Member_ID="604875").first()
    #print("Member-",member.Last_Name)

    #sql = """SELECT Member_ID, Last_Name FROM tblMember_Data Where Member_ID = """ + "'605875'" 
    #print (sql) 
    #member = db.engine.execute(sql)
    #for m in member:
    #    print (m.Member_ID, m.Last_Name)
    
    nameOfUser = 'Unknown'
   #print("Status-",current_user.is_authenticated)
    if current_user.is_authenticated:
        nameOfUser = db.session.query(Member.fullName).filter(Member.Member_ID==current_user.userID).first()
        return  redirect(url_for('home'))
       #print("authenicated -", nameOfUser)
        #return redirect(url_for('home'),nameOfUser=nameOfUser)
        
    form = LoginForm()
    #print("before validate_on_submit")
    if form.validate_on_submit():
       #print("validate_on_submit routine")
        user = User.query.filter_by(userID=form.userID.data).first()
               
        print("User-",user.userName)
        #print("PW-",form.password.data)
        #print("PW status-", user.check_password(form.password.data))
        pw1=user.set_password("infosys03")
        if user.check_password("infosys03"):
           print("infosys03 ok")

        if user is None:   
            flash('Invalid userID',"info")
            return redirect(url_for('login'))

       #print("PW: ", form.password.data)
       #print("Checking pw for ",user.userName)
       #print(user.password_hash)
       #print(generate_password_hash(form.password.data))
        if not user.check_password(form.password.data):
            flash(user.check_password(form.password.data),"info")
            flash('Invalid password',"warning")
            return redirect(url_for('login'))
            
        # check to see if person is authorized for this application
            # if not authorized display message
            # return ?
        # retrieve nickname or first name
        # nameOfUser = db.session.query(Person.firstName).filter(Member.Member_ID==form.userName.data).scalar()
        #member = Member.query.filter_by(Member_ID=form.userID.data).first()

        #records = Member.query.all()  'THIS WORKS!
        #records = db.session.query(Member).all()
        #for record in records:
        #    print(record)
        #sql = """SELECT Member_ID, Last_Name FROM tblMember_Data Where Member_ID = """ + "'605875'" 
        #print (sql) 
        #member = db.engine.execute(sql)
        #member = Member.query.filter_by(Member_ID=form.userID.data).first()
        #print (member.Last_Name)
        
        member = db.session.query(Member.fullName).filter(Member.Member_ID==form.userID.data).first()
        if member is None:
            flash("ID is in user table but not in member table.","warning")
            return redirect(url_for('login'))

        #if p.nickName:
        #    nameOfUser = p.nickName
        #else:
        #    nameOfUser = p.firstname
        nameOfUser=member.fullName 
        print ("Name of user - ", nameOfUser)

        login_user(user, remember=form.remember_me.data)
        # THE FOLLOWING IS NEEDED IF WE NEED TO RETURN TO THE PAGE THAT CAUSED THE USER TO GET TO THE LOGIN
        # WITHOUT THIS CODE THE USER WILL ALWAYS BE SENT TO THE index.html PAGE AFTER LOGIN
        # next_page = request.args.get('next')
        # if not next_page or url_parse(next_page).netloc != '':
        #     next_page = url_for('index')
        # return redirect(next_page,nameOfUser=nameOfUser)
       
        #return render_template('home.html',nameOfUser=nameOfUser)
        return  redirect(url_for('home'))

    return render_template('login.html', title='Sign In', form=form)   


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

        
#Either restrict this routine to the DBA or put it in the DBA app
#Should not register person unless they are in the Person table
#Should pull email address from Person table
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(userName=form.userName.data, email=form.email.data)
       #print( "Register pw:",form.password.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!','success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password','info')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.','success')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)     

@app.context_processor
def inject_last_year():
    return {'last_year': datetime.date.today().year-1}

@app.context_processor
def inject_this_year():
    return {'this_year': datetime.date.today().year}


@app.route("/showmonthlist", methods=["GET","POST"])
def showmonthlist():
   # monthlist = None
    monthlist = MonthList.query.all()
    return render_template("editmonthlist.html", monthlist=monthlist)


""" @app.route("/editmonthlist", methods=["GET","POST"])
def editmonthlist():
    try:
        monthnumber = request.form.get("monthnumber")
        newname = request.form.get("newname")
        #oldname = request.form.get("oldname")
        newabbr = request.form.get("newabbr")
       # oldabbr = request.form.get("oldabbr")

        monthlist = MonthList.query.filter_by(monthNumber=monthnumber).first()
        monthlist.monthname = newname
        monthlist.monthabbr = newabbr
        db.session.commit()
    except Exception as e:
           #print("Couldn't update month name")
           #print(e)
            db.session.rollback()
    return redirect("/showmonthlist")

 """
""" @app.route('/notcertified', methods=['GET', 'POST'])
def notcertified():
    form = NotCertifiedForm()
    if form.validate_on_submit():
        person = Person(villageID=form.villageID.data)
        db.session.add(person)
        db.session.commit()
        return redirect(url_for('notcertified'))
   # members = Person.query.all()
    people = db.session.query\
        (Member.Member_ID,Person.firstName,Person.lastName,Person.fullName,Person.certTrainingShop1,\
         Person.homePhone,Person.nickName,Person.Certified,Person.Date_Joined)\
        .filter(Person.Certified == False and Person.Date_Joined != None)

    #for p in people:
       #print(p.fullName, p.certTrainingShop1)
        

    return render_template('notcertified.html', title='Members Not Certified', people=people, form=form)
 """

""" @app.route('/editsessions', methods=['GET', 'POST'])
def editsessions():
    # ADD NEW TRAINING DATE
    #form = EditRowForm()
    if form.validate_on_submit():
        cert = CertificationClass(shopNumber=form.shopNumber ,trainingDate=form.trainingDate.data, classLimit=form.classLimit.data)
        db.session.add(cert)
        db.session.commit()
        return redirect(url_for('editsessions'))

    # DISPLAY CURRENT TRAINING DATES
    # PREPARE trainingDatesShop1 USING RAW SQL
    #sql = """#SELECT trainingDate, classLimit, (select count(*) from person where certTrainingShop1= trainingDate) AS seatsTaken 
    #FROM certificationClass Where shopNumber = 1 ORDER BY trainingDate"""
    #trainingDatesShop1 = db.engine.execute(sql)

    #sql = """SELECT trainingDate, classLimit, (select count(*) from person where certTrainingShop2= trainingDate) AS seatsTaken 
    #FROM certificationClass WHERE shopNumber = 2 ORDER BY trainingDate"""
    #trainingDatesShop2 = db.engine.execute(sql)
    #newThisYear = db.session.query(func.count(Member.Member_ID)).filter(extract('year',Person.Date_Joined) == datetime.date.today().year).scalar()
   #newThisYear = db.session.query(func.count(Member.Member_ID)).filter(Person.yearJoined == datetime.date.today().year).scalar()
   # return render_template('editsessions.html', title='Edit Training Dates', trainingDatesShop1=trainingDatesShop1, trainingDatesShop2=trainingDatesShop2,form=form)


""" @app.route("/updateSessions",methods=['POST'])
def updateSessions():
    shopNumber = request.form.get("shopNumber")
    certTrainingDate = request.form.get("trainingDate")
    oldClassLimit = request.form.get("oldClassLimit")
    newClassLimit = request.form.get("newClassLimit")
    
    # IS THERE A NEW CLASS LIMIT
    if newClassLimit == None:
        return redirect("/editsessions")

    # DETERMINE IF NEW CLASS LIMIT IS GREATER THAN NUMBER ALREADY ENROLLED'
    if shopNumber == 1:
        membersEnrolled=db.session.query\
        (func.count(Member.Member_ID))\
        .filter(Person.certTrainingShop1 == oldTrainingDate).scalar()

    if shopNumber == 2:
        membersEnrolled=db.session.query\
        (func.count(Member.Member_ID))\
        .filter(Person.certTrainingShop2 == oldTrainingDate).scalar()

    if membersEnrolled > newClassLimit: 
        msg = "Members enrolled exceeds new limit of " + membersEnrolled + "."
        flash (msg,'warning')
        return redirect("/editsessions")

    # RETRIEVE RECORD TO BE UPDATED
    if shopNumber == 1:
        c= CertificationClass.query.filter(trainingDateShop1 = certTrainingDate)\
            .filter(shopNumber = 1)

    if shopNumber == 2:
        c= CertificationClass.query.filter(trainingDateShop2 = certTrainingDate)\
            .filter(shopNumber = 2)  

    if c == None:
       #print ("No record found.")
        return redirect("/editsessions")    

    if oldClassLimit != newClassLimit:
        c.classLimit = newClassLimit

    try:
        db.session.commit()
    except Exception as e:
       #print("Couldn't update certification class limit")
       #print(e)
        db.session.rollback()

    return redirect("/editsessions")
 """
@app.route("/changeClassLimit/<string:id>/",methods=['GET','POST'])
def editTrainingSession(id):
    if request.method == 'GET':
        trainingClassID = id
        qry = db.session.query(CertificationClass).filter(CertificationClass.id == int(trainingClassID))
        cls = qry.first()
        if cls:
            form = ChangeClassLimitForm(obj=cls)
            return render_template ('changeClassLimit.html', form=form,id=id)
        else:
            return 'Record not found #{id}'.format(id=id)

    if request.method == 'POST': # and form.validate():
        #Get current Certification Class class limit using id
        qry = db.session.query(CertificationClass).filter(CertificationClass.id == int(id))
        cc = qry.first()
        if cc == None:
            flash("Record not found","danger")
            return redirect(url_for('/changeClassLimit'))

        # Is there a new class limit?
        currentClassLimit = cc.classLimit
        newClassLimit = request.form['classLimit']
        #newClassLimit = form.classLimit.data
        if newClassLimit == currentClassLimit:
            flash ("No change to class limit","success")
            return redirect(url_for("/home"))

        # DETERMINE IF NEW CLASS LIMIT IS GREATER THAN NUMBER ALREADY ENROLLED'
        membersEnrolled = 0
       #print("Members enrolled - ", str(membersEnrolled))
        if cc.shopNumber == 1:
            membersEnrolled = db.session.query\
            (func.count(Member.Member_ID))\
            .filter(Member.Certification_Training_Date == cc.trainingDate).scalar()

        if cc.shopNumber == 2:
            membersEnrolled = db.session.query\
            (func.count(Member.Member_ID))\
            .filter(Member.Certification_Training_Date_2 == cc.trainingDate).scalar()

        if membersEnrolled > int(newClassLimit):
            flash ("Members enrolled exceeds new limit; limit not changed.","info")
            return redirect(url_for("home"))

        # Change class limit in database
        try:
            cc.classLimit = newClassLimit
            db.session.commit()
            flash("Limit was changed.","success")
        except Exception as e:
            flash("Couldn't update Certification Class Limit","danger")
            db.session.rollback()
            return redirect(url_for('changeClassLimit'))

    return redirect(url_for('home'))

'''
@app.route("/deleteTrainingClass/<string:id>/",methods=['GET','POST'])
def deleteTrainingClass(id):
    # Get record to be deleted
    qry = db.session.query(CertificationClass).filter(CertificationClass.id == int(id))
    cc = qry.first()
    if cc == None:
        flash("Could not delete; record not found","warning")
        return redirect(url_for('/changeClassLimit'))

    shopNumber = cc.shopNumber
    trainingDate = cc.trainingDate

    # Are there any members enrolled?
    if shopNumber == 1:
        membersEnrolled = db.session.query\
        (func.count(Member.Member_ID))\
        .filter(Person.certTrainingShop1 == trainingDate).scalar()

    if shopNumber == 2:
        membersEnrolled = db.session.query\
        (func.count(Member.Member_ID))\
        .filter(Person.certTrainingShop2 == trainingDate).scalar()
    
    if membersEnrolled == 0:
        try:
            db.session.delete(cc)
            db.session.commit()
            deleteMsg = "Training class of " + str(trainingDate) + " removed."
            flash (deleteMsg,"warning")
        except:
            db.session.rollback()
            flash ("Delete was not successful","warning")
        finally:
            return redirect("/home")
    else:
        msg = "Cannot delete as there are still student(s) enrolled."
        flash (msg,"warning")
        return redirect("/home")
'''

@app.route("/rptNotCertified", methods=["GET","POST"])
def rpt():
    notCertified = None
    #notCertified = Person.query.filter(Certified == false).all()
    notCertified = db.session.query(Person.wholeName,Person.certTrainingShop1,Person.mobilePhone,\
        Person.homePhone,Person.emailAddress,Person.Date_Joined)\
        .order_by(Person.wholeName)\
        .filter(Person.Certified == False).all()
    
    todays_date = date.today().strftime('%m-%d-%Y')
   #print("Today is  ",todays_date)

    return render_template('rptNotCertified.html', notCertified=notCertified,todays_date=todays_date)

@app.route("/rptCertified", methods=["GET","POST"])
def rpt2():
    filterClause="Person.Certified == True"
    certified = None
    certified = db.session.query(Person.id,Person.wholeName,Person.certTrainingShop1,Person.mobilePhone,\
        Person.homePhone,Person.emailAddress,Person.Date_Joined)\
        .order_by(Person.wholeName)\
        .filter(Person.Certified == True).all()

    todays_date = date.today().strftime('%m-%d-%Y')
    recordCount = db.session.query(Person).filter(Person.Certified == True).count()
    return render_template('rptCertified.html', certified=certified,todays_date=todays_date,recordCount=recordCount)

@app.route("/rptSignIn/<string:id>/", methods=["GET","POST"])
def rptSignIn(id):
    # GET SHOPNUMBER, TRAINING DATE
    trainingDates = db.session.query(CertificationClass).filter(CertificationClass.id == id).all()
    for t in trainingDates:
        shopNumber = t.shopNumber
        trainingDate = t.trainingDate
    shopName = db.session.query(ShopName).filter(ShopName.Shop_Number == shopNumber).scalar()
    
    if shopNumber == 1:
        enrollees = db.session.query(Member).filter(Member.Certification_Training_Date == trainingDate).all()
        recordCount = db.session.query(Member).filter(Member.Certification_Training_Date == trainingDate).count()
    else:
        enrollees = db.session.query(Member).filter(Member.Certification_Training_Date_2 == trainingDate).all()
        recordCount = db.session.query(Member).filter(Member.Certification_Training_Date_2 == trainingDate).count()

    for e in enrollees:
        print (e.Last_Name)

    todays_date = date.today().strftime('%m-%d-%Y')
    
    
    return render_template('rptSignIn.html', enrollees=enrollees,todays_date=todays_date,recordCount=recordCount)


@app.route("/certify", methods=["GET", "POST"])
def certify():
    notcertified = None
    #notcertified = db.session.query(Person)
    #Person(Person.id, Person.fullName, Person.homePhone, Person.dateForCertificationTraining, \
    #    Person.certified).filter(Person.certified == False).all()
    notcertified = db.session.query\
        (Person.id, Person.fullName, Person.homePhone, Person.certTrainingShop1, \
        Person.Date_Joined,Person.Certified).all()
       #Person.Date_Joined,Person.certified).filter(Person.certified == False).all()
    return render_template("certify.html", notcertified=notcertified)

@app.route("/certifySelected", methods=["GET","POST"])
def certifySelected():
    selectedIDs = request.get_json()
    # GET SHOPNUMBER FROM FRONT OF ARRAY AND REMOVE FROM ARRAY
    shopNumber = selectedIDs.pop(0)
    # GET TRAINING CLASS ID FROM FRONT OF ARRAY AND REMOVE FROM ARRAY
    trainingClassID = selectedIDs.pop(0)
        
    # ROUTINE TO SET CERTIFIED TO TRUE FOR EACH MEMBER_ID IN THE ARRAY PASSED FROM JAVASCRIPT
    for id in selectedIDs:
        m = db.session.query(Member).filter(Member.Member_ID == id).first()
        if m != None:
            # UPDATE CERTIFIED FLAG
            try:
                if shopNumber == '1':
                    m.Certified = True
                else:
                    m.Certified_2 = True

                db.session.commit()
            except:
                db.session.rollback()
        else:
            print ("Nothing in m")

    ## THE FOLLOWING LINE IS NOT REFRESHING THE PAGE
    ## BUT A 'RELOAD' DOES 
    return redirect(url_for('trainingClass',id=trainingClassID))
    
@app.route("/trainingClass/<string:id>/", methods=["GET", "POST"])
def trainingClass(id):
    sql = """SELECT tblTrainingDates.id, tblTrainingDates.shopNumber, tblTrainingDates.trainingDate, tblShop_Names.Shop_Name
        FROM tblTrainingDates LEFT JOIN tblShop_Names ON tblTrainingDates.shopNumber = tblShop_Names.Shop_Number
        WHERE tblTrainingDates.id = """ + str(id)
    currentTrainingClass = db.engine.execute(sql)

    for c in currentTrainingClass:
        headingDate = c.trainingDate.strftime("%A, %B %e, %Y")
        shopNumber = c.shopNumber
        shopName = c.Shop_Name 
        trainingDate = c.trainingDate.strftime('%x')

    # IF SHOP 1 THEN COMPARE TRAINING DATE TO CERTIFICATION_TRAINING_DATE
    if shopNumber == 1: 
        sqlSelect = ""
        sqlSelect = '''SELECT Member_ID, (Last_Name + ', ' + First_Name) as fullName, Cell_Phone,
            Home_Phone, [E-mail] as Email,Certification_Training_Date,format(Date_Joined,'M/d/yy') as DateJoined,
            Certified,Certified_2,iif(Certified=1,'CERTIFIED','') as labelCertified,iif(Certified_2=1,'CERTIFIED','') as labelCertified_2
            from dbo.tblMember_Data WHERE Certification_Training_Date = ' ''' + str(trainingDate) + ''' ' ORDER BY Last_Name;'''
    else:
         # IF SHOP 2 THEN COMPARE TRAINING DATE TO CERTIFICATION_TRAINING_DATE_2
        sqlSelect = '''SELECT Member_ID, (Last_Name + ', ' + First_Name) as fullName, Cell_Phone,
            Home_Phone, [E-mail] as Email,Certification_Training_Date,format(Date_Joined,'M/d/yy') as DateJoined,
            Certified,Certified_2,iif(Certified=1,'CERTIFIED','') as labelCertified,iif(Certified_2=1,'CERTIFIED','') as labelCertified
            from dbo.tblMember_Data WHERE Certification_Training_Date_2 = ' ''' + str(trainingDate) + ''' ' ORDER BY Last_Name;'''
    trainingClass = db.engine.execute(sqlSelect)
    
    if trainingClass == None:
        flash("No members are enrolled.","info")
        return redirect(url_for('home'))
       
    return render_template("trainingClass.html",trainingClass=trainingClass,trainingClassID=id,headingDate=headingDate,shopName=shopName,shopNumber=shopNumber)



@app.route("/certifyupdate", methods=["POST"])
def certifyupdate():
   
    oldPersonID = request.form.get("oldpersonID")
    oldHomePhone = request.form.get("oldHomePhone")
    newHomePhone = request.form.get("newHomePhone")
    oldTraining = request.form.get("oldTraining")
    newTraining = request.form.get("newTraining")
    oldCertified = request.form.get("oldCertified")
    newCertified = request.form.get("newCertified")
    newBooleanCertified = request.form.get("newBooleanCertified")
    c = Person.query.filter_by(id=oldPersonID).first()
   #print ("STOP HERE",c)

        #c = db.session.query(Person).filter(id==oldPersonID)
        #c = db.session.query(Person).filter(id==oldPersonID).first()
   

    if c == None:
       #print ("No record found.")
        return redirect("/certify")    

   #print ("Boolean - ", newBooleanCertified)

    if newHomePhone != oldHomePhone:
        c.homePhone = newHomePhone

    if newTraining != oldTraining:
        c.dateForCertificationTraining = newTraining

    if newCertified != oldCertified: #and newCertified != None:
        c.certified = newCertified

    #if newBooleanCertified != oldCertified:
    #    c.certified = newBooleanCertified 
        
    try:
        db.session.commit()
    except Exception as e:
       #print("Couldn't update certification data")
        print(e)
        db.session.rollback()

    return redirect("/certify")

@app.route("/reportPrint")
def reportPrint():
    form = ReportForm()
    return render_template('reportPrint.html',form=form)

@app.route("/printReport", methods=['GET','POST'])
def printReport():
    #if request.method != 'POST':
    #    return 'GET request'

    #if request.method == 'POST':
    shopNumber = request.form.get("shopNumber")
    trainingDate = request.form.get("trainingDate")
    reportNumber = request.form.get("reportNumber")

    if reportNumber == '1':
        if shopNumber == '1':
            try:
                enrollees = None
                enrollees = db.session.query(Person.id,Person.wholeName,Person.certTrainingShop1.label("trainingDt"),Person.mobilePhone,\
                Person.homePhone,Person.emailAddress,Person.Date_Joined) \
                .order_by(Person.wholeName) \
                .filter(Person.certTrainingShop1 == trainingDate).all()
            except:
               #print ("No records.")
                flash("No records available for sign in report.","info")
                return redirect(url_for('/reportPrint'))
        if shopNumber == '2':
            try:
                enrollees = None
                enrollees = db.session.query(Person.id,Person.wholeName,Person.certTrainingShop2.label("trainingDt"),Person.mobilePhone,\
                Person.homePhone,Person.emailAddress,Person.Date_Joined) \
                .order_by(Person.wholeName) \
                .filter(Person.certTrainingShop2 == trainingDate).all()
            except:
                print ("No records.")
                flash("No records available for sign in report.","info")
                return redirect(url_for('/reportPrint'))
       
        recordCount = 0
        shopName = db.session.query(ShopName.shopName).filter(ShopName.shopNumber == shopNumber).scalar()
        todays_date = date.today().strftime('%m-%d-%Y')
        if shopNumber == '1':
            recordCount = db.session.query(Person).filter(Person.certTrainingShop1 == trainingDate).count()
        if shopNumber == '2':
            recordCount = db.session.query(Person).filter(Person.certTrainingShop2 == trainingDate).count()
            
        return render_template('rptSignIn.html', enrollees=enrollees, todays_date=todays_date,recordCount=recordCount,shopName=shopName)  
    return redirect(url_for('reportPrint')) 
 

@app.route("/memberlookup", methods=['GET','POST'])  # menu item link
def memberlookup():
    form=DisplayMemberForm()
    #print ("Name:", form.fullName.data)
    if request.method != 'POST':
        return render_template('memberLookup.html',form=form)

    return render_template('memberLookup.html',form=form)
#        members = db.session.query(Person.fullName,Person.id)
#        return render_template('/results.html', members=members)


@app.route("/memberLookupRoutine", methods=['GET', 'POST'])
def memberLookupRoutine():
    searchByID = request.form.get("searchByID")
    searchByName = request.form.get("searchByName")
    form=DisplayMemberForm()

    if request.method != 'POST':
        return render_template('memberLookup.html',form=form)

    if searchByID != '':
        #lookup member by ID
        qry = db.session.query(Member).filter(Member.Member_ID == searchByID)
        member = qry.first()
        if member:
            print(member.Member_ID,member.Home_Phone,member.Cell_Phone)
            form = DisplayMemberForm(obj=member)
            #form.populate_obj(member)
            return render_template ('memberLookup.html', form=form)
        else:
            flash ("Member ID " + searchByID + " not found.","warning")
            return render_template('memberlookup.html', form=form)

    if searchByName != '':
        #name was entered
        search_string = searchByName + '%'
        #people = db.session.query(Person.fullName,Member.Member_ID).filter(Person.lastName.like('H*'))
        members = db.session.query(Member.Member_ID, Member.fullName).filter(Member.Last_Name.like(search_string)).order_by(Member.fullName)
        #people = db.session.query(Person.fullName,Member.Member_ID).filter(Member.Member_ID == search_string)
        for m in members:
            print(m.fullName, m.Member_ID)

        return render_template('memberLookup.html',members=members,form=form)  

    flash("Please enter a Village ID or a name.","warning")
    return render_template('memberLookup.html',form=form)

# --------------------------------------------------------------------------
# TEST OF PASSING PARAMETERS IN URL
@app.route('/memberByID', defaults={'id' : '604875'})
@app.route('/memberByID/<id>')  
def memberByID(id):
    searchID = id
    qry = db.session.query(Person).filter(Member.Member_ID == searchID)
    member = qry.first()
    if member:
        form = DisplayMemberForm(obj=member)
        return render_template ('memberLookup.html', form=form)
    else:
        flash("ID was not found.","warning")
        form = DisplayMemberForm()
        return render_template('memberLookup.html',form=form)
        #return 'Error loading #{id}'.format(id=id)
 
# --------------------------------------------------------------------------

@app.route("/displayMember",methods = ['POST'])   
def displayMember():
    id = request.form.get("memberID")
    qry = db.session.query(Member).filter(Member.Member_ID == id)
    member = qry.first()
    if member:
        #print ("Name - ", member.fullName)
        form = DisplayMemberForm(obj=member)
        return render_template ('memberLookup.html', form=form)
    else:
        return 'Error loading #{id}'.format(id=id)
        
@app.route('/reportMenu/<id>/')
def reportMenu(id):
    #print (type(id))
    #print (id)
    #trainingDates = db.session.query(CertificationClass).join(ShopName,Shop_Number==shopNumber).filter(CertificationClass.id == {id}).all()
    trainingDates = db.session.query(CertificationClass).filter(CertificationClass.id == id).all()
    for t in trainingDates:
        #print (t.trainingDate,t.shopNumber)
        headingDate = t.trainingDate.strftime("%A, %B %e, %Y")
        shopNumber = t.shopNumber
        shopName='Unknown'
        shopName= db.session.query(ShopName.Shop_Name).filter(ShopName.Shop_Number == shopNumber).scalar()
    return render_template('reportMenu.html',shopName=shopName,headingDate=headingDate,trainingDate=t.trainingDate,trainingDateID=id,shopNumber=shopNumber)

@app.route('/reports/<id>/')
def reports(id):
    trainingDatesShop1 = db.session.query(CertificationClass).filter(CertificationClass.id == {id}).all()
    trainingDatesShop1 = db.session.query(CertificationClass).filter(CertificationClass.shopNumber == 1).order_by(CertificationClass.trainingDate).all()
    return render_template('reports.html',  trainingDatesShop1=trainingDatesShop1)

#@app.route('/selectDate1', methods = ['POST'])
#def selectDate1():
#    id = request.form.get("id1")
   #print("ID - ",id)
#    return redirect('/reports')

@app.route('/results')
def search_results(search):
    #results = []
    search_string = search.data['searchByID']
   #print(todays_date)

    if search.data['searchByID'] != '':
        flash("place lookup by ID here ...")
        redirect('/memberLookup')
        #qry = db_session.query(Album)
        #results = qry.all()

    if search.data['searchByName'] != '':
        search_string = search.data['searchByName'] & '*'
        people = db.session.query(Person.fullName,Member.Member_ID).filter(Member.Member_ID == search_string)
        return redirect('/memberLookup',people=people)  

    if search.data['searchByName'] == 'b':
        members = db.session.query(Person.fullName,Member.Member_ID).filter(Member.Member_ID == search_string)
        return render_template('/results.html', members=members)

@app.route('/printSignIn')
def printSignIn():
   #print ("Test printSignIn")
    #return "print Sign In"
    return redirect(url_for('index'))


@app.route("/removeTrainingClass/<string:id>/",methods=['GET','POST'])
def removeTrainingClass(id):
    # Get record to be deleted
    qry = db.session.query(CertificationClass).filter(CertificationClass.id == int(id))
    cc = qry.first()
    if cc == None:
        flash("Could not delete; record not found","warning")
        return redirect(url_for('/trainingClass'))

    shopNumber = cc.shopNumber
    trainingDate = cc.trainingDate

    # Are there any members enrolled?
    if shopNumber == 1:
        membersEnrolled = db.session.query\
        (func.count(Member.Member_ID))\
        .filter(Member.Certification_Training_Date == trainingDate).scalar()

    if shopNumber == 2:
        membersEnrolled = db.session.query\
        (func.count(Member.Member_ID))\
        .filter(Member.Certification_Training_Date_2 == trainingDate).scalar()
    
    if membersEnrolled == 0:
        try:
            db.session.delete(cc)
            db.session.commit()
            deleteMsg = "Training class of " + str(trainingDate) + " removed."
            flash (deleteMsg,"success")
        except:
            db.session.rollback()
            flash ("Delete was not successful","danger")
        finally:
            return redirect("/")
    else:
        msg = "Cannot delete as there are still student(s) enrolled."
        flash (msg,"warning")
        return redirect("/")


@app.route("/editClassLimit/<string:id>/",methods=['GET','POST'])
def editClassLimit(id):
    if request.method == 'GET':
        trainingClassID = id
        qry = db.session.query(CertificationClass).filter(CertificationClass.id == int(trainingClassID))
        cls = qry.first()
        if cls:
            editForm = ChangeClassLimitForm(obj=cls)
            return render_template ('editClassLimit.html', editForm=editForm,id=id)
        else:
            return 'Record not found #{id}'.format(id=id)

    if request.method == 'POST': # and form.validate():
        #Get current Certification Class class limit using id
        qry = db.session.query(CertificationClass).filter(CertificationClass.id == int(id))
        cc = qry.first()
        if cc == None:
            flash("Record not found","danger")
            return redirect(url_for('/editClassLimit'))

        # Is there a new class limit?
        currentClassLimit = cc.classLimit
        newClassLimit = request.editForm['classLimit']
       
        if newClassLimit == currentClassLimit:
            flash ("No change to class limit","info")
            return redirect(url_for("/editClassLimit"))

        # DETERMINE IF NEW CLASS LIMIT IS GREATER THAN NUMBER ALREADY ENROLLED'
        membersEnrolled = 0
       #print("Members enrolled - ", str(membersEnrolled))
        if cc.shopNumber == 1:
            membersEnrolled = db.session.query\
            (func.count(Member.Member_ID))\
            .filter(Person.certTrainingShop1 == cc.trainingDate).scalar()

        if cc.shopNumber == 2:
            membersEnrolled = db.session.query\
            (func.count(Member.Member_ID))\
            .filter(Person.certTrainingShop2 == cc.trainingDate).scalar()

        if membersEnrolled > int(newClassLimit):
            flash ("Members enrolled exceeds new limit; limit not changed.","warning")
            return redirect(url_for("/editClassLimit"))

        # Change class limit in database
        try:
            cc.classLimit = newClassLimit
            db.session.commit()
            flash("Limit was changed.","success")
        except Exception as e:
            flash("Couldn't update Certification Class Limit","danger")
            db.session.rollback()
            return redirect(url_for('/editClassLimit'))

    return redirect(url_for('/editClassLimit'))

@app.route('/queryExample')
def queryExample():
    selectedIDs=[];
    #idArray = request.args.get(id) #if key doesn't exist, returns None
    selectedIDs = request.form.getlist('idString')
    #framework = request.args['framework'] #if key doesn't exist, returns a 400, bad request error
    #website = request.args.get('website')

    return '''<h1>The language value is: {}</h1>'''.format(language)
             #<h1>The framework value is: {}</h1>
             # <h1>The website value is: {}'''.format(language, framework, website)

@app.route('/form-example',methods=["GET","POST"])
def formexample():
    if request.method == 'POST': #this block is only entered when the form is submitted
        language = request.form.get('language')
        framework = request.form['framework']

        return '''<h1>The language value is: {}</h1>
                  <h1>The framework value is: {}</h1>'''.format(language, framework)

    return '''<form method="POST">
                  Language: <input type="text" name="language"><br>
                  Framework: <input type="text" name="framework"><br>
                  <input type="submit" value="Submit"><br>
              </form>'''

@app.route('/jsonExample',methods=["POST"])
def jsonexample():
    req_data = request.get_json()

    language = None
    if 'language' in req_data:
        language = req_data['language']
    
    framework = None
    if 'framework' in req_data:
        framework = req_data['framework']

    python_version = req_data['version_info']['python'] #two keys are needed because of the nested object

    example = None
    if 'example' in req_data:
        example = req_data['examples'][0] #an index is needed because of the array

    boolean_test = False
    if 'boolean_test' in req_data:    
        boolean_test = req_data['boolean_test']

    return '''
           The language value is: {}
           The framework value is: {}
           The Python version is: {}
           The item at index 0 in the example list is: {}
           The boolean value is: {}'''.format(language, framework, python_version, example, boolean_test)

@app.route('/processjson', methods=['POST'])
def processjson():
    data = request.get_json()
    name = data['name']
    location = data['location']
    randomlist = data['randomlist']

    return jsonify({'result' : 'Success!', 'name' : name, 'location' : location, 'randomkeyinlist' : randomlist[1]});   


@app.route('/getmethod/<jsdata>')
def getmethod(jsdata):
    print("/getmethod routine")
    print(jsdata)
    return json.loads(jsdata)[0]

@app.route('/postmethod', methods = ['GET','POST'])
def postmethod():
    if request.method == "POST":
        jsdata = request.get_json()
        print (jsdata)
        msg = "postmethod data - '" + str(jsdata) + "'"
        print (msg)
        # add code to update certified fields in person table
        # need member ID to get the right training class
    #return redirect(url_for('/trainingClass?id=3'))
    id=2
   #return redirect('/trainingClass',id=id)
    return ('/trainingClass?id=2')
