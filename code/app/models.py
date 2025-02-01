import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """用户表"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    # ...
    chats = db.relationship('Chat', backref='user', lazy=True)
    api_keys = db.relationship('UserAPIKey', backref='user', lazy=True)

class UserAPIKey(db.Model):
    """用户的各模型 API Key 存储"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    provider = db.Column(db.String(50), nullable=False)
    api_key = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class Chat(db.Model):
    """对话表"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), default="未命名会话")
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    model_provider = db.Column(db.String(50), nullable=True)
    model_version = db.Column(db.String(50), nullable=True)

    messages = db.relationship('Message', backref='chat', lazy=True)

class Message(db.Model):
    """每条消息"""
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'user' or 'assistant'
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
