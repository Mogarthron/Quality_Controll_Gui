from QC_db import Base
from sqlalchemy import Column, String, Integer, Numeric, SmallInteger, Boolean, Float, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime as dt
import bcrypt
from flask_login import UserMixin


class Users(Base, UserMixin):
    __tablename__ = "users"

    uid = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role =  Column(String, nullable=True)
    user_number = Column(String(10), nullable=True)

    def __init__(self, username, password, role, user_number=None):
        self.username = username
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.role = role
        self.user_number = user_number

    def get_id(self):
        return self.uid
    
    def set_new_password(self, new_password):
        self.password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    def __repr__(self):
        return f"<utowrzono: {self.username} z id {self.uid}, rola: {self.role}>"


class User_permissions(Base):
    __tablename__ = "user_permissions"

    upid = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey("users.uid"))
    admin = Column(Boolean, default=False)
    quality_controll = Column(Boolean, default=True)

    users = relationship("Users")

    def __init__(self, uid, quality_controll:bool, admin=False):

        self.uid = uid
        self.admin = admin
        self.quality_controll = quality_controll

    

class Defects(Base):
    __tablename__ = "defects"

    did = Column(Integer, primary_key=True, autoincrement=True)
    defect_name = Column(String(150), nullable=False)
    description = Column(String(512), nullable=True)
    photo_dir = Column(String(512), nullable=True)

    def __init__(self, defect_name, description=None, photo_dir=None):
        self.defect_name = defect_name
        self.description = description
        self.photo_dir = photo_dir


class Quality_controlled_items(Base):
    __tablename__ = "quality_controlled_items"

    qciid = Column(Integer, primary_key=True)
    item_name = Column(String(256), nullable=False)
    description = Column(String(512), nullable=True)
    photo_dir = Column(String(512), nullable=True)

    def __init__(self, item_name, description:None, photo_dir:None):
        
        self.item_name = item_name
        self.description = description
        self. photo_dir = photo_dir


class Work_card(Base):
    __tablename__ = "work_card"

    wcid = Column(Integer, primary_key=True)
    wc_name = Column(String(64), nullable=True)
    qciid = Column(Integer, ForeignKey("quality_controlled_items.qciid"))
    uid = Column(Integer, ForeignKey("users.uid"))
    quantity = Column(Integer, nullable=False)
    creation_time = Column(DateTime, default=dt.now())
    close_time = Column(DateTime)

    quality_controll_item = relationship("Quality_controlled_items")
    user = relationship("Users")

    def __init__(self, wc_name:str, qciid:int, uid:int, quantity):
        
        self.wc_name=wc_name
        self.qciid = qciid
        self.quantity = quantity
        self.uid = uid

    def close_work_card(self):
        self.close_time = dt.now()


class Quality_controll(Base):
    __tablename__ = "quality_controll"

    qcid = Column(Integer, primary_key=True)
    wcid = Column(Integer, ForeignKey("work_card.wcid"))
    uid = Column(Integer, ForeignKey("users.uid"))
    did = Column(Integer, ForeignKey("defects.did"))
    date_time = Column(DateTime, default=dt.now())
     

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