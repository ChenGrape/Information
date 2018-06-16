from flask import g
from flask import request
from flask import session, jsonify

from info import constants
from info import redis_store
from info.models import User, News, Category
from info.utils.common import user_login_data
from info.utils.response_code import RET
from . import index_blu
from flask import render_template,current_app


#首页新闻列表
# 请求路径: /newslist
# 请求方式: GET
# 请求参数: cid,page,per_page
# 返回值: data数据
@index_blu.route('/newslist')
def news_list():
    """
    思路分析
    1.获取参数
    2.校验参数,转换参数类型
    3.根据条件查询数据
    4.将查询到的分类对象数据,转成字典
    5.返回响应请求
    :return:
    """
    # 1.获取参数
    cid =  request.args.get("cid")
    page =  request.args.get("page",1)
    per_page =  request.args.get("per_page",10)

    # 2.校验参数,转换参数类型
    try:
        page = int(page)
        per_page = int(per_page)
    except Exception as e:
        current_app.logger.error(e)
        page = 1
        per_page = 10

    # 3.根据条件查询数据
    try:
        #判断分类编号是否不等于 1
        filters = []
        if cid != "1":
            filters.append(News.category_id == cid)

        #查询新闻数据根据条件
        paginate = News.query.filter(*filters).order_by(News.create_time.desc()).paginate(page,per_page,False)

        #获取分页中的内容,总页数,当前页,当前页的所有对象
        totalPage = paginate.pages
        currentPage = paginate.page
        items = paginate.items

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="数据查询失败")

    # 4.将查询到的分类对象数据,转成字典
    newsList = []
    for news in items:
        newsList.append(news.to_dict())

    # 5.返回响应请求
    return jsonify(errno=RET.OK,errmsg="获取数据成功",cid=cid,currentPage=currentPage,totalPage=totalPage,newsList=newsList)

@index_blu.route("/", methods=['GET', 'POST'])
@user_login_data
def hello_world():
    # # 获取用户编号
    # user_id = session.get("user_id")
    # # 查询用户的对象
    # user = None
    # if user_id:
    #     try:
    #         user = User.query.get(user_id)
    #     except Exception as e:
    #         current_app.logger.error(e)

    # 查询数据库，返回点击量前10的新闻数据
    try:
        click_news =News.query.order_by(News.clicks.desc()).limit(constants.CLICK_RANK_MAX_NEWS).all();
    except Exception as e:
        current_app.logger.error(e)

    click_news_list = []
    for news in click_news:
        click_news_list.append(news.to_dict())


    # 导航条
    try:
        category = Category.query.all()
    except Exception as e:
        current_app.logger.error(e)
    category_list = []
    for categorys in category:
        category_list.append(categorys.to_dict())

    # 返回数据到模板页面
    data = {
        # 如果user为空返回None,如果有内容返回左边
        "user_info":g.user.to_dict() if g.user else None,
        "news_info":click_news_list,
        "category_info": category_list
    }


    return render_template("news/index.html", data = data)

# 设置favicon.ico小图标
# 使用current_app.send_static_file(),自动加载static文件下的内容
@index_blu.route('/favicon.ico')
def web_logo():
    return current_app.send_static_file("news/favicon.ico")