import os
import datetime
import openai
import requests
from flask import render_template, request, redirect, url_for, session, flash
from app.models  import db, Chat, Message
from . import chat_blueprint
from app.models import User, UserAPIKey



def get_api_key(user_id, provider):
    record = UserAPIKey.query.filter_by(user_id=user_id, provider=provider).first()
    if record:
        return record.api_key
    return None


def call_openai_api(messages, api_key, model_version="gpt-3.5-turbo"):
    os.environ['HTTPS_PROXY'] = "http://127.0.0.1:7890"  # 代理示例
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key) 
        resp = client.chat.completions.create(
            model=model_version,
            messages=messages
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"[OpenAI 调用出错] {e}"



def call_qwen_api(messages, api_key, model_version="qwen-plus"):
    try:
        from openai import OpenAI
        client = OpenAI(
            api_key=api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        completion = client.chat.completions.create(
            model=model_version,
            messages=messages
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"[通义千问调用出错] {str(e)}"
    
@chat_blueprint.route('/')
def index():
    if 'user_id' not in session:
        flash("请先登录")
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    # 查询当前用户
    user = User.query.get(user_id)
    if not user:
        flash("用户不存在，请重新登录")
        return redirect(url_for('auth.login'))

    chats = Chat.query.filter_by(user_id=user_id).order_by(Chat.created_at.desc()).all()

    return render_template('index.html', user=user, chats=chats)



@chat_blueprint.route('/create_chat', methods=['POST'])
def create_chat():
    if 'user_id' not in session:
        flash("请先登录")
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    new_chat = Chat(user_id=user_id, title="新会话")
    db.session.add(new_chat)
    db.session.commit()
    return redirect(url_for('chat.chat_view', chat_id=new_chat.id))

@chat_blueprint.route('/chat/<int:chat_id>', methods=['GET', 'POST'])
def chat_view(chat_id):
    """
    显示会话，处理用户发送消息
    """
    if 'user_id' not in session:
        flash("请先登录")
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    chat_obj = Chat.query.get_or_404(chat_id)
    if chat_obj.user_id != user_id:
        flash("无权访问他人的会话")
        return redirect(url_for('chat.index'))

    messages = Message.query.filter_by(chat_id=chat_obj.id).order_by(Message.created_at).all()

    if request.method == 'POST':
        user_input = request.form.get('user_input', '').strip()
        provider = request.form.get('model_provider', '').strip()
        model_version = request.form.get('model_version', '').strip()

        if not user_input:
            flash("请输入内容")
            return redirect(url_for('chat.chat_view', chat_id=chat_id))

        if not provider or not model_version:
            flash("请选择模型提供商和模型版本")
            return redirect(url_for('chat.chat_view', chat_id=chat_id))

        user_msg = Message(chat_id=chat_obj.id, role='user', content=user_input)
        db.session.add(user_msg)
        db.session.commit()

        chat_obj.model_provider = provider
        chat_obj.model_version = model_version
        db.session.commit()

        api_key = get_api_key(user_id, provider)
        if not api_key:
            assistant_reply = f"{provider.capitalize()} ({model_version}): 尚未配置[{provider}]的API Key，无法调用。"
        else:
            # 组装对话
            conversation = []
            all_msgs = Message.query.filter_by(chat_id=chat_obj.id).order_by(Message.created_at).all()
            for m in all_msgs:
                conversation.append({"role": m.role, "content": m.content})

            if provider == 'openai':
                assistant_reply = call_openai_api(conversation, api_key, model_version)
            elif provider == 'qwen':
                assistant_reply = call_qwen_api(conversation, api_key, model_version)
            else:
                assistant_reply = f"不支持的模型: {provider}"

        ai_msg = Message(chat_id=chat_obj.id, role='assistant', content=assistant_reply)
        db.session.add(ai_msg)
        db.session.commit()

        return redirect(url_for('chat.chat_view', chat_id=chat_id))

    # GET
    current_provider = chat_obj.model_provider
    current_version = chat_obj.model_version
    return render_template(
        'chat.html',
        chat=chat_obj,
        messages=messages,
        current_provider=current_provider,
        current_version=current_version
    )
