from flask import Flask,render_template,request,redirect,session,url_for,jsonify
import re
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = "super secret key"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'STL@1234'
app.config['MYSQL_DB'] = 'msproject'
 
mysql = MySQL(app)

@app.route("/")
def hello_world():
    return "Hi there!! It's working..."

@app.route('/reg',methods=['POST','Get'])
def reg():
    if request.method=='POST':
        Name = request.form["Name"]
        Email = request.form["Email"]
        Password = request.form["Password"]
        Speciality = request.form["Speciality"]
        cur = mysql.connection.cursor()
        cur.execute("Select * from patient_details where Email = %s",(Email, ))
        account = cur.fetchone()
        if account:
           return jsonify("Account already exists!")
        elif not re.match(r'[^@]+@[^@]+\.[^@]+',Email):
           return jsonify("Invalid email address! ")
        elif not Name or not Password or not Email:
           return jsonify("Please fill out the form!")
        cur.execute("INSERT INTO patient_details(Name,Email,Password,Speciality) VALUES(%s,%s,%s,%s)",(Name,Email,Password,Speciality))
        mysql.connection.commit()
        cur.close()
        return jsonify("Successfully Registered")
    return jsonify("Failed")

if __name__ == '__main__':
    app.run(debug=True) 