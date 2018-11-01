# 爬虫爬取到默认放置的位置

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DB_CONNECT_STRING = 'mysql+mysqldb://root:root@localhost/bboard?charset=utf8'
engine = create_engine(DB_CONNECT_STRING, echo=False)
DB_Session = sessionmaker(bind=engine)
session = DB_Session()
BaseModel = declarative_base()

BaseModel.metadata.create_all(engine)
