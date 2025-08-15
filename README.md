# 异世界角色个性化分析与冒险故事生成器

本项目是一个基于Flask的Web应用，用户可以输入MBTI、九型人格等类型学标签，系统将调用 DeepSeek API 生成异世界角色的个性化分析和冒险故事。

## 功能
- 输入类型学标签（如MBTI、九型人格等）
- AI生成角色分析与冒险故事
- 简单网页界面

## 快速开始
1. 安装依赖：
   推荐使用 requirements.txt 一键安装：
   ```bash
   pip install -r requirements.txt
   ```
   或手动安装：
   ```bash
   pip install flask openai
   ```
2. 设置 DeepSeek API 密钥：
   在项目根目录下创建 `.env` 文件，内容如下：
   ```env
   DEEPSEEK_API_KEY=你的API密钥
   ```
3. 运行项目：
   ```bash
   python app.py
   ```
4. 打开浏览器访问 http://127.0.0.1:5000


## 文件结构
- app.py         —— Flask主程序
- templates/
   - index.html   —— 前端页面
   - result.html   —— 输出结果页面
- .env           —— DeepSeek 密钥（需自行创建）
- requirements.txt —— 依赖包列表
- .gitignore     —— 已包含常用忽略规则
- LICENSE        —— 已包含 MIT 开源协议

## 注意
- 需自行注册账号并获取API Key。
- 本项目仅供学习和交流使用。
