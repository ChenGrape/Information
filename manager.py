
from flask_migrate import  Migrate, MigrateCommand
from flask_script import Manager
from info import create_app,db

# 调用工厂方法
app = create_app("develop")

# 配置数据库迁移
manager = Manager(app)
Migrate(app, db)
manager.add_command("db", MigrateCommand)

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    # redis_store.set("name", "zhangsan")
    # name = redis_store.get("name")
    # print(name)
    return "hello word!"

if __name__ == '__main__':
    app.run()

