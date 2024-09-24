from qualitycontroll_flask import db
from sqlalchemy import  String, Integer, Numeric, SmallInteger, Boolean, Float, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime as dt
import bcrypt
from flask_login import UserMixin


class Users(db.Model, UserMixin):
    __tablename__ = "users"

    uid = db.Column(Integer, primary_key=True)
    user_name = db.Column(String(128), nullable=False, unique=True)
    password = db.Column(String(512), nullable=False) 
    role = db.Column(String(128), nullable=False)   
    user_number = db.Column(String(10), nullable=True)

    admin = db.Column(Boolean, default=False)
    quality_controll = db.Column(Boolean, default=True)

    def __init__(self, user_name, password, role=None, user_number=None, **permisions):
        self.user_name = user_name
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.role = role
        self.user_number = user_number
        self.admin = permisions["admin"]
        self.quality_controll = permisions["quality_controll"]



    def get_id(self):
        return self.uid
    
    def set_new_password(self, new_password):
        self.password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    def __repr__(self):
        return f"<{self.username}: id {self.uid}, role {self.role}>"
    

class Defects(db.Model):
    __tablename__ = "defects"

    did = db.Column(Integer, primary_key=True, autoincrement=True)
    defect_name = db.Column(String(150), nullable=False)
    description = db.Column(String(512), nullable=True)
    photo_dir = db.Column(String(512), nullable=True)

    def __init__(self, defect_name, description=None, photo_dir=None):
        self.defect_name = defect_name
        self.description = description
        self.photo_dir = photo_dir


class Quality_controlled_items(db.Model):
    __tablename__ = "quality_controlled_items"

    qciid = db.Column(Integer, primary_key=True)
    item_name = db.Column(String(256), nullable=False)
    description = db.Column(String(512), nullable=True)
    photo_dir = db.Column(String(512), nullable=True)

    def __init__(self, item_name, description:None, photo_dir:None):
        
        self.item_name = item_name
        self.description = description
        self. photo_dir = photo_dir


class Work_card(db.Model):
    __tablename__ = "work_card"

    wcid = db.Column(Integer, primary_key=True)
    wc_name = db.Column(String(64), nullable=True)
    qciid = db.Column(Integer, ForeignKey("quality_controlled_items.qciid"))
    uid = db.Column(Integer, ForeignKey("users.uid"))
    quantity = db.Column(Integer, nullable=False)
    creation_time = db.Column(DateTime, default=dt.now())
    close_time = db.Column(DateTime)

    quality_controll_item = relationship("Quality_controlled_items")
    user = relationship("Users")

    def __init__(self, wc_name:str, qciid:int, uid:int, quantity):
        
        self.wc_name=wc_name
        self.qciid = qciid
        self.quantity = quantity
        self.uid = uid

    def close_work_card(self):
        self.close_time = dt.now()


class Quality_controll(db.Model):
    __tablename__ = "quality_controll"

    qcid = db.Column(Integer, primary_key=True)
    wcid = db.Column(Integer, ForeignKey("work_card.wcid"))
    uid = db.Column(Integer, ForeignKey("users.uid"))
    did = db.Column(Integer, ForeignKey("defects.did"))
    date_time = db.Column(DateTime, default=dt.now())
     

    work_card = relationship("Work_card")
    user = relationship("Users")
    defect = relationship("Defects")

    def __init__(self, wcid, uid, did):
        self.wcid = wcid
        self.uid = uid
        self.did = did

    def qc_ids_to_json(self):
        return {
            "wcid": self.wcid,
            "uid": self.uid,
            "did": self.did,
            "date_time": self.date_time
        }