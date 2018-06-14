from flask import session

from info import redis_store
from info.models import User
from . import index_blu
from flask import render_template,current_app


@index_blu.route("/", methods=['GET', 'POST'])
def hello_world():
    # 获取用户编号
    user_id = session.get("user_id")
    # 查询用户的对象
    user = None
    if user_id:
        try:
            user = User.query.get(user_id)
        except Exception as e:
            current_app.logger.error(e)

    # 返回数据到模板页面
    data = {
        # 如果user为空返回None,如果有内容返回左边
        "user_info":user.to_dict() if user else None
    }

    return render_template("news/index.html", data = data)

# 设置favicon.ico小图标
# 使用current_app.send_static_file(),自动加载static文件下的内容
@index_blu.route('/favicon.ico')
def web_logo():
    return current_app.send_static_file("news/favicon.ico")