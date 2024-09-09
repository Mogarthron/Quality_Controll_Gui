from flask import Flask, render_template, request, jsonify 
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

from qualitycontroll_flask import app
from qualitycontroll_flask.models import *

login_manager = LoginManager()
login_manager.init_app(app=app)

@login_manager.user_loader
def load_user(uid):
    return db.session.query(Users).get(uid) 

@app.route('/', methods=["GET", "POST"])
def index():
    return render_template("index.html", user=current_user)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    elif request.method == "POST":
        username = request.form.get("userName")
        haslo = request.form.get("password")

        # user = User.query.filter(User.username == username).first()        
        user = db.session.query(Users).filter(Users.username == username).first()        

        if user.haslo == haslo:
            login_user(user)
            return render_template("index.html")
        else:
            return "FILED!!!!!!!"

@app.route("/logout")
def logout():
    logout_user()
    return render_template("index.html")

@app.route("/quality_controll", methods=["POST", "GET"])
@login_required
def quality_controll():

    glass_defects = ["Pladra zamknięta",
"Pladra otwarta",
"Wtrącenie ceramiczne",
"Wtrącenie ceramiczne z pladerkami",
"Wtrącenie ceramiczne 5mm",
"Wtrącenie ceramiczne 10mm",
"Smuga capierzasta",
"Nić z pladrą na poczatku",
"Nić z pladrą w środku"
]
   
    
    return render_template("quality_controll.html", glass_defects=glass_defects)