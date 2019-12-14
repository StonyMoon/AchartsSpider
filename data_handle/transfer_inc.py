from db.api_models import session as api_session
from db.api_models import Billboard as ApiBillboard
from db.api_models import Singer as ApiSinger, Song as ApiSong
from db.models import session
from db.models import Billboard, Songonbillboard, Song, Singer, Songtosinger

songs = session.query(Song).all()
for each in songs:
    api_song = api_session.query(ApiSong).filter_by(id = each.id).first()
    if api_song is None:
        api_session.add(ApiSong(id=each.id, title=each.title))
api_session.commit()


singers = session.query(Singer).all()
for each in singers:
    api_singer = api_session.query(ApiSinger).filter_by(id=each.id).first()
    if api_singer is None:
        api_session.add(ApiSinger(id=each.id, image=each.image, name=each.name,
                              info=each.info, area=each.area, type=each.type, born=each.born))
api_session.commit()

print('billboard start')
billboards = session.query(Billboard).order_by(Billboard.date.desc()).all()
for each in billboards:
    if api_session.query(ApiBillboard).filter_by(date=each.date).first():
        break
    song_id = session.query(Songonbillboard).filter_by(billboardRank=each.rank, billboardDate=each.date).first().songId
    billboard_date = each.date
    y = billboard_date.year % 2000 * 10e6
    m = billboard_date.month * 10e4
    d = billboard_date.day * 10e2
    id = int(each.rank + y + m + d)
    api_session.add(ApiBillboard(id=id, previous=each.previous,
                                     weeks=each.weeks, peak=each.peak,
                                     rank=each.rank, date=each.date, song_id=song_id,
                                     ))

try:
    api_session.commit()
except Exception as e:
    print(str(e))
    api_session.rollback()

print('billboard success')



singer_song = session.query(Songtosinger).all()
songs = api_session.query(ApiSong).all()


for each in songs:
    singer_song = session.query(Songtosinger).filter_by(songId=each.id).all()
    for singer in singer_song:
        ss = session.query(Singer).filter_by(url=singer.singerName).first()
        s = api_session.query(ApiSinger).filter_by(name=ss.name, area=ss.area, type=ss.type, born=ss.born).first()
        each.singers.append(s)
        api_session.add(each)
api_session.commit()