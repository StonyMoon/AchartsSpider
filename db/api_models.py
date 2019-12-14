# coding: utf-8
from sqlalchemy import Column, DateTime, Index, Integer, String, Text, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_CONNECT_STRING = 'mysql+pymysql://root:chunxiaoqianhe@localhost:3306/bboard_dev?charset=utf8'
engine = create_engine(DB_CONNECT_STRING, echo=False)
DB_Session = sessionmaker(bind=engine)
session = DB_Session()
BaseModel = declarative_base()
BaseModel.metadata.create_all(engine)

Base = declarative_base()
metadata = Base.metadata
song_singer = Table('song_singer', metadata,
                    Column('song_id', Integer, ForeignKey('song.id')),
                    Column('singer_id', Integer, ForeignKey('singer.id'))
                    )


class Billboard(Base):
    __tablename__ = 'billboard'
    __table_args__ = (
        Index('rank', 'date', 'song_id'),
    )
    # id计算：180613 100名次
    id = Column(Integer, primary_key=True)
    previous = Column(Integer)
    weeks = Column(Integer)
    peak = Column(Integer)
    rank = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)
    song_id = Column('song_id', Integer, ForeignKey('song.id'))


class Singer(Base):
    __tablename__ = 'singer'

    id = Column(Integer, primary_key=True)
    image = Column(String(255))
    name = Column(String(255))
    info = Column(Text)
    area = Column(String(255))
    type = Column(String(255))
    born = Column(DateTime)
    songs = relationship('Song', secondary=song_singer)


class Song(Base):
    __tablename__ = 'song'

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    singers = relationship('Singer', secondary=song_singer)

    def __repr__(self):
        return self.title


if __name__ == '__main__':
    Base.metadata.create_all(engine)
