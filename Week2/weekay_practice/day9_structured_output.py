import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List


load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)


# ── 实战：技术文章信息提取 ────────────────────────────────
class TechArticleSummary(BaseModel):
    """技术文章摘要。"""
    title: str = Field(description="文章标题或主题")
    main_technologies: List[str] = Field(description="涉及的主要技术/框架")
    key_points: List[str] = Field(description="3-5个关键观点")
    difficulty: str = Field(description="难度级别：入门/中级/高级")
    recommended_audience: str = Field(description="推荐阅读人群")

def analyze_article(article_text: str) -> TechArticleSummary:
    """分析技术文章并提取结构化摘要。"""
    schema_desc = json.dumps(TechArticleSummary.model_json_schema(), ensure_ascii=False, indent=2)
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": f"你是一个技术文章分析助手。请分析用户提供的文章内容，严格按以下 JSON Schema 输出摘要：\n\n{schema_desc}"
            },
            {"role": "user", "content": article_text},
        ],
        response_format={"type": "json_object"},
        temperature=0.2,
    )
    return TechArticleSummary.model_validate_json(response.choices[0].message.content)

# 测试
sample_article = """
LangChain 是一个用于构建 LLM 应用的开源框架。它提供了 Chain、Agent、Memory 等核心抽象，
让开发者可以快速搭建复杂的 AI 应用。使用 LangChain，你可以将 LLM 与外部工具（搜索引擎、
数据库、API）连接起来，实现远超纯文本生成的功能。LangChain 支持 Python 和 JavaScript，
目前已是 AI 应用开发领域最流行的框架之一。对于有 Python 基础的开发者来说，上手 LangChain
只需 1-2 天的时间。
"""

if __name__ == "__main__":
    summary = analyze_article(sample_article)
    print(f"标题：{summary.title}")
    print(f"技术栈：{summary.main_technologies}")
    print(f"关键观点：")
    for i, point in enumerate(summary.key_points, 1):
        print(f"  {i}. {point}")
    print(f"难度：{summary.difficulty}")
    print(f"推荐读者：{summary.recommended_audience}")