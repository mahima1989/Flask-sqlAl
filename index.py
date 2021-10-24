from flask import Flask,redirect,url_for,render_template,request,session
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)
app.secret_key="Sab moh maya hai"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False




db = SQLAlchemy(app)
class users(db.Model):
   id = db.Column("id", db.Integer, primary_key = True)
   name = db.Column(db.String(100))
   email = db.Column(db.String(100))  
  

def __init__(self,name,email):
   self.name = name
   self.email = email
  




@app.route("/")
def home():
    return render_template("index.html") 

@app.route("/view")
def view():
    return render_template("view.html",values=users.query.all())    




@app.route("/login",methods=["POST","GET"])
def login():
        if request.method=="POST":
            user=request.form["nm"]
            email=request.form["email"]
            session["user"]=user
            

            #database code 
            found_user=users.query.filter_by(name=user).first()
            if found_user:
                session["email"]=found_user.email
            else: 
                usr=users(name=user,email=email)   
                db.session.add(usr)
                db.session.commit() 
                session["email"]=email

            return redirect(url_for("user"))
        else :
            return render_template("login.html")    


@app.route("/user")
def user():
    if "user" in session:

         user=session["user"]
         email=session["email"]
         
         return f"<h1> hello {user} with email id {email} </h1>"
    else:
        return redirect(url_for("login"))



@app.route("/logout") 
def logout():
    session.pop("user",None)
    session.pop("email",None)
    return redirect(url_for("login"))       



   







if __name__=="__main__":
    db.create_all()
    app.run(debug=True)