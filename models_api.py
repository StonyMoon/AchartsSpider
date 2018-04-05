# coding: utf-8
from flask_restful import fields
from bboard import db

Column = db.Column
Integer = db.Integer
DateTime = db.DateTime
String = db.String
Text = db.Text
Date = db.Date
Index = db.Index

song_singer = db.Table('song_singer', db.Model.metadata,
                       db.Column('song_id', db.Integer, db.ForeignKey('song.id')),
                       db.Column('singer_url', db.String(255), db.ForeignKey('singer.url'))
                       )

song_billboard = db.Table('song_billboard', db.Model.metadata,
                          db.Column('song_id', db.Integer, db.ForeignKey('song.id')),
                          db.Column('billboard_id', db.Integer, db.ForeignKey('billboard.id')),
                          )


class Billboard(db.Model):
    __tablename__ = 'billboard'
    __table_args__ = (
        Index('rank', 'rank', 'date'),
    )
    # id计算：180613 100名次
    id = Column(Integer, primary_key=True)
    previous = Column(Integer)
    weeks = Column(Integer)
    peak = Column(Integer)
    rank = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)
    songs = db.relationship('Song', secondary=song_billboard)


class Singer(db.Model):
    __tablename__ = 'singer'

    url = Column(String(255), primary_key=True)
    image = Column(String(255))
    name = Column(String(255))
    info = Column(Text)
    area = Column(String(255))
    type = Column(String(255))
    born = Column(Date)
    songs = db.relationship('Song', secondary=song_singer)

    fields = {
        'image': fields.Integer,
        'name': fields.String,
        'info': fields.String,
        'area': fields.String,
        'type': fields.String,
        'born': fields.DateTime
    }


class Song(db.Model):
    __tablename__ = 'song'

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    billboards = db.relationship('Billboard', secondary=song_billboard)
    singers = db.relationship('Singer', secondary=song_singer)

    def __repr__(self):
        return self.title


if __name__ == '__main__':
    db.create_all()
    # a = db.session.query(Singer).filter_by(song='drake').first()
    # for each in a.songs:
    #     print(each)
