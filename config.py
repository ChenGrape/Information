import logging
import redis


class Config(object):

    DEBUG = True
    SECRET_KEY = "fdhgsbjfsa"

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost:3306/information"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #创建redis
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    # 配置session
    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.StrictRedis(REDIS_HOST,REDIS_PORT) # 存储在redis中
    SESSION_USE_SIGNER = True # 设置签名
    PERMANENT_SESSION_LIFETIME = 3600 * 24 * 2  # 设置session有效时间

    # 设置日志等级
    LEVEL = logging.DEBUG

# 开发模式
class DeveloperConfig(Config):
    pass
# 生产模式
class ProductConfig(Config):
    DEBUG = False
    LEVEL = logging.ERROR
    pass
# 测试模式
class TestingConfig(Config):
    pass

# 设置统一访问入口
config_dict ={
    "develop":DeveloperConfig,
    "product":ProductConfig,
    "testing":TestingConfig

}