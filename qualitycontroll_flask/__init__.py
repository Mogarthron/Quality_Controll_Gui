from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__, template_folder='templates')

db = SQLAlchemy()

def create_app(db_url="sqlite:///./QC.db"):
    
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.secret_key = "SUPER SECRET KEY"

    db.init_app(app)

    from .routes import index, login, logout, quality_controll

    migrate = Migrate(app, db)

    return app
