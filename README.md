多源谈（Duoyuantan）

多源谈 是一个基于 Flask 开发的多模型 AI 聊天系统，支持 OpenAI GPT、通义千问 Qwen 等多个 AI 提供商，用户可以在不同模型之间切换，并进行对话记录管理。

✨ 项目特色

📌 多 AI 模型支持：目前支持 OpenAI GPT、通义千问 Qwen，未来可扩展其他大模型。

🏗 模块化架构：使用 Flask 蓝图（Blueprint）进行模块化开发，结构清晰，可扩展性强。

📄 对话记录管理：可创建多个聊天会话，支持消息存储、历史查询。

🔐 用户 API Key 绑定：不同用户可配置自己的 API Key，并选择使用不同模型。

🌐 Web 端 UI：提供简单易用的前端界面，用户可直接通过浏览器访问。


📥 安装与运行

1️⃣ 环境准备

确保你的环境安装了 Python 3.8+，建议使用 virtualenv 创建虚拟环境：

创建虚拟环境（可选）

python -m venv venv

激活虚拟环境

source venv/bin/activate # Mac/Linux

venv\Scripts\activate # Windows

安装依赖

pip install -r requirements.txt 

2️⃣ 运行项目

cd code

python run.py

启动后，在浏览器中访问 http://127.0.0.1:5003。

功能截图

登录界面

![image](https://github.com/user-attachments/assets/ee45bfb2-efbb-4f1c-a80e-b28cc3d4a0ec)


注册界面

![image](https://github.com/user-attachments/assets/c10bcba1-33f4-4619-854d-27f8035a996b)


主页界面

![image](https://github.com/user-attachments/assets/3af63f54-f1be-420f-955a-f8aec4ce7244)


api设置界面

![image](https://github.com/user-attachments/assets/ecfcea17-5c58-4c9e-8866-1df1393f8d8e)


聊天界面
![image](https://github.com/user-attachments/assets/2d785f4d-d05f-4430-a72f-5e4c8819bc38)


