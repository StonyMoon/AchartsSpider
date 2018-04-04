import requests as req
import json
import pyquery
from Cache import session
from models import *

def get_rank(song_id, chart):
    url = 'https://acharts.co/callback/GraphData'
    data = {
        'titleid': song_id,
        "chart": chart,
        "initiator": ' automatic_first'
    }
    re = req.post(url, data).text
    re = json.loads(re)['data']['data']
    for e in re:
        print(int(e[2]))

def get_info(song_id):
    url = 'https://acharts.co/song/' + song_id
    soup = pyquery.PyQuery(req.get(url).text)
    singers_name = [x.text() for x in soup('.ArtistSpace').items()]
    singers_url = [x.attr('href').split('/')[2] for x in soup('.ArtistSpace a').items()]
    for each in zip(singers_name, singers_url):
        if session.query(Songtosinger).filter_by(songId=song_id, singerName=each[0]).first():
            return
        session.add(Songtosinger(song_id, each[1]))
        get_singer(each[0], each[1])


def get_board(year, week):
    url = 'https://acharts.co/us_singles_top_100/%s/%s' % (year, week)
    re = req.get(url).text
    soup = pyquery.PyQuery(re)
    date = soup('[itemprop=datePublished]').attr('datetime')
    soup = soup('#ChartTable tbody tr')

    for each in soup.items():
        rank = int(each('[itemprop=position]').text())
        [previous, peak, weeks] = each('.cStats').text().split(' ')
        if previous == 'new':
            previous = None
        if session.query(Billboard).filter_by(date=date, rank=rank).first() \
                is None:
            billboard_item = Billboard(previous, weeks, peak, rank, date=date)
            session.add(billboard_item)
            session.commit()

        song_name = each('[itemprop=name]').html()
        song_url = each('a').attr('href')
        song_id = song_url.split('/')[-1]
        if session.query(Songonbillboard).filter_by(songId=song_id, billboardDate=date, billboardRank=rank).first() \
                is None:
            session.add(Songonbillboard(songId=song_id, billboardDate=date, billboardRank=rank))
            session.commit()
        if session.query(Song).filter_by(id=song_id).first() is None:
            session.add(Song(song_id, song_name))
            session.commit()
        get_info(song_id)


def get_singer(name, singer_url):
    # 判断歌手是否已经被爬过
    if session.query(Singer).filter_by(url=singer_url).first():
        return
    url = 'https://acharts.co/artist/' + singer_url
    re = req.get(url).text
    soup = pyquery.PyQuery(re)
    image_url = soup('.ArtworkSlide').attr('content')
    des = soup('[itemprop=description]').text()
    info = soup('#Biography')
    html = info.html()
    try:
        html = html.replace('<br/>', '').replace('<b>', '').replace('</b>', '') \
            .split('Type: ')[1].split('Tags: ')[0].replace('  ', '')
    except:
        print(name)
        session.add(Singer(url=singer_url, name=name, image=image_url, info=None, area=None, born=None))
        session.commit()
        return

    info_list = [x for x in html.split('\n') if x != '']
    type = None
    area = None
    born = None
    for each in info_list:
        if 'Person' in each:
            type = each.replace('Person ', '').replace('(', '').replace(')', '')
        elif 'Area' in each:
            area = each.replace('Area: ', '')
        elif 'Born' in each:
            born = each.replace('Founded: ', '').replace('Born: ', '')

    if session.query(Singer).filter_by(name=name).first():
        return
    session.add(Singer(type=type, url=singer_url, name=name, image=image_url, info=des, area=area, born=born))
    session.commit()


get_board(2018,5)
#get_info('112140')
