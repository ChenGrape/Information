from info.utils.common import user_login_data
from . import profile_blu
from flask import render_template,g

# 新闻列表
@profile_blu.route('/news_list')
def news_list():
    return render_template("news/user_news_list.html")

# 新闻发布
@profile_blu.route('/news_release')
def news_release():
    return render_template("news/user_news_release.html")

# 我的收藏页面
@profile_blu.route('/collection')
def collection():
    return render_template("news/user_collection.html")

# 密码修改页面
@profile_blu.route('/pass_info')
def pass_info():
    return render_template("news/user_pass_info.html")

# 我的关注页面
@profile_blu.route('/user_follow')
def user_follow():
    return render_template("news/user_follow.html")

# 头像设置页面
@profile_blu.route('/pic_info')
def pic_info():

    return render_template("news/user_pic_info.html")

# 基本信息页面
@profile_blu.route('/base_info')
def baes_info():
    return render_template("news/user_base_info.html")

# 个人中心页面
@profile_blu.route('/user_info')
@user_login_data
def get_user_info():

    data = {
        "user_info":g.user.to_dict()
    }

    return render_template("news/user.html", data=data)