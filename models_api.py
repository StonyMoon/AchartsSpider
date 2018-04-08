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


class TimeItem(fields.Raw):
    def format(self, value):
        return str(value.year) + '-' + str(value.month) + '-' + str(value.day)


class RankItem(fields.Raw):
    def format(self, value):
        l = [x.rank for x in value]
        return l



song_singer = db.Table('song_singer', db.Model.metadata,
                       db.Column('song_id', db.Integer, db.ForeignKey('song.id')),
                       db.Column('singer_id', db.Integer, db.ForeignKey('singer.id'))
                       )




class Billboard(db.Model):
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
    song_id = db.Column('song_id', db.Integer, db.ForeignKey('song.id'))



class Singer(db.Model):
    __tablename__ = 'singer'

    id = Column(Integer, primary_key=True)
    image = Column(String(255))
    name = Column(String(255))
    info = Column(Text)
    area = Column(String(255))
    type = Column(String(255))
    born = Column(DateTime)
    songs = db.relationship('Song', secondary=song_singer)


class Song(db.Model):
    __tablename__ = 'song'

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    singers = db.relationship('Singer', secondary=song_singer)

    def __repr__(self):
        return self.title


song_simple_field = {
    'id': fields.Integer,
    'title': fields.String
}

singer_name_fields = {
    'name': fields.String,
    'id': fields.Integer
}

billboard_fields = {
    'previous': fields.Integer,
    'weeks': fields.Integer,
    'peak': fields.Integer,
    'rank': fields.Integer,
    'songs': song_simple_field
}

singer_profile_fields = {
    'id': fields.Integer,
    'image': fields.String,
    'name': fields.String,
    'info': fields.String,
    'area': fields.String,
    'type': fields.String,
    'born': TimeItem()
}

singer_fields = {
    'image': fields.String,
    'name': fields.String,
    'info': fields.String,
    'area': fields.String,
    'type': fields.String,
    'born': TimeItem(),
    'songs': fields.List(fields.Nested(song_simple_field))
}

song_with_singer_field = {
    'id': fields.Integer,
    'title': fields.String,
    'singers': fields.List(fields.Nested(singer_name_fields))

}

song_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'ranks': RankItem(attribute='billboards'),
    'singers': fields.List(fields.Nested(singer_profile_fields))
}

if __name__ == '__main__':
    db.create_all()