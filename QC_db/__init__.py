from sqlalchemy import create_engine
from sqlalchemy import URL

from sqlalchemy.orm import sessionmaker, declarative_base
import json

Base = declarative_base()

# url_obj = URL.create("mysql+mysqlconnector",
#                      username=mip_url["username"],
#                      password=mip_url["password"],
#                      host=mip_url["host"],
#                      port=mip_url["port"],
#                      database=mip_url["database"]
#                      )
from QC_db.models import * 

def create_db(url="sqlite:///QC.db"):
    
    db_engine = create_engine(url, echo=False)
 
    Base.metadata.create_all(bind=db_engine)
    Session = sessionmaker(bind=db_engine)
    db_session = Session()

    db_session.add(Users("admin", "admin", "admin"))
    db_session.commit()



def connect_to_db(url="sqlite:///QC.db"):
    
    db_engine = create_engine(url, echo=False)
    Session = sessionmaker(bind=db_engine)
    db_session = Session()

    return db_engine, db_session
