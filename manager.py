import redis
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_wtf.csrf import CSRFProtect
from flask_migrate import  Migrate, MigrateCommand
from flask_script import Manager
from config import Config,ProductConfig
app = Flask(__name__)


app.config.from_object(ProductConfig)

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

