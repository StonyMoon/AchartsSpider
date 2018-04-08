from Cache import session
from models import Song, Singer, Billboard, Songonbillboard, Songtosinger
from models_api import Song as ApiSong, Singer as ApiSinger, Billboard as ApiBillboard

from bboard import db

# songs = session.query(Song).all()
# for each in songs:
#     db.session.add(ApiSong(id=each.id,title=each.title))
# db.session.commit()


# i = 0
# singers = session.query(Singer).all()
# for each in singers:
#     db.session.add(ApiSinger(id=i,image=each.image,name=each.name,
#                              info=each.info,area=each.area,type=each.type,born=each.born))
#     i+=1
# db.session.commit()


billboards = session.query(Billboard).all()
for each in billboards:
    song_id = session.query(Songonbillboard).filter_by(billboardRank=each.rank, billboardDate=each.date).first().songId

    billboard_date = each.date
    y = billboard_date.year % 2000 * 10e6
    m = billboard_date.month * 10e4
    d = billboard_date.day * 10e2
    id = int(each.rank + y + m + d)
    try:
        db.session.add(ApiBillboard(id=id, previous=each.previous,
                                    weeks=each.weeks, peak=each.peak,
                                    rank=each.rank, date=each.date, song_id=song_id,
                                    ))
        db.session.commit()
    except Exception:
        db.session.rollback()


# singer_song = session.query(Songtosinger).all()
        #
# songs = db.session.query(ApiSong).all()
#
# for each in songs:
#     singer_song = session.query(Songtosinger).filter_by(songId=each.id).all()
#     for singer in singer_song:
        #         ss = session.query(Singer).filter_by(url=singer.singerName).first()
        #         s = db.session.query(ApiSinger).filter_by(name=ss.name,area=ss.area,type=ss.type,born=ss.born).first()
#         each.singers.append(s)
#         db.session.add(each)
# db.session.commit()
        #
