# Week 2 · Day 9 — 结构化输出：JSON Mode、Structured Outputs 与 Pydantic

> **目标**：掌握让 LLM 输出严格结构化数据的三种方式（Prompt 约束、JSON Mode、Structured Outputs），使用 Pydantic 定义输出 Schema 并自动解析 LLM 响应。  
> **时间**：1 小时  
> **前置条件**：已完成 Day 8，理解 System Prompt 设计原则，Python 环境已安装 `openai` 和 `python-dotenv`。

---

## 一、为什么需要结构化输出？（10 分钟）

Day 8 中我们用 System Prompt 约束了 LLM 的输出格式（Markdown 模板），但这种约束是"软约束"——LLM *大概率* 会按格式输出，但偶尔会"跑偏"。在生产环境中，Agent 的输出往往需要被**下游程序自动处理**（解析 JSON、写入数据库、驱动 UI），任何格式偏差都会导致代码崩溃。

### 三种方式对比

| 方式 | 原理 | 可靠性 | 适用场景 |
|------|------|--------|---------|
| **Prompt 约束** | 在 System Prompt 中写"请以 JSON 格式输出" | ⭐⭐ 中等 | 简单场景，对格式要求不严格 |
| **JSON Mode** | API 参数 `response_format={"type": "json_object"}` | ⭐⭐⭐ 较高 | 确保输出合法 JSON，但不限定 Schema |
| **Structured Outputs** | API 参数中传入 JSON Schema 或 Pydantic 模型 | ⭐⭐⭐⭐ 最高 | 需要精确控制每个字段的类型和结构 |

> **重要认知转变**：在传统软件中，函数签名就能保证返回值类型。但 LLM 的"返回值"是自由文本——结构化输出就是给 LLM 的"返回值"加上**类型约束**，让 AI 输出像函数返回值一样可靠。

---

## 二、动手实践三种方式（25 分钟）

在 `Week2/` 目录下创建 `day9_structured_output.py`：

### Step 1：纯 Prompt 约束（不可靠版本）

```python
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

# ── 方式 1：纯 Prompt 约束 ───────────────────────────────
def extract_info_v1(text: str) -> str:
    """通过 Prompt 约束输出 JSON（不可靠）。"""
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个信息提取助手。请从用户输入中提取信息，以 JSON 格式输出，包含 name、age、skills 字段。不要输出任何其他文字。"},
            {"role": "user",   "content": text},
        ],
        temperature=0.1,
    )
    return response.choices[0].message.content

# 测试
text = "张三今年28岁，擅长Python和机器学习，最近在学习LangChain。"
result = extract_info_v1(text)
print("方式1 输出：", result)

# 尝试解析——有可能失败！
try:
    data = json.loads(result)
    print("解析成功：", data)
except json.JSONDecodeError as e:
    print(f"解析失败：{e}")
    print("这就是纯 Prompt 约束不可靠的原因——LLM 可能加了额外文字或格式不对")
```

### Step 2：JSON Mode（保证合法 JSON）

```python
# ── 方式 2：JSON Mode ────────────────────────────────────
def extract_info_v2(text: str) -> dict:
    """使用 JSON Mode 确保输出合法 JSON。"""
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个信息提取助手。请从用户输入中提取信息，以 JSON 格式输出，包含 name(字符串)、age(整数)、skills(字符串数组) 字段。"},
            {"role": "user",   "content": text},
        ],
        response_format={"type": "json_object"},  # 关键参数！
        temperature=0.1,
    )
    return json.loads(response.choices[0].message.content)

result = extract_info_v2(text)
print("方式2 输出：", result)
print(f"  姓名: {result['name']}, 年龄: {result['age']}, 技能: {result['skills']}")
```

> **注意**：JSON Mode 保证输出是合法 JSON，但不保证字段存在或类型正确。LLM 可能返回 `{"person": "张三", "years": 28}` 而非你期望的 `{"name": "张三", "age": 28}`。

### Step 3：Pydantic + 手动解析（推荐生产方案）

```python
from pydantic import BaseModel, Field
from typing import List

# ── 方式 3：Pydantic 定义 Schema ─────────────────────────
class PersonInfo(BaseModel):
    """人物信息提取结果。"""
    name: str = Field(description="人物姓名")
    age: int = Field(description="年龄")
    skills: List[str] = Field(description="技能列表")
    summary: str = Field(description="一句话总结此人的背景")

def extract_info_v3(text: str) -> PersonInfo:
    """使用 Pydantic 定义 Schema，JSON Mode + 解析验证。"""
    # 将 Pydantic 模型转为 JSON Schema 描述
    schema_desc = json.dumps(PersonInfo.model_json_schema(), ensure_ascii=False, indent=2)

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": f"你是一个信息提取助手。请从用户输入中提取信息，严格按以下 JSON Schema 输出：\n\n{schema_desc}"
            },
            {"role": "user", "content": text},
        ],
        response_format={"type": "json_object"},
        temperature=0.1,
    )

    raw = response.choices[0].message.content
    # Pydantic 自动验证字段类型和必填项
    return PersonInfo.model_validate_json(raw)

person = extract_info_v3(text)
print("方式3 输出：")
print(f"  姓名: {person.name}")
print(f"  年龄: {person.age}")
print(f"  技能: {person.skills}")
print(f"  总结: {person.summary}")
print(f"  类型: {type(person)}")  # <class 'PersonInfo'> — 真正的类型安全！
```

---

## 三、实战练习：构建一个结构化提取管道（15 分钟）

将结构化输出应用到更复杂的场景——从一段技术文章中提取多维信息：

```python
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
```

> **观察要点**：对比方式 1 和方式 3，思考以下问题——当 Pydantic 验证失败时如何优雅处理？在 Agent 流程中，结构化输出能消除哪些不确定性？

---

## 四、关键要点总结

| # | 要点 | 说明 |
|---|------|------|
| 1 | 纯 Prompt 约束是"软约束" | LLM 大概率遵守，但无法保证 100% |
| 2 | JSON Mode 保证合法 JSON | 但不约束具体的字段和类型 |
| 3 | Pydantic + JSON Schema = 类型安全 | 既约束输出结构，又自动验证和解析 |
| 4 | `temperature` 越低，格式越稳定 | 结构化输出任务推荐 0.1~0.3 |
| 5 | 结构化输出是 Agent 管道化的基础 | Agent 的思考 → 工具调用 → 结果处理，全靠结构化数据流转 |

---

## 五、自检清单

- [ ] 能说出三种结构化输出方式的优劣和适用场景
- [ ] 已运行三种方式的代码并对比输出结果
- [ ] 能用 Pydantic 的 `BaseModel` 定义一个包含嵌套结构的输出模型
- [ ] 理解 `response_format={"type": "json_object"}` 的作用和局限性
- [ ] 为一个自定义场景（如：简历解析、Bug 报告提取）编写了结构化提取代码

---

## 六、明日预告

> 明天将学习 **LangChain 快速入门**，了解 Chain、LLM、PromptTemplate 三大核心概念。建议提前安装 LangChain：`pip install langchain langchain-openai`，并浏览 [LangChain 官方文档](https://python.langchain.com/docs/get_started/introduction) 的 Quickstart 部分。

---