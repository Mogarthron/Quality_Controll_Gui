from flask import Flask, render_template, redirect, url_for, request, jsonify, flash 
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

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


class Login_form(FlaskForm):
    username = StringField('Username',  validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')



@app.route("/login", methods=["GET", "POST"])
def login():

    if db.session.query(Users).count() == 0:
            print("brak userów!!!!")                   
            return redirect(url_for("dodaj_urzytkownika"))
          
    form = Login_form()
    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data       
       
        user = db.session.query(Users).filter(Users.username == username).first()

        if user and user.check_password(password):  
            login_user(user)  
            flash('Logged in successfully.', 'success')
            return redirect(url_for('index'))  
        
        else:
            flash('Invalid username or password', 'danger')  

    return render_template('login.html', form=form)




@app.route("/dodaj_urzytkownika", methods=["POST", "GET"])
def dodaj_urzytkownika():

    if request.method == "POST":
        new_user = request.form["nazwaUrzytkownika"]
        new_user_role = request.form["rolaUrzytkownika"]
        new_user_password = request.form["hasloUrzytkownika"]

        db.session.add(Users(new_user, new_user_password, new_user_role))
        db.session.commit()

        return redirect(url_for('login'))

    return render_template("dodaj_urzytkownika.html")


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