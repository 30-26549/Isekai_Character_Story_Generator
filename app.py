
from flask import Flask, render_template, request, redirect, url_for, session
import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # 用于session

# DeepSeek API Key 和 Base URL

# 兼容 DeepSeek 和 OpenAI 的环境变量
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY") or os.getenv("OPENAI_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")

# 调试输出，确认环境变量读取
print(f"[DEBUG] DEEPSEEK_API_KEY: {DEEPSEEK_API_KEY}")
print(f"[DEBUG] DEEPSEEK_BASE_URL: {DEEPSEEK_BASE_URL}")

client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)

def generate_story_and_analysis(tags):
    type_info = '''
【MBTI（迈尔斯-布里格斯类型指标）】
将人格分为16种类型，由四个维度组合而成：
1. 精力来源：外向（E）- 内向（I）
2. 信息获取：实感（S）- 直觉（N）
3. 决策方式：思考（T）- 情感（F）
4. 生活态度：判断（J）- 知觉（P）
如INTP（内向、直觉、思考、知觉），每种类型有独特的思维、行为和人际风格。

【九型人格】
分为九种基本类型：
1号 改革者（理想主义、追求完美）
2号 助人者（关怀、付出）
3号 成就者（进取、目标导向）
4号 自我者（敏感、独特）
5号 调查者（理性、好奇）
6号 忠诚者（安全、责任）
7号 活跃者（乐观、冒险）
8号 领袖者（果断、掌控）
9号 和平者（温和、包容）
每型有核心动机、恐惧、成长方向。

【气质类型】
古典理论分为：
多血质（外向、乐观、易亲近）、
胆汁质（冲动、热情、易怒）、
粘液质（冷静、稳定、被动）、
抑郁质（敏感、内省、易忧郁）。
气质影响情绪反应、社交风格和压力应对。

【霍格沃茨分院】
格兰芬多：勇气、冒险、正义。
赫奇帕奇：忠诚、勤奋、包容。
拉文克劳：智慧、好学、理性。
斯莱特林：野心、机智、目标明确。
每个学院有独特的价值观和行为准则。

【DND阵营】
阵营系统为角色设定道德与伦理坐标：
善恶轴：善良（助人）、中立、邪恶（自利）。
秩序轴：守序（守规则）、中立、混乱（重自由）。
九种组合：守序善良、守序中立、守序邪恶、中立善良、绝对中立、中立邪恶、混乱善良、混乱中立、混乱邪恶。
阵营影响角色的行为准则、世界观和冒险选择。
'''
    prompt = f"""
你是一位精通心理学、类型学和世界观构建的故事设计师。
你的任务是：
1. 接收用户输入的类型学标签（包括但不限于MBTI、九型人格、气质、霍格沃茨分院、DND阵营等）。
2. 参考以下权威简介理解各类型学标签：
{type_info}
3. 基于这些标签生成清晰、条理化的角色性格分析（包括优点、缺点、动机、潜在冲突）。避免使用笼统的形容词，尽量用具体行为和细节刻画。
4. 根据角色分析，构建一个异世界冒险故事的开篇情节，要求故事有明确的世界观设定、冲突背景、配角设定，并融入角色性格特点。要有强烈的代入感和视觉冲击，世界观独特且充满未知感。
5. 语言简洁、生动，逻辑连贯，避免出现现代世界元素 unless 用户指定。
6. 额外要求：根据角色性格，生成一个最适合他的异世界世界观设定（如“机械魔法融合的废墟都市”或“漂浮在云海上的群岛王国”），并给出适合该性格的世界难度与任务类型。
7. 输出文本不要直接提到用户所输入的类型，避免出现类似“作为一名INTP”之类的句子。
8. 故事开篇必须包含：世界观背景、主角的第一场关键事件、潜在敌对势力或威胁、至少一个有记忆点的配角。（不用在输出文本中特地标明）
9. 风格应更接近轻小说或高质量奇幻小说的开篇，语言生动，细节具体，避免平淡描述。
用户输入如下：
{tags}
请按以下 JSON 格式输出：
{{
    "世界观": "...",  // 适合该角色的世界观设定
    "角色分析": {{
        "性格概述": "...",
        "优点": [...],
        "缺点": [...],
        "核心动机": "...",
        "潜在冲突": "..."
    }},
    "世界难度": "...",  // 如“高”、“中”、“低”
    "任务类型": "...",  // 如“探索”、“解谜”、“生存”、“外交”等
    "冒险故事": "..."
}}
"""
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        mbti = request.form.get('mbti', '').strip()
        enneagram = request.form.get('enneagram', '').strip()
        temperament = request.form.get('temperament', '').strip()
        hogwarts = request.form.get('hogwarts', '').strip()
        dnd = request.form.get('dnd', '').strip()
        extra = request.form.get('extra', '').strip()
        tags = f"MBTI: {mbti}\n九型人格: {enneagram}\n气质: {temperament}\n霍格沃茨分院: {hogwarts}\nDND阵营: {dnd}\n额外设定: {extra}"
        session['result'] = None
        if any([mbti, enneagram, temperament, hogwarts, dnd, extra]):
            try:
                session['result'] = generate_story_and_analysis(tags)
            except Exception as e:
                session['result'] = f"生成失败: {e}"
        return redirect(url_for('result_page'))
    return render_template('index.html')



@app.route('/result')
def result_page():
    result = session.get('result', None)
    parsed = None
    if result:
        try:
            # 只提取JSON部分，防止AI前后有多余内容
            json_start = result.find('{')
            json_end = result.rfind('}')
            if json_start != -1 and json_end != -1:
                json_str = result[json_start:json_end+1]
                parsed = json.loads(json_str)
        except Exception:
            parsed = None
    return render_template('result.html', result=result, parsed=parsed)

if __name__ == '__main__':
    app.run(debug=True)
