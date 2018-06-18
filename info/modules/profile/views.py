from flask import current_app
from flask import redirect, jsonify
from flask import request
from flask import session

from info import db
from info.utils.common import user_login_data
from info.utils.response_code import RET
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
# 请求路径: /user/base_info
# 请求方式:GET,POST
# 请求参数:POST请求有参数,nick_name,signature,gender
# 返回值:errno,errmsg
@profile_blu.route('/base_info', methods=['GET','POST'])
@user_login_data
def baes_info():
    """
    用户基本信息
    1. 获取用户登录信息
    2. 获取到传入参数
    3. 更新并保存数据
    4. 返回结果
    :return:
    """
    # 1. 获取用户登录信息
    if request.method == 'GET':
        return render_template("news/user_base_info.html",data={"user_info":g.user.to_dict()})
    # 获取参数
    data_dict = request.json
    nick_name = data_dict.get("nick_name")
    signature = data_dict.get("signature")
    gender = data_dict.get("gender")
    # 判断用户昵称是否为空
    if not nick_name:
        return jsonify(errno=RET.PARAMERR, errmsg="用户昵称不能为空")

    # 3. 更新并保存数据

    try:
        g.user.nick_name = nick_name
        g.user.gender = gender
        g.user.signature = signature
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="保存数据失败")

    # 将 session 中保存的数据进行实时更新
    session["nick_name"] = nick_name
    # 4. 返回结果
    return jsonify(errno=RET.OK,errmsg="更新成功")


# 个人中心页面
@profile_blu.route('/user_info')
@user_login_data
def get_user_info():

    # 判断用户是否登陆
    if not g.user:
        return redirect('/')

    data = {
        "user_info":g.user.to_dict()
    }

    return render_template("news/user.html", data=data)