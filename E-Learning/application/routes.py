
from application import app,db

from flask import render_template,request,Response,flash,redirect,url_for,session
from application.models import User,Course,Enrollment
from application.forms import LoginForm,RegisterForm
import json
coursedata = [{"courseID": "1111", "title": "PHP 111", "description": "Introduction to Php", "credits": "4",
               "term": "Fall,Spring"},
              {"courseID": "1112", "title": "Java", "description": "Introduction to Java", "credits": "5",
               "term": "Fall"},
              {"courseID": "1113", "title": "Python", "description": "Introduction to Python", "credits": "3",
               "term": "Fall"},
              {"courseID": "1114", "title": "C++", "description": "Introduction to C++", "credits": "5",
               "term": "Fall,Spring"}]




#Create route for root directory
@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html",index=True)

@app.route("/login",methods = ["GET","POST"])
def login():

    #redirect to homepage if already loggedin
    if session.get("username"):
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.objects(email = email).first()
        #first element if not use first it will return
        #object as well as data

        if user and user.get_password(password):
            # One time if refresh data is lost just like alert
            flash("{},You are successfully Logged In".format(user.first_name),"success")
            session['user_id'] = user.user_id
            session["username"] = user.first_name
            return redirect(url_for("index"))
        else:
            flash("Sorry, Something went wrong","danger")
    return render_template("login.html",form = form,login = True)

@app.route("/logout")
def logout():
    session.pop("username",None)
    session["user_id"] = False
    return redirect(url_for("index"))


@app.route("/courses/")
@app.route("/courses/<term>")
def courses(term = None):
    if term is None:
        term = "Spring 2019"
    classes = Course.objects.order_by("courseID")
    #use all() for no order
    #use +courseID will ASEC
    #use -courseID will desc

    return render_template("courses.html",classes=classes,course=True,term = term)

@app.route("/register",methods = ["GET","POST"])
def register():
    if session.get("username"):
        return redirect(url_for("index"))
    form = RegisterForm()
    if form.validate_on_submit():
        user_id = User.objects.count()
        #Total num of data/rows
        user_id += 1
        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User(user_id = user_id,email = email,first_name=first_name,last_name=last_name)
        user.set_password(password)
        user.save()
        flash("Registration Successfull..","success")
        return redirect(url_for("index"))
    return render_template("register.html",register=True,form=form)

@app.route("/enrollment", methods=["GET","POST"])
def enrollment():
    if not session.get("username"):
        return redirect(url_for("login"))

    #many to many relationship b/w user and courses
    courseID = request.form.get("id")
    #courseTitle =request.form["title"]
    courseTitle = request.form.get("title")
    #Another method to fetch data
    #[]--> very strict return error
    #get() return None if empty
    user_id = session.get("user_id")
    if courseID:
        if Enrollment.objects(user_id = user_id,courseID=courseID):
            flash("You are already registered in {}".format(courseTitle))
            return redirect(url_for("courses"))
        else:
            Enrollment(user_id = user_id,courseID=courseID).save()
            flash("Successfully Enrolled in {} course".format(courseTitle))

    classes = list(User.objects.aggregate(*[
            {
                '$lookup': {
                    'from': 'enrollment',
                    'localField': 'user_id',
                    'foreignField': 'user_id',
                    'as': 'r1'
                }
            }, {
                '$unwind': {
                    'path': '$r1',
                    'includeArrayIndex': 'r1_id',
                    'preserveNullAndEmptyArrays': False
                }
            }, {
                '$lookup': {
                    'from': 'course',
                    'localField': 'r1.courseID',
                    'foreignField': 'courseID',
                    'as': 'r2'
                }
            }, {
                '$unwind': {
                    'path': '$r2',
                    'preserveNullAndEmptyArrays': False
                }
            }, {
                '$match': {
                    'user_id': user_id
                }
            }, {
                '$sort': {
                    'courseID': 1
                }
            }
        ]))

    return render_template("enrollment.html",enrollment=True,classes = classes)

#Retrun data to the user
@app.route("/api/")
@app.route("/api/<idx>")
def api(idx=None):
    if idx is None:
        jdata = coursedata
    else:
        jdata = coursedata[int(idx)]

    return Response(json.dumps(jdata),mimetype = "application/json")



@app.route("/user")
def user():
    #Creating entries on the table
    #User(user_id =1,first_name = "Jitendra",last_name = "Jeena", email ="jittu@gmail.com",password="Password123").save()
    #User(user_id=2, first_name="Kamlesh", last_name="Dasila", email="kammu@gmail.com", password="kamlesh123").save()
    #fetch data
    users = User.objects.all()
    return render_template("user.html",users=users)

#import json data to mongo
#set_path C:\Program Files\MongoDB\Server\4.2\bin
#mongoimport --DB UTA_Enrollment --collection user --file users.json
