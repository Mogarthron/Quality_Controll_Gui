from QC_db import Base
from sqlalchemy import Column, String, Integer, Numeric, SmallInteger, Boolean, Float, Date, DateTime
from datetime import datetime as dt
import bcrypt
from flask_login import UserMixin


class Users(Base, UserMixin):
    __tablename__ = "users"

    uid = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role =  Column(String, nullable=True)

    def __init__(self, username, password, role):
        self.username = username
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.role = role

    def get_id(self):
        return self.uid
    
    def set_new_password(self, new_password):
        self.password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    def __repr__(self):
        return f"<utowrzono: {self.username} z id {self.uid}, rola: {self.role}>"

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

    iid = Column(Integer, primary_key=True)
    item_name = Column(String(256), nullable=False)
    description = Column(String(512), nullable=True)
    photo_dir = Column(String(512), nullable=True)




class Work_card(Base):
    __tablename__ = "work_card"

    wcid = Column(Integer, primary_key=True)
    wc_name = Column(String(64), nullable=True)
    qciid = Column(Integer, nullable=False)
    creation_time = Column(DateTime, default=dt.now())
    close_time = Column(DateTime)
