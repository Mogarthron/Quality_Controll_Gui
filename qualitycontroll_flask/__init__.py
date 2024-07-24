from flask import Flask 
from flask_login import LoginManager, login_user, logout_user, current_user, login_required


app = Flask(__name__, template_folder="templates")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./appdb.db"
app.secret_key = "SUPER SECRET KEY"

from qualitycontroll_flask.routes import *

login_manager = LoginManager()
login_manager.init_app(app=app)

@login_manager.user_loader
def load_user(uid):
    return User.query.get(uid) 

with app.app_context():
    db.create_all()

