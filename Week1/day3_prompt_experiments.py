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