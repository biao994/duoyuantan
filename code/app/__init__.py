from flask import Flask
from .models import db
from .auth import auth_blueprint
from .config_bp import config_blueprint
from .chat import chat_blueprint

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-key-123'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myapp.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 初始化数据库
    db.init_app(app)

    # 如果你想在启动时自动创建表
    with app.app_context():
        db.create_all()

    # 注册各功能模块蓝图
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(config_blueprint)
    app.register_blueprint(chat_blueprint)

    return app
