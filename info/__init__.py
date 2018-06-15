import logging
from logging.handlers import RotatingFileHandler
from config import config_dict
import redis
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_wtf.csrf import CSRFProtect, generate_csrf

# 创建对象db
from info.utils.common import do_index_filter

db = SQLAlchemy()

# 定义redis为全局变量
redis_store = None

# 工厂方法，根据不同的参数，创建不同的环境下的app对象
def create_app(config_name):

    app = Flask(__name__)

    # 根据传入的config_name获取到对应的配置类
    config = config_dict[config_name]

    # 日志方法的调用
    log_file(config.LEVEL)

    # 加载配置类的中配置信息
    app.config.from_object(config)

    #  初始化db中的app
    db.init_app(app)

    # 创建redis
    global redis_store
    redis_store = redis.StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT,decode_responses=True)

    # 创建session，添加到app中
    Session(app)

    # 设置应用程序csrf保护
    #开了了csrf保护之后,会对['POST', 'PUT', 'PATCH', 'DELETE']类型的请求方法做校验
    #获取cookie中的csrf_token, 获取headers请求头里面的csrf_token做校验,只做校验
    #开发者: 需要手动设置,cookie, headers中的csrf_token
    CSRFProtect(app)

    # 设置请求钩子after_request,每次请求完成之后都会走该钩子修饰的方法
    @app.after_request
    def after_request(resp):
        csrf_token = generate_csrf()
        resp.set_cookie("csrf_token", csrf_token)
        return resp
    # 注册首页蓝图对象
    # 解决循环导包，使用内导包方法
    from info.modules.index import index_blu
    app.register_blueprint(index_blu)

    # 注册图片验证码蓝图
    from info.modules.passport import passport_blu
    app.register_blueprint(passport_blu)

    # 将过滤器添加到模板过滤器中
    app.add_template_filter(do_index_filter, "index_filter")

    return app

# 日志文件，作用：用来记录程序的运行过程
def log_file(level):
    # 设置日志的记录等级 ，设置日志等级：常见等级：DEBUG < INFO < WARING < ERROR < FATAL
    logging.basicConfig(level=level)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件编号
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)