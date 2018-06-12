from info import redis_store
from . import index_blu
from flask import render_template,current_app


@index_blu.route("/", methods=['GET', 'POST'])
def hello_world():

    return render_template("news/index.html")

# 设置favicon.ico小图标
# 使用current_app.send_static_file(),自动加载static文件下的内容
@index_blu.route('/favicon.ico')
def web_logo():
    return current_app.send_static_file("news/favicon.ico")