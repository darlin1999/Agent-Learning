import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # 从 .env 文件读取 DEEPSEEK_API_KEY

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

def chat(system_prompt: str, user_prompt: str, temperature: float = 0.7) -> str:
    """发送一次对话请求，返回模型回复文本。"""
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt},
        ],
        temperature=temperature,
        max_tokens=512,
    )
    return response.choices[0].message.content


def experiment(title: str, system: str, user: str, temperature: float = 0.7):
    """打印实验标题和结果，方便对比。"""
    print(f"\n{'='*60}")
    print(f"实验：{title}")
    print(f"{'='*60}")
    print(f"[System] {system}")
    print(f"[User]   {user}")
    print(f"[输出]")
    print(chat(system, user, temperature))

SYSTEM_BASE = "你是一个严谨的逻辑推理助手。"

PROBLEM = (
    "一家工厂有三条流水线 A、B、C。"
    "A 每小时生产 120 件，B 每小时生产 80 件，C 每小时生产 60 件。"
    "工厂运行 8 小时后，因维修 A 停工 2 小时。"
    "请问 8 小时内工厂共生产多少件产品？"
)

def chat_with_messages(messages: list[dict]) -> str:
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        temperature=0.0,
        max_tokens=512,
    )
    return response.choices[0].message.content

cot_messages = [
    {"role": "system", "content": SYSTEM_BASE},
    # ── Few-shot 示例：带推理步骤 ──
    {
        "role": "user",
        "content": (
            "车间有 2 台机器，甲每小时产出 50 件，乙每小时产出 30 件，"
            "工作 5 小时，其中乙停机 1 小时，共生产多少件？"
        ),
    },
    {
        "role": "assistant",
        "content": (
            "第一步：甲全程工作 5 小时，产出 = 50 × 5 = 250 件\n"
            "第二步：乙实际工作 5 - 1 = 4 小时，产出 = 30 × 4 = 120 件\n"
            "第三步：合计 = 250 + 120 = 370 件\n"
            "最终答案：370 件"
        ),
    },
    # ── 真实问题 ──
    {"role": "user", "content": PROBLEM},
]

print(f"\n{'='*60}")
print("实验：3c - Few-shot CoT（带推理示例）")
print(f"{'='*60}")
print("[输出]")
print(chat_with_messages(cot_messages))