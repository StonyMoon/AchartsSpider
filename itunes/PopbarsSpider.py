# 拿到 资料保存到 redis 中
import requests
from pyquery import PyQuery as pq
import json
import redis

pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
conn = redis.Redis(connection_pool=pool)


class Song(json.JSONEncoder):
    title = ''
    position = 0
    now_point = 0
    now_color = ''
    discounted = 0

    def __init__(self, title, position, now_point, now_color, discounted):
        super().__init__()
        self.title = title
        self.position = position
        self.now_point = now_point
        self.now_color = now_color
        self.discounted = discounted

    def json(self):
        return {"title": self.title, "position": self.position, "now_point": self.now_point,
                "now_color": self.now_color, "discounted": self.discounted}


def get_color(item):
    html = item('td').eq(1).__str__()
    html = html.split("\"")[1][0:2]
    return html


def get_title(item):
    return item('td').eq(1).text()


def get_now_point(item):
    return float(item('b').text())


def get_discounted(item):
    if item('td').eq(2).text() == '$':
        return 1
    else:
        return 0


def initSong(item, po):
    title = get_title(item)
    point = get_now_point(item)
    color = get_color(item)
    discounted = get_discounted(item)
    song = Song(title, po, point, color, discounted)
    return song


def open_url(url):
    r = requests.get(url)
    return pq(r.text)


def get_song(url):
    song_list = []
    soup = open_url(url)
    song_items = soup('tbody')('tr')
    i = 1
    for each in song_items.items():
        song_list.append(initSong(each, i))
        i += 1
    return song_list


def get_json(url):
    son_json = []
    sl = get_song(url)
    for each in sl:
        j = each.json()
        son_json.append(json.dumps(j))
    return son_json


def get_response():
    response = ''
    song_json = get_json('http://kworb.net/pop/')
    flag = False
    for each in song_json:
        if (flag):
            response = response + ',' + each
        else:
            response += each
            flag = True

    response = u'{\"all_song\":[' + response + '],\"time\":}'
    return response


def save():
    itunes = get_response()
    conn.set('itunes', itunes, ex=999999)


def get_itunes():
    print(conn.get('itunes'))


save()
