import redis
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_wtf.csrf import CSRFProtect
from flask_migrate import  Migrate, MigrateCommand
from flask_script import Manager

app = Flask(__name__)

class Config(object):

    DEBUG = True
    SECRET_KEY = "fdhgsbjfsa"

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost:3306/information"
    SQLALCHEMY_TRACK_MODIFICATIONS = Flask

    #创建redis
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    # 配置session
    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.StrictRedis(REDIS_HOST,REDIS_PORT) # 存储在redis中
    SESSION_USE_SIGNER = True # 设置签名
    PERMANENT_SESSION_LIFETIME = 3600 * 24 * 2  # 设置session有效时间

app.config.from_object(Config)

#创建数据库连接
db = SQLAlchemy(app)

# 创建redis
redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT,decode_responses=True)

# 创建session，添加到app中
Session(app)

# 设置应用程序csrf保护
CSRFProtect(app)

# 配置数据库迁移
manager = Manager(app)
Migrate(app, db)
manager.add_command("db", MigrateCommand)

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    redis_store.set("name", "zhangsan")
    name = redis_store.get("name")
    print(name)
    return "hello word!"

if __name__ == '__main__':
    app.run()

