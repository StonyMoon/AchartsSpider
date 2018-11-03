# 把爬虫爬取到数据库中

import pyquery
import requests

from db.models import *


def get(url, try_time=2):
    # 设置请求头
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
    }
    try:
        re = requests.get(url, headers=headers)
    except Exception:
        if try_time > 0:
            return get(url, try_time - 1)
        print('网页:', url, '抓取失败')
        return None
    else:
        return re.text


# 通过歌曲 id 来获取歌曲信息
def get_song_info(song_id, song_name):
    print('爬取歌曲信息', song_name)
    if session.query(Song).filter_by(id=song_id).first():
        return
    url = 'https://acharts.co/song/' + song_id
    soup = pyquery.PyQuery(get(url))
    singers_name = [x.text() for x in soup('.ArtistSpace').items()]
    singers_url = [x.attr('href').split('/')[2] for x in soup('.ArtistSpace a').items()]
    for each in zip(singers_name, singers_url):
        if session.query(Songtosinger).filter_by(songId=song_id, singerName=each[0]).first():
            return
        session.add(Songtosinger(song_id, each[1]))
        get_singer(each[0], each[1])
    session.add(Song(song_id, song_name))
    session.commit()


# 参数年份 月份
def get_board(year, week):
    print('开始爬取', year, week)
    url = 'https://acharts.co/us_singles_top_100/%s/%s' % (year, week)
    re = get(url)
    soup = pyquery.PyQuery(re)
    next_page = soup('#st-container > div > div > header > div.title > h2:nth-child(3) > a').attr('href') \
        .split('/')
    next_year = int(next_page[2])
    next_week = int(next_page[3])
    date = soup('[itemprop=datePublished]').attr('datetime')
    soup = soup('#ChartTable tbody tr')
    for each in soup.items():
        rank = int(each('[itemprop=position]').text())
        [previous, peak, weeks] = each('.cStats').text().split(' ')
        if previous == 'new':
            previous = None
        elif previous == 're-entry':
            previous = 101
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

        get_song_info(song_id, song_name)
    print(next_year, next_week)
    get_board(next_year, next_week)


def get_singer(name, singer_url):
    # 判断歌手是否已经被爬过
    if session.query(Singer).filter_by(url=singer_url).first():
        return
    url = 'https://acharts.co/artist/' + singer_url
    re = get(url)
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
        elif 'Born' in each and each.count('-') == 2:
            born = each.replace('Founded: ', '').replace('Born: ', '')
    print('歌手', name)
    session.add(Singer(type=type, url=singer_url, name=name, image=image_url, info=des, area=area, born=born))
    session.commit()


# def schedule():
#     for year in range(15):
#         for i in range(0, 54):
#             print(2018 - year, 54 - i)
#             get_board(2018 - year, 54 - i)


# schedule()
get_board(2018, 44)
