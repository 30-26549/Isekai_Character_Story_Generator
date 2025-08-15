# 异世界角色个性化分析与冒险故事生成器

本项目是一个基于Flask的Web应用，用户可以输入MBTI、九型人格等类型学标签，系统将调用API生成异世界角色的个性化分析和冒险故事。

## 功能
- 输入类型学标签（如MBTI、九型人格等）
- AI生成角色分析与冒险故事
- 简单网页界面

## 快速开始
1. 安装依赖：
   ```bash
   pip install flask openai
   ```
2. 设置OpenAI API密钥：
   在项目根目录下创建`.env`文件，内容如下：
   ```env
   OPENAI_API_KEY=你的API密钥
   ```
3. 运行项目：
   ```bash
   python app.py
   ```
4. 打开浏览器访问 http://127.0.0.1:5000

## 文件结构

- `app.py`         ：Flask 主程序
- `templates/`     
  - `index.html`   ：前端页面
- `.env`           ：OpenAI 密钥（需自行创建）


## 注意
- 需自行获取API Key。
- 本项目仅供学习和交流使用。



