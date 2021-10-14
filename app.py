from flask import Flask,render_template,redirect,request
from flask.helpers import url_for
from datetime import *
from flask_sqlalchemy import SQLAlchemy
from pytz import timezone 
from sqlalchemy.orm import defaultload
import psycopg2

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://qfehkayaqurkii:4ca8a1d0027ca4b9112a2224e5d5ffec1649a499569082c12c68b66f90798a09@ec2-18-207-72-235.compute-1.amazonaws.com:5432/d4m3fuumk8tmu2"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'thisismykey'
db = SQLAlchemy(app)


#-------------------------------DATABASE CREATION------------------------------------------------
#-------------------------------TABLE CREATION---------------------------------------------------
class Customer(db.Model):
    __tablename__='customer_details'
    customer_id = db.Column(db.Integer,primary_key = True)
    date = db.Column(db.Date,default = date.today(),nullable=False)
    time = db.Column(db.String(10),default = datetime.now(timezone("Asia/Kolkata")).strftime('%H:%M'),nullable=False)
    customer_name = db.Column(db.String(40))
    customer_vehicle_type = db.Column(db.String(30))
    customer_vehicle_problem = db.Column(db.String(45))
    problem_status = db.Column(db.String(20),default='pending',nullable=False)
    customer_number = db.Column(db.String(20))
    vehicle_near_area = db.Column(db.String(40))
    pass

class Workers(db.Model):
    __tablename__='workers_details'
    worker_id = db.Column(db.Integer,primary_key = True)
    date = db.Column(db.Date,default = date.today(),nullable=False)
    time = db.Column(db.String(10),default = datetime.now(timezone("Asia/Kolkata")).strftime('%H:%M'),nullable=False)
    worker_name = db.Column(db.String(40))
    worker_area = db.Column(db.String(40))
    worker_number = db.Column(db.String(20))

    
#------------------------------Rountes----------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------

@app.route("/")
@app.route("/home")
def main():
    return render_template("index.html")

@app.route("/twowheeler")
def twowheeler():
    return render_template("two.html")

@app.route("/fuel")
def threewheeler():
    return render_template("three.html")

@app.route("/fourwheeler")
def fourwheeler():
    return render_template("four.html")

@app.route("/<type>/<problem>", methods=["GET"])
def service(type,problem):
    print(type,problem)
    return render_template("contact.html",type=type,problem=problem)

@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/posted", methods=["POST"])
def posted():
    vtype=request.form.get("v-type")
    proble=request.form.get("problem")
    name=request.form.get('name')
    area=request.form.get('area')
    number=request.form.get('number')
    #print(name,area,number,vtype,proble)

    pro=Customer(customer_name=name,customer_vehicle_type=vtype,customer_vehicle_problem=proble,customer_number=number,vehicle_near_area=area)
    db.session.add(pro)
    db.session.commit()
    return render_template("success.html",data=pro)


#--------------------Admin Routes---------------------------------------------------------------------------------------------
@app.route("/admin-dashboard-panel")
def basic_admin():
    data = Customer.query.filter_by(problem_status='pending').all()
    l=len(data)
    # print(data)
    # for i in data :
    #     print(i.customer_name)
    #     print(i.customer_vehicle_type)
    return render_template("admin-index.html",data=data,l=l)

@app.route("/customer-status-update/<int:ids>")
def customerStatusUpdate(ids):
    data = Customer.query.filter_by(customer_id=ids).first()
    data.problem_status="completed"
    db.session.commit()

    return redirect(url_for('basic_admin'))

@app.route("/admin-alldata")
def alldata():
    data = Customer.query.filter_by(problem_status="completed").all()
    da = Customer.query.filter_by(problem_status="pending").all()
    return render_template("admin-alldata.html",c_data=data,p_data=da)

@app.route("/workers-data")
def workersData():
    data=Workers.query.all()
    return render_template("workersdata.html",data=data)

@app.route("/workers", methods=["POST"])
def workersnewdata():
    name=request.form.get("name")
    phone=request.form.get("phone")
    area=request.form.get('area')
    
    pro=Workers(worker_name=name,worker_number=phone,worker_area=area)
    db.session.add(pro)
    db.session.commit()
    return redirect('/workers-data')

@app.route("/worker/del/<value>")
def workerDel(value):
    user=Workers.query.filter_by(worker_id=value).one()
    db.session.delete(user)
    db.session.commit()
    return redirect('/workers-data')


if __name__=='__main__' :
    db.create_all()
    app.run()
