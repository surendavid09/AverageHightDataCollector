from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email
from sqlalchemy.sql import func

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI']='postgresql+psycopg2://postgres:postgres123@localhost/height_collector'
app.config['SQLALCHEMY_DATABASE_URI']='postgres://gzszbiazhqrizv:8cee839873db2a5887ebc76914d024b1a555ec378244964e43b193d50a409685@ec2-34-203-255-149.compute-1.amazonaws.com:5432/d3lj4n9d38pu0e?sslmode=required'

db=SQLAlchemy(app)

#create model for table - column parameters -- create database model object
class Data(db.Model):
    __tablename__="data"
    id=db.Column(db.Integer, primary_key=True)
    email_=db.Column(db.String(120), unique=True)
    height_=db.Column(db.Integer)

    def __init__(self, email, height):
        self.email_=email
        self.height_=height


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success",methods=['POST'])
def success():
    if request.method=="POST":
        #assign values to variables to transfer to database
        email=request.form["email_name"]
        height=request.form["height_name"]


        #add values to database
        if db.session.query(Data).filter(Data.email_==email).count() == 0:
            data=Data(email,height)
            db.session.add(data)
            db.session.commit()

            #calculate average of height .scalar to extract number
            average_height=db.session.query(func.avg(Data.height_)).scalar()
            average_height=round(average_height,1)
            count=db.session.query(Data.height_).count()
            send_email(email, height, average_height, count)
            print(average_height)
            return render_template("success.html")

    #if not  render index.html page instead
    return render_template("index.html",
    text="Seems like we've got something from that email address already!")

if __name__ == '__main__':
    app.debug=True
    app.run()
