# coding: utf-8
from sqlalchemy import Column, Date, DateTime, Index, Integer, String, Table, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()
metadata = Base.metadata


class Billboard(Base):


    def __init__(self,pre,weeks,peak,rank,date):
        self.previous =pre
        self.weeks = weeks
        self.peak = peak
        self.rank = rank
        self.date = date


    __tablename__ = 'billboard'
    __table_args__ = (
        Index('rank', 'rank', 'date'),
    )
    songs = relationship('Song', secondary=t_songonbillboard)
    previous = Column(Integer)
    weeks = Column(Integer)
    peak = Column(Integer)
    rank = Column(Integer, primary_key=True, nullable=False)
    date = Column(DateTime, primary_key=True, nullable=False)


class Singer(Base):
    __tablename__ = 'singer'

    name = Column(String(255), primary_key=True)
    image = Column(String(255))
    info = Column(Text)
    area = Column(String(255))
    born = Column(Date)


class Song(Base):
    __tablename__ = 'song'

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    billboards = relationship('Billboard', secondary=t_songonbillboard)

t_songonbillboard = Table(
    'songonbillboard', metadata,
    Column('songId', Integer, index=True),
    Column('billboardDate', DateTime),
    Column('billboardRank', Integer),
    Index('billboardRank', 'billboardRank', 'billboardDate')
)


t_songtosinger = Table(
    'songtosinger', metadata,
    Column('songId', Integer, index=True),
    Column('singerName', String(255), index=True)
)
