from flask import Blueprint

# 创建蓝图对象，设置访问前缀
news_blu = Blueprint("news",__name__,url_prefix="/news")

from . import views