# 脚本管理，处理分为两步，第一步爬取需要的数据
# 第二步处理数据

# 自动导入数据过程：第一步，get 最新的榜单，如果没get到就关闭爬虫
# 如果 get 到了就更新数据库，然后删库重新导入
from db.api_models import *
from db.models import Chart, session as md_session
from data_handle.transfer import reimport
from spider.main import get_board, get_new_week


def delete_table():
    session.execute("delete from song_singer")
    session.query(Billboard).delete()
    session.query(Singer).delete()
    session.query(Song).delete()
    session.commit()


def get_next_week():
    year, week = get_new_week()
    chart = md_session.query(Chart).filter(Chart.week == week and Chart.year == year).first()
    print(week, year)
    print(chart)
    if chart is not None:
        print("爬过了")
        return
    try:
        get_board(year, week)
    except Exception as e:
        print("还莫有更新榜单")
        exit(0)
    delete_table()
    reimport()
    md_session.add(Chart(year, week))
    md_session.commit()


get_next_week()
