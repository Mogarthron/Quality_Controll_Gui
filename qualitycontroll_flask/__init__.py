from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import URL, create_engine, text



app = Flask(__name__, template_folder='templates')

url_obj = URL.create(drivername="mysql+mysqlconnector",
                     username="root",
                     password="password",
                     host="127.0.0.1",
                     port=3306,
                     database="Quality_Controll_db"
                     )


db = SQLAlchemy()

def create_app(db_url=url_obj):

    engine = create_engine(url_obj)
    with engine.connect() as conn:
        conn.execute(text("CREATE DATABASE IF NOT EXISTS Quality_Controll_db"))

        conn.close()

    # del engine

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.secret_key = "SUPER SECRET KEY"

    db.init_app(app)

    from .routes import index, login, logout, quality_controll

    migrate = Migrate(app, db)

    return app
