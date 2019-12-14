# coding: utf-8
from sqlalchemy import Column, Date, DateTime, Index, Integer, String, Text
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_CONNECT_STRING = 'mysql+pymysql://root:chunxiaoqianhe@localhost:3306/bboard?charset=utf8'
engine = create_engine(DB_CONNECT_STRING, echo=False)
DB_Session = sessionmaker(bind=engine)
session = DB_Session()
BaseModel = declarative_base()

BaseModel.metadata.create_all(engine)
Base = declarative_base()
metadata = Base.metadata


class Billboard(Base):
    __tablename__ = 'billboard'
    __table_args__ = (
        Index('rank', 'rank', 'date'),
    )

    def __init__(self, previous, weeks, peak, rank, date):
        self.previous = previous
        self.weeks = weeks
        self.peak = peak
        self.rank = rank
        self.date = date

    previous = Column(Integer)
    weeks = Column(Integer)
    peak = Column(Integer)
    rank = Column(Integer, primary_key=True, nullable=False)
    date = Column(DateTime, primary_key=True, nullable=False)


class Chart(Base):
    def __init__(self, year, week):
        self.year = year
        self.week = week

    __tablename__ = 'chart'
    id = Column(Integer, primary_key=True)
    year = Column(Integer)
    week = Column(Integer)


class Singer(Base):
    __tablename__ = 'singer'

    url = Column(String(255), primary_key=True)
    id = Column(Integer)
    image = Column(String(255))
    name = Column(String(255))
    info = Column(Text)
    area = Column(String(255))
    type = Column(String(255))
    born = Column(Date)


class Song(Base):
    __tablename__ = 'song'

    def __init__(self, id, title):
        self.id = id
        self.title = title

    id = Column(Integer, primary_key=True)
    title = Column(String(255))


class Songonbillboard(Base):
    __tablename__ = 'songonbillboard'
    __table_args__ = (
        Index('billboardRank', 'billboardRank', 'billboardDate'),
    )

    id = Column(Integer, primary_key=True)
    songId = Column(Integer, index=True)
    billboardDate = Column(DateTime)
    billboardRank = Column(Integer)


class Songtosinger(Base):
    __tablename__ = 'songtosinger'

    def __init__(self, songId, singerName):
        self.songId = songId
        self.singerName = singerName

    id = Column(Integer, primary_key=True)
    songId = Column(Integer, index=True)
    singerName = Column(String(255), index=True)


if __name__ == '__main__':
    Base.metadata.create_all(engine)
