import redis
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

class Config(object):

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost:3306/information"
    SQLALCHEMY_TRACK_MODIFICATIONS = Flask

    #创建redis
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

app.config.from_object(Config)

#创建数据库连接
db = SQLAlchemy(app)

# 创建redis
redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT,decode_responses=True)

@app.route("/")
def hello_world():
    redis_store.set("name", "zhangsan")
    name = redis_store.get("name")
    print(name)
    return "hello word!"

if __name__ == '__main__':
    app.run(debug=True)

