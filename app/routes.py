# routes.py

from flask import render_template, flash, redirect, url_for, request, jsonify
#from flask_login import current_user, login_user, logout_user #, login_required
from flask_bootstrap import Bootstrap
from werkzeug.utils import cached_property
from werkzeug.urls import url_parse

from app.forms import MemberLookupForm, LoginForm, RegistrationForm, DisplayMemberForm  ,NewSessionForm,\
ChangeClassLimitForm, ReportForm
from app.models import User, Person, MonthList, AuthorizedUser, CertificationClass, ShopName, Member
from app import app
from app import db
from sqlalchemy import func, case, desc, extract, select, update
from app.forms import ResetPasswordRequestForm, ResetPasswordForm, NotCertifiedForm
# from app.email import send_password_reset_email
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date

app.secret_key = 'My secret key'

@app.route('/')
@app.route('/index/')
@app.route('/home')
def index():
    # PREPARE trainingDatesShop1 USING RAW SQL
    sql = """SELECT id, shopNumber, format(trainingDate,'M/d/yyyy') as trainingDate, classLimit, (select count(*) from tblMember_Data where Certification_Training_Date = trainingDate) AS seatsTaken 
    FROM tblTrainingDates Where shopNumber = 1 and trainingDate >= CAST (GETDATE() AS DATE) ORDER BY format(trainingDate,'yyyyMMdd') """
    trainingDatesShop1 = db.engine.execute(sql)

    sql = """SELECT id, shopNumber, format(trainingDate,'M/d/yyyy') as trainingDate, classLimit, (select count(*) from tblMember_Data where Certification_Training_Date_2= trainingDate) AS seatsTaken 
    FROM tblTrainingDates WHERE shopNumber = 2 and trainingDate >= CAST (getdate() as Date) ORDER BY format(trainingDate,'yyyyMMdd')"""
    trainingDatesShop2 = db.engine.execute(sql)
    
    form = NewSessionForm(request.form)

    # CALCULATE STATISTICS
    newThisYear = db.session.query(func.count(Member.Member_ID)).filter(extract('year',Member.Date_Joined) == datetime.date.today().year).scalar() 
    currentPaidMembers = db.session.query(func.count(Member.Member_ID)).filter(Member.Dues_Paid == True).scalar()
    certifiedShop1=db.session.query(func.count(Member.Member_ID)).filter((Member.Certified == True and Member.Dues_Paid == True)).scalar()
    certifiedShop2=db.session.query(func.count(Member.Member_ID)).filter((Member.Certified_2 == True and Member.Dues_Paid == True)).scalar()
    certifiedForBothShops=db.session.query(func.count(Member.Member_ID)).filter((Member.Certified == True and Member.Certified_2 == True and Member.Dues_Paid == True)).scalar() 
    notCertifiedShop1=db.session.query(func.count(Member.Member_ID))\
        .filter((Member.Certified == False) | (Member.Certified == None))\
        .filter((Member.Dues_Paid == True)).scalar()

    notCertifiedShop2=db.session.query(func.count(Member.Member_ID))\
        .filter((Member.Certified_2 == False) | (Member.Certified_2 == None))\
        .filter((Member.Dues_Paid == True)).scalar()

    noCertification=db.session.query\
        (func.count(Member.Member_ID))\
        .filter((Member.Certified == False) | (Member.Certified == None))\
        .filter((Member.Certified_2 == False) | (Member.Certified_2 == None))\
        .filter((Member.Dues_Paid == True)).scalar()
    
    return render_template("home.html",trainingDatesShop1=trainingDatesShop1,trainingDatesShop2=trainingDatesShop2,\
        form=form,newThisYear=newThisYear,currentPaidMembers=currentPaidMembers,certifiedShop1=certifiedShop1,\
        certifiedShop2=certifiedShop2,certifiedForBothShops=certifiedForBothShops,notCertifiedShop1=notCertifiedShop1,\
        notCertifiedShop2=notCertifiedShop2,noCertification=noCertification)

@app.route("/newSession", methods=["GET","POST"])
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
            flash("This session is already on file.","warning")
            return redirect(url_for('index'))

        if trainingDate < datetime.date.today():
            flash ("The training date may not be a past date.","warning")
            return redirect(url_for('index'))

        try:
            cert = CertificationClass(shopNumber=form.shopNumber.data ,trainingDate=form.trainingDate.data, classLimit=form.classLimit.data)
            db.session.add(cert)
            db.session.commit()
            flash("Session added successfully.","success")
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash("Session could not be added.","danger")
            return redirect(url_for('index'))
    return  redirect(url_for('index'))

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
        if newClassLimit == currentClassLimit:
            flash ("No change to class limit","success")
            return redirect(url_for("/index"))

        # DETERMINE IF NEW CLASS LIMIT IS GREATER THAN NUMBER ALREADY ENROLLED'
        membersEnrolled = 0
       
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
            return redirect(url_for("index"))

        # Change class limit in database
        try:
            cc.classLimit = newClassLimit
            db.session.commit()
            flash("Limit was changed.","success")
        except Exception as e:
            flash("Couldn't update Certification Class Limit","danger")
            db.session.rollback()
            return redirect(url_for('changeClassLimit'))

    return redirect(url_for('index'))

@app.route("/rptNotCertified", methods=["GET","POST"])
def rpt():
    notCertified = None
    #notCertified = Person.query.filter(Certified == false).all()
    notCertified = db.session.query(Person.wholeName,Person.certTrainingShop1,Person.mobilePhone,\
        Person.homePhone,Person.emailAddress,Person.Date_Joined)\
        .order_by(Person.wholeName)\
        .filter(Person.Certified == False).all()
    
    todays_date = date.today().strftime('%m-%d-%Y')
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
    trainingDates = db.session.query(CertificationClass)\
        .filter(CertificationClass.id == id).all()
    for t in trainingDates:
        shopNumber = t.shopNumber
        trainingDate = t.trainingDate 
        trainingDisplayDate = trainingDate.strftime("%A, %B %e, %Y")
    shopName = db.session.query(ShopName).filter(ShopName.Shop_Number == shopNumber).scalar()
    
    if shopNumber == 1:
        enrollees = db.session.query(Member)\
            .filter(Member.Certification_Training_Date == trainingDate)\
            .order_by(Member.Last_Name,Member.First_Name).all()
        recordCount = db.session.query(Member).filter(Member.Certification_Training_Date == trainingDate).count()
    else:
        enrollees = db.session.query(Member)\
            .filter(Member.Certification_Training_Date_2 == trainingDate)\
            .order_by(Member.Last_Name,Member.First_Name).all()
        recordCount = db.session.query(Member).filter(Member.Certification_Training_Date_2 == trainingDate).count()

    todays_date = date.today().strftime("%A, %B %e, %Y")
    
    return render_template('rptSignIn.html', enrollees=enrollees,todays_date=todays_date,recordCount=recordCount,trainingDisplayDate=trainingDisplayDate)


@app.route("/certify", methods=["GET", "POST"])
def certify():
    notcertified = None
    notcertified = db.session.query\
        (Person.id, Person.fullName, Person.homePhone, Person.certTrainingShop1, \
        Person.Date_Joined,Person.Certified).all()
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
        return redirect(url_for('index'))
       
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
   
    if c == None:
       #print ("No record found.")
        return redirect("/certify")    


    if newHomePhone != oldHomePhone:
        c.homePhone = newHomePhone

    if newTraining != oldTraining:
        c.dateForCertificationTraining = newTraining

    if newCertified != oldCertified: #and newCertified != None:
        c.certified = newCertified
    
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
            return render_template ('memberLookup.html', form=form)
        else:
            flash ("Member ID " + searchByID + " not found.","warning")
            return render_template('memberlookup.html', form=form)

    if searchByName != '':
        #name was entered
        search_string = searchByName + '%'
        members = db.session.query(Member.Member_ID, Member.fullName).filter(Member.Last_Name.like(search_string)).order_by(Member.fullName)
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
    trainingDates = db.session.query(CertificationClass).filter(CertificationClass.id == id).all()
    for t in trainingDates:
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

@app.route('/results')
def search_results(search):
    search_string = search.data['searchByID']

    if search.data['searchByID'] != '':
        flash("place lookup by ID here ...")
        redirect('/memberLookup')

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
