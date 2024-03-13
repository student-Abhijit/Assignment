from flask import *
import random
import sqlite3
from flask import Flask
# sho time and date
from datetime import datetime
# from flask_keycloak import Keycloak

app = Flask(__name__)

app.secret_key="edbujusguxcgqvwdy"
app.config["UPLOAD_FOLDER"]="C:/Users/vaibh/OneDrive/Desktop/Abhijit-talekar/Todo App/static/image/"
import os

# keycloak = Keycloak(app)

# # Configure Keycloak settings
# app.config['KEYCLOAK_REALM'] = 'your_realm'
# app.config['KEYCLOAK_SERVER_URL'] = 'http://your-keycloak-server/auth/'
# app.config['KEYCLOAK_CLIENT_ID'] = 'your_client_id'
# app.config['KEYCLOAK_CLIENT_SECRET'] = 'your_client_secret'




@app.route("/", methods=["GET", "POST"])
def index():
    return redirect(url_for("welcome"))

@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method=="POST":
        Title= request.form["Title"]
        Description= request.form["Description"]
        f=request.files['photo']
        f.save(os.path.join(app.config["UPLOAD_FOLDER"],f.filename))
        
        con=sqlite3.connect("mydb.db")
        cur=con.cursor()
        cur.execute("insert into ToDo(Title,Description,photo)values(?,?,?) ",(Title,Description,f.filename))
        con.commit()
        
        return redirect(url_for("welcome"))
    else:
        return redirect(url_for("inidex"))
  
   
@app.route("/welcome")
def welcome():
    con=sqlite3.connect("mydb.db")
    cur=con.cursor()
    cur.execute("select * from ToDo")
    data=cur.fetchall()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template("welcome.html",data=data, current_time=current_time)
    # return render_template("welcome.html",data=data)

@app.route("/delete/<int:id>")
def delete(id):
    con = sqlite3.connect("mydb.db")
    cur = con.cursor()
    cur.execute("delete from ToDo where id=?",[id])
    con.commit()
   
    return redirect(url_for("welcome"))


@app.route("/edit/<int:id>")
def edit(id):
    con = sqlite3.connect("mydb.db")
    cur = con.cursor()
    cur.execute("select * from ToDo where id=?",[id])
    data = cur.fetchone()
   
    return render_template("edit.html",data=data)




@app.route("/profile_update",methods=["POST","GET"])
def profile_update():
    if request.method =="POST":
        id=request.form['id']
        Title= request.form["Title"]
        Description= request.form["Description"]
        f=request.files['photo']
        
        con = sqlite3.connect("mydb.db")
        cur = con.cursor()
        cur.execute("update ToDo set Title=?, Description=?,photo=? where id=?",(Title,Description,f.filename,id))
        con.commit()


       
        return redirect(url_for("welcome"))
   
    else:
       
        return redirect(url_for("welcome"))



if __name__ == "__main__":
    app.run(debug=True)