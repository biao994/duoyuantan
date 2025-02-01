import os
import datetime
from flask import render_template, request, redirect, url_for, session, flash
from app.models  import db, User, UserAPIKey
from . import config_blueprint

@config_blueprint.route('/api_config')
def api_config():
    if 'user_id' not in session:
        flash("请先登录")
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    user = User.query.get(user_id)
    if not user:
        flash("用户不存在，请重新登录")
        return redirect(url_for('auth.login'))

    user_keys = {key.provider: key.api_key for key in user.api_keys}
    return render_template('api_config.html', user=user, user_keys=user_keys)

@config_blueprint.route('/set_api_key', methods=['POST'])
def set_api_key():
    if 'user_id' not in session:
        flash("请先登录")
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    user = User.query.get(user_id)
    if not user:
        flash("用户不存在，请重新登录")
        return redirect(url_for('auth.login'))

    provider = request.form.get('provider', '').strip()
    new_key = request.form.get('api_key', '').strip()
    if not provider or not new_key:
        flash("请填写提供商和 Key")
        return redirect(url_for('config_bp.api_config'))

    record = UserAPIKey.query.filter_by(user_id=user.id, provider=provider).first()
    if record:
        record.api_key = new_key
    else:
        record = UserAPIKey(user_id=user.id, provider=provider, api_key=new_key)
        db.session.add(record)
    db.session.commit()

    flash(f"已更新 {provider} 的 API Key")
    return redirect(url_for('config_bp.api_config'))
