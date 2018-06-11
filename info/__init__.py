from config import config_dict
import redis
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_wtf.csrf import CSRFProtect

# 创建对象db
db = SQLAlchemy()

# 工厂方法，根据不同的参数，创建不同的环境下的app对象
def create_app(config_name):

    app = Flask(__name__)

    # 根据传入的config_name获取到对应的配置类
    config = config_dict[config_name]
    # 加载配置类的中配置信息
    app.config.from_object(config)

    #  初始化db中的app
    db.init_app(app)

    # 创建redis
    redis_store = redis.StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT,decode_responses=True)

    # 创建session，添加到app中
    Session(app)

    # 设置应用程序csrf保护
    CSRFProtect(app)