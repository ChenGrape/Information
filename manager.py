from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

class Config(object):

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost:3306/information"
    SQLALCHEMY_TRACK_MODIFICATIONS = Flask

app.config.from_object(Config)

db = SQLAlchemy(app)

@app.route("/")
def hello_world():
    return "hello word!"

if __name__ == '__main__':
    print(db)
    app.run(debug=True)

