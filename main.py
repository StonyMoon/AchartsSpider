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


# get_rank("107913","uk_singles_top_75")


def get_info(song_id):
    url = 'https://acharts.co/song/' + song_id
    soup = pyquery.PyQuery(req.get(url).text)
    authors = [x.text() for x in soup('.ArtistSpace').items()]
    for each in authors:
        session.add(Songtosinger())
        get_singer(each)


def get_board(year, week):
    url = 'https://acharts.co/us_singles_top_100/%s/%s' % (year, week)
    re = req.get(url).text
    soup = pyquery.PyQuery(re)
    date = soup('[itemprop=datePublished]').attr('datetime')
    soup = soup('#ChartTable tbody tr')

    for each in soup.items():
        rank = int(each('[itemprop=position]').text())
        [previous, peak, weeks] = each('.cStats').text().split(' ')
        b = Billboard(previous,weeks,peak,rank,date=date)
        song_name = each('[itemprop=name]').html()
        song_url = each('a').attr('href')
        song_id = song_url.split('/')[-1]
        session.add(Songonbillboard(songId=song_id, billboardDate=date, billboardRank=rank))
        session.add(b)
        session.add(Song(song_id, song_name))
        session.commit()
        get_info(song_id)


def get_singer(name):
    url = 'https://acharts.co/artist/' + name
    re = req.get(url).text
    soup = pyquery.PyQuery(re)
    image_url = soup('.ArtworkSlide').attr('content')
    des = soup('[itemprop=description]').text()
    info = soup('#Biography')
    html = info.html()
    html = html.replace('<br/>', '').replace('<b>', '').replace('</b>', '') \
        .split('Type: ')[1].split('Tags: ')[0].replace('  ', '')
    info_list = [x for x in html.split('\n') if x != '']
    type = info_list[0].replace('Person ', '').replace('(', '').replace(')', '')
    area = info_list[1].replace('Area: ', '')
    born = info_list[2].replace('Founded: ', '').replace('Born: ', '')
    session.add(Singer())

    session.commit()

    print(type, area, born, image_url, des)


get_board(2018,5)