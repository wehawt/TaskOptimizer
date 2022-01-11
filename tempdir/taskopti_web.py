from flask import json, url_for
from flask import redirect
from flask import jsonify
from flask import request
from flask import Flask
from flask import render_template
import sqlite3 as sql

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime
from sqlalchemy import text



task_app = Flask(__name__)
task_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ordering.sqlite'
task_app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(task_app)
ma = Marshmallow(task_app)

#----------------CREATING USER TABLE---------------------
class User(db.Model):
    tablename = "user"
    user_id = db.Column(db.String(50), primary_key=True)
    user_fname = db.Column(db.String(50))
    user_lname = db.Column(db.String(50))
    user_email = db.Column(db.String(50))
    user_password = db.Column(db.String(50))
    user_number = db.Column(db.String(50))
    user_address = db.Column(db.String(50))
    user_city = db.Column(db.String(50))
    user_zipcode = db.Column(db.String(50))


    def __init__(self, user_id, user_fname, user_lname, user_email, user_password, user_number, user_address, user_city, user_zipcode):
        self.user_id = user_id
        self.user_fname = user_fname
        self.user_lname = user_lname
        self.user_email = user_email
        self.user_password = user_password
        self.user_number = user_number
        self.user_address = user_address
        self.user_city = user_city
        self.user_zipcode = user_zipcode


class UserSchema(ma.Schema):
    class Meta:
        fields = ("user_id", "user_fname" , "user_lname", "user_email", "user_password", "user_number", "user_address", "user_city", "user_zipcode")

user_schema = UserSchema()
users_schema = UserSchema(many=True)


#----------------CREATING LOG table---------------------
class Log(db.Model):
    tablename = "log"
    log_id = db.Column(db.String(50), primary_key=True)
    user_email = db.Column(db.String(50))
    date_logged = db.Column(db.String(50))

    def __init__(self, log_id, user_email, date_logged):
        self.log_id = log_id
        self.user_email = user_email
        self.date_logged = date_logged



class LogSchema(ma.Schema):
    class Meta:
        fields = ("log_id","user_email", "date_logged")

log_schema = LogSchema()
logs_schema = LogSchema(many=True)




#----------------CREATING PRODUCT table---------------------
class Product(db.Model):
    tablename = "product"
    prod_id = db.Column(db.String(50), primary_key=True)
    prod_name = db.Column(db.String(50))
    price = db.Column(db.Integer)

    def __init__(self, prod_id, prod_name, price):
        self.prod_id = prod_id
        self.prod_name = prod_name
        self.price = price



class ProductSchema(ma.Schema):
    class Meta:
        fields = ("prod_id", "prod_name", "price")

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


#----------------CREATING ORDER TABLE---------------------
class Order(db.Model):
    tablename = "order"
    order_id = db.Column(db.String(50), primary_key=True)
    user_id = db.Column(db.String(50))
    prod_id = db.Column(db.String(50))
    order_quantity = db.Column(db.Integer)
    date_ordered = db.Column(db.String(50))
    price = db.Column(db.String(50))

    def __init__(self, order_id, user_id, prod_id, order_quantity, date_ordered, price):
        self.order_id = order_id
        self.user_id = user_id
        self.prod_id = prod_id
        self.order_quantity = order_quantity
        self.date_ordered = date_ordered
        self.price = price


class OrderSchema(ma.Schema):
    class Meta:
        fields = ("order_id", "user_id" , "prod_id", "order_quantity", "date_ordered", "price")

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)


#----------------CREATING SUMMARY TABLE---------------------
class Summary(db.Model):
    tablename = "summary"
    summary_id = db.Column(db.String(50), primary_key=True)
    user_id = db.Column(db.String(50))
    prod_id = db.Column(db.String(50))
    order_quantity = db.Column(db.Integer)
    date_ordered = db.Column(db.String(50))
    price = db.Column(db.String(50))

    def __init__(self, summary_id, user_id, prod_id, order_quantity, date_ordered, price):
        self.summary_id = summary_id
        self.user_id = user_id
        self.prod_id = prod_id
        self.order_quantity = order_quantity
        self.date_ordered = date_ordered
        self.price = price


class SummarySchema(ma.Schema):
    class Meta:
        fields = ("summary_id", "user_id" , "prod_id", "order_quantity", "date_ordered", "price")

summary_schema = SummarySchema()
summarys_schema = SummarySchema(many=True)

#--------------------RENDERING---------------------------

#------MY home.html is my signin.html-----
@task_app.route("/", methods=['POST','GET'])
def home():
    if request.method == 'POST':
        return redirect(url_for('home'))
    return render_template("home.html")
#------MY home.html is my signin.html-----

@task_app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        return redirect(url_for('signup'))
    return render_template("signup.html")


@task_app.route('/menu', methods=['POST','GET'])
def menu():  
    return render_template("menu.html")


@task_app.route('/about',methods=['POST','GET'])
def about():
    if request.method == 'POST':
        return redirect(url_for('about'))
    return render_template("Aboutus.html")

@task_app.route('/ordersum',methods=['POST','GET'])
def ordersum():
    subtotal=0
    total=0
    que = Summary.query.all()
    email = Log.query.with_entities(Log.user_email).order_by(Log.log_id.desc()).first()[0]
    user_fname = User.query.with_entities(User.user_fname).filter_by(user_email = email).first()[0]
    res = summarys_schema.dump(que)

    tup_prices = Summary.query.with_entities(Summary.price).all()

    for price in tup_prices:
        subtotal = subtotal + int(price[0])
        
    total = subtotal + 59

    return render_template('ordersummary.html', rows = res, product_price = subtotal, total_price = total, user = user_fname)


#--------------------render---------------------------




@task_app.route('/regis', methods=['POST'])
def regis():  
    if request.method == 'POST':
        json_data = request.get_json()
        user_id = datetime.now().strftime("%m%d%H%M%S")
        user_fname = json_data[0]["fname_signup"]
        user_lname = json_data[0]["lname_signup"]
        user_email = json_data[0]['email_signup']
        user_password = json_data[0]['password_signup']
        user_number = json_data[0]['number_signup']
        user_address = json_data[0]['address_signup']
        user_city = json_data[0]['city_signup']
        user_zipcode = json_data[0]['zipcode_signup']

        user = User.query.filter_by(user_email=user_email).first()
        user = user_schema.dump(user)
        

        if len(user)==0:
            new_user = User(user_id, user_fname, user_lname, user_email, user_password, user_number, user_address, user_city, user_zipcode)
            db.session.add(new_user)
            db.session.commit()

            message = {"message":"Account Created Successfuly"}
            # message = {"message":"Email is already taken"}

        else:
            message = {"message":"Email is already taken"}

        return jsonify(message)



@task_app.route('/validate', methods=['POST','DELETE'])
def validate():
    if request.method == 'POST':

        json_data = request.get_json()
        email = json_data[0]["email"]
        password = json_data[0]["password"]
        log_id = datetime.now().strftime("%m%d%H%M%S")
        date_logged = datetime.now().strftime("%m/%d/%H")
        user = User.query.filter_by(user_email=email).first()
        user = user_schema.dump(user)
        


        if(len(user)>0):
            if (user['user_password'] == password):
                message = {"message":"Successfuly logged in"}


                new_log = Log(log_id,email,date_logged)
                db.session.add(new_log)
                db.session.commit()

                # print(Log.query.with_entities(Log.user_email).first()[0]) #PRINTING CHECK
                

            else:
                user = None
                message = {"message":"Incorrect Credentials"}

        else:
            user = None
            message = {"message":"Incorrect Credentials"}

    return jsonify(message)






@task_app.route('/addorder', methods=['GET','POST'])
def addorder():  
    if request.method == 'POST':
        
        json_data = request.get_json()
        productID = json_data[0]["prod_id"] #dipa sure , dagdagan ng "[0]" para ma alis sa tuple
        order_quantity = json_data[0]["quantity"]


        order_id = datetime.now().strftime("%m%d%H%M%S")
        user_id = Log.query.with_entities(Log.user_email).first()[0]
        date_ordered = datetime.now().strftime("%m/%d/%H/%M/%S")

        
        price = Product.query.filter_by(prod_id = productID).first()
        row = product_schema.dump(price)
        price = row['price']
        totalprice = order_quantity * price

        # price = int(order_quantity) * int(Product.query.with_entities(Product.price).filter_by(prod_id = productID)[0][0])  #dipa sure, dagdagan ng "[0]" para ma alis sa tuple
        new_order = Order(order_id, user_id, productID, order_quantity, date_ordered, totalprice)
        db.session.add(new_order)
        new_summary = Summary(order_id, user_id, productID, order_quantity, date_ordered, totalprice)
        db.session.add(new_summary)
        db.session.commit()
        
        message = {"message":"Order Placed Successfully"}
        return jsonify(message)


# checkRows = Summary.query.with_entities(Summary.summary_id).first()
@task_app.route('/checkorder', methods=['POST','GET'])
def checkorder():  
    if request.method == 'POST':
        checkRows = Summary.query.with_entities(Summary.summary_id).first()
        
        if checkRows != None:
            message = {"message":"There is"}
        else:
            message = {"message":"There is none"}
        return jsonify(message)


@task_app.route('/deletesummary', methods=['DELETE'])
def deletesummary():  
    if request.method == 'DELETE':
        
        db.session.query(Summary).delete()
        db.session.commit()

        message = {"message":"Deleted Successfully"}
    return jsonify(message)







if __name__ == "__main__":
    db.create_all()
    task_app.run(host="0.0.0.0", port=8080 , debug=True)