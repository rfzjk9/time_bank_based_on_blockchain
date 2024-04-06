from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import *
import templates.config2


app = Flask(__name__)
app.config.from_object(templates.config2)
# 初始化一个SQLAlchemy对象（该步要在导入config后执行）
# 实例化的同时将与数据库相关的配置读入
db = SQLAlchemy(app)
# 初始化app对象中与数据库相关的配置的设置，防止数据库连接泄露
db.init_app(app)


class Users:
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column()
