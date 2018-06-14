from flask import Blueprint

# 创建蓝图对象，设置访问前缀，所有的访问该蓝图的请求都需要加上/passport
passport_blu = Blueprint("passport",__name__,url_prefix="/passport")

from . import views