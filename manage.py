# encoding: utf-8

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from zlktqa import app
from exts import db
# 需導入model, 執行MigrateCommand時才能找到模型, init -> migrate -> upgrade
from models import User, Question, Answer

manager = Manager(app)

# 使用Migrate綁定app和db
migrate = Migrate(app, db)

# 增加遷移的命令到manager中
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()