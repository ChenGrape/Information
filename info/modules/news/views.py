from flask import abort
from flask import current_app
from flask import g

from info import constants
from info.models import News
from info.utils.common import user_login_data
from . import news_blu
from flask import render_template

@news_blu.route("/<int:news_id>")
@user_login_data
def new_detail(news_id):

    # 查询数据库，返回点击量前10的新闻数据
    try:
        click_news =News.query.order_by(News.clicks.desc()).limit(constants.CLICK_RANK_MAX_NEWS).all();
    except Exception as e:
        current_app.logger.error(e)

    click_news_list = []
    for news in click_news:
        click_news_list.append(news.to_dict())

    # 获取新闻对象
    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)

    # 如果没有该条新闻直接找不到页面
    if not news:
        abort(404)

    data = {
        # 如果user为空返回None,如果有内容返回左边
        "user_info": g.user.to_dict() if g.user else None,
        "news_info": click_news_list,
        "news":news.to_dict()

    }
    return render_template("news/detail.html", data = data)