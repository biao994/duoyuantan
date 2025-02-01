import os
import datetime
from passlib.hash import pbkdf2_sha256
from flask import render_template, request, redirect, url_for, session, flash
from app.models import db, User
from . import auth_blueprint

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        if not username or not password:
            flash("用户名或密码不能为空")
            return redirect(url_for('auth.register'))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("用户名已被注册")
            return redirect(url_for('auth.register'))

        password_hash = pbkdf2_sha256.hash(password)
        new_user = User(username=username, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()

        flash("注册成功，请登录")
        return redirect(url_for('auth.login'))
    return render_template('register.html')  # 放在 templates/auth/register.html

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        user = User.query.filter_by(username=username).first()
        if user and pbkdf2_sha256.verify(password, user.password_hash):
            session['user_id'] = user.id
            flash("登录成功")
            return redirect(url_for('chat.index'))  # 登录成功后跳到聊天首页 or index
        else:
            flash("用户名或密码错误")
            return redirect(url_for('auth.login'))
    return render_template('login.html')  # 放在 templates/auth/login.html

@auth_blueprint.route('/logout')
def logout():
    session.clear()
    flash("已退出登录")
    return redirect(url_for('auth.login'))
