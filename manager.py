import logging

from flask import current_app

from flask_migrate import  Migrate, MigrateCommand
from flask_script import Manager
from info import create_app,db,models

# 调用工厂方法
app = create_app("develop")

# 配置数据库迁移
manager = Manager(app)
Migrate(app,db)
manager.add_command("db", MigrateCommand)


if __name__ == '__main__':

    print(app.url_map)
    manager.run()
