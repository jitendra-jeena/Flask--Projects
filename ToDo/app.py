#importing necessary modules
from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)   #Creating Instance of Flask
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///data.db?check_same_thread=False'

#Creating Instance of the Database
db = SQLAlchemy(app)

#Creating table
class Task(db.Model):
    """
    Table for storing various tasks with their time of creation and ID
    """
    __tablename__ = "Task"
    id = db.Column(db.Integer,primary_key = True)
    task = db.Column(db.String(30),nullable = False)
    time = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Boolean,default = False)
#Initialise the process of DB Creation
db.init_app(app)

#Creating the database
with app.app_context():
    db.create_all()
    """
    #Adding a column in table
    task1 = Task(task = "Learn Python")

    #Adding data to the table
    try:
        db.session.add(task1)
        db.session.commit()
    except:
        db.session.rollback()
    """

@app.route("/",methods = ["GET","POST"])
def home():
    """
    Function to add the task and update the homepage
    :return: render index.html page
            :error- if any error occured during the addition of task
            : Added task information if method = "POST"
    """

    error = None
    if request.method == "POST":

        new_task = request.form["new_task"]
        task = Task(task=new_task)
        try:
            db.session.add(task)
            db.session.commit()
            error = "Task Successfully Added"
            return redirect("/")
        except:
            error = "Unable To Add Task"
            db.session.rollback()
    task_info = Task.query.order_by(Task.time).all()
    return render_template("index.html",task_info = task_info,error = error)



@app.route("/complete/<int:id>")
def completed(id):
    """
    Function to remove task from the database and
    Give 5 points to user for successfully completing tasks
    :return:  render index page with updated tasks
    """
    task_id = Task.query.get_or_404(id)
    #Update Points
    task_id.status = True
    try:
        db.session.commit()
        return redirect("/")
    except:
        return "Unable to delete"


#Route for updating the task
@app.route("/update/<int:id>",methods = ["POST","GET"])
def update(id):
    """
    Function for updating task
    :return: renders index page with updated data
    """
    tasks = Task.query.get_or_404(id)
    # Delete task from the database
    if request.method == "POST":
        #Fetching updated task
        tasks.task = request.form["updated_task"]
        tasks.status = False
        #Updating task on Database
        try:
            db.session.commit()
            return redirect("/")
        except:
            return "Unable to Update Task"
    else:
        return render_template("update.html",tasks = tasks)

@app.route("/delete/<int:id>")
def delete(id):
    """
    Function to remove task form database
    And deduct 3 points for not completing the task
    :return:  render index page with updated tasks
    """
    #Getting the id of the task to be deleted
    task_id  = Task.query.get_or_404(id)
    print("something")
    #Delete task from the database
    try:
        db.session.delete(task_id)
        db.session.commit()
        return redirect("/")
    except:
        return "Unable to delete"
if __name__ == "__main__":
    app.run()