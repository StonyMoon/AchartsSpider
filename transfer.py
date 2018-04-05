from Cache import session
from models import Song, Singer, Billboard, Songonbillboard, Songtosinger
from models_api import Song as ApiSong, Singer as ApiSinger, Billboard as ApiBillboard

from bboard import db
# songs = session.query(Song).all()
# for each in songs:
#     db.session.add(ApiSong(id=each.id,title=each.title))
# db.session.commit()
#
#
# singers = session.query(ApiSinger).all()
# for each in singers:
#     db.session.add(ApiSinger(url=each.url,image=each.image,name=each.name,
#                              info=each.info,area=each.area,type=each.type,born=each.born))
# db.session.commit()


# billboards = session.query(Billboard).all()
# for each in billboards:
#     billboard_date = each.date
#     y = billboard_date.year%2000 * 10e6
#     m = billboard_date.month * 10e4
#     d = billboard_date.day * 10e2
#     id = int(each.rank + y+m+d)
#     db.session.add(ApiBillboard(id=id,previous=each.previous,
#                                 weeks=each.weeks,peak=each.peak,
#                                 rank=each.rank,date=each.date
#                                 ))
# db.session.commit()

# singer_song = session.query(Songtosinger).all()

# songs = db.session.query(ApiSong).all()
#
# for each in songs:
#     singer_song = session.query(Songtosinger).filter_by(songId=each.id).all()
#     for singer in singer_song:
#         s = db.session.query(ApiSinger).filter_by(url=singer.singerName).first()
#         each.singers.append(s)
#         db.session.add(each)
#     db.session.commit()




# songs = db.session.query(ApiSong).all()
#
# for each in songs:
#     billboard_song = session.query(Songonbillboard).filter_by(songId=each.id).all()
#     for billboard_item in billboard_song:
#         billboard_date = billboard_item.billboardDate
#         y = billboard_date.year%2000 * 10e6
#         m = billboard_date.month * 10e4
#         d = billboard_date.day * 10e2
#         id = int(billboard_item.billboardRank + y+m+d)
#         s = db.session.query(ApiBillboard).filter_by(id=id).first()
#         each.billboards.append(s)
#         db.session.add(each)
# db.session.commit()
