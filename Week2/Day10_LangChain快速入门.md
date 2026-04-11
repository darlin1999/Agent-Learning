# Week 2 · Day 10 — LangChain 快速入门：Chain、LLM、PromptTemplate

> **目标**：理解 LangChain 框架的设计哲学和核心抽象（LLM、PromptTemplate、Chain），跑通官方快速入门示例，建立"用框架构建 AI 应用"的思维方式。  
> **时间**：1 小时  
> **前置条件**：已完成 Day 8-9，掌握 System Prompt 设计和结构化输出。Python 环境已安装 `openai`、`pydantic`。

---

## 一、LangChain 是什么？为什么需要它？（10 分钟）

Week 1 我们用原生 SDK 手写了 ChatBot 和 ReAct Agent，这种方式的优点是理解底层原理，但缺点也很明显——**大量重复的胶水代码**。LangChain 就是用来消除这些胶水代码的框架。

### 核心概念

| 概念 | 说明 | 类比传统开发 |
|------|------|-------------|
| **LLM / ChatModel** | 对各AI 模型的统一封装（OpenAI、DeepSeek、Anthropic…… | 数据库连接层（不管用 MySQL 还是 PostgreSQL，接口一样） |
| **PromptTemplate** | 可复用的 Prompt 模板，支持变量插值 | 前端的模板引擎（如 Jinja2） |
| **Chain (LCEL)** | 将多个组件串联成流水线（Prompt → LLM → 解析器） | Unix 管道（`cat file | grep pattern | sort`） |
| **OutputParser** | 将 LLM 的文本输出解析为结构化数据 | 反序列化层（JSON → 对象） |

> **重要认知转变**：LangChain 不是让你用更少的代码调 API——它是让你用**可组合的积木**搭建复杂的 AI 流程。就像 React 不只是简化 DOM 操作，而是引入了组件化思维。

### LangChain 生态速览

```
┌─────────────────────────────────────────────┐
│  langchain-core   ← 核心抽象（必装）        │
│  langchain        ← Chain/Agent/Memory 实现 │
│  langchain-openai ← OpenAI/DeepSeek 集成    │
│  langchain-community ← 社区工具集成          │
│  langsmith        ← 可观测性平台（选装）     │
└─────────────────────────────────────────────┘
```

---

## 二、环境准备 + 快速上手（25 分钟）

### Step 1：安装 LangChain

```powershell
pip install langchain langchain-openai langchain-core
```

### Step 2：最简示例——直接调用 ChatModel

在 `Week2/` 目录下创建 `day10_langchain_intro.py`：

```python
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

# ── 1. 创建 ChatModel 实例 ──────────────────────────────
# LangChain 封装了模型连接，支持通过统一接口对接多种模型
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
    temperature=0.7,
)

# ── 2. 最简调用（等价于直接用 openai SDK） ───────────────
response = llm.invoke("用一句话解释什么是 LangChain")
print(response.content)
print(f"Token 使用: {response.response_metadata.get('token_usage', 'N/A')}")
```

对比原生 SDK 的代码量：

| 操作 | 原生 SDK | LangChain |
|------|---------|-----------|
| 初始化客户端 | 3-4 行 | 4-5 行 |
| 发送请求 | 5-8 行 | 1 行 |
| 提取回复内容 | `response.choices[0].message.content` | `response.content` |

到目前为止优势并不明显。**真正的威力在 Chain 组合**——继续往下看。

### Step 3：PromptTemplate——可复用的模板

```python
from langchain_core.prompts import ChatPromptTemplate

# ── 3. 使用 PromptTemplate ───────────────────────────────
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个{domain}领域的专家，用{style}的风格回答问题。"),
    ("human", "{question}"),
])

# 查看模板变量
print("模板变量:", prompt.input_variables)  # ['domain', 'question', 'style']

# 填充模板——此时还没调用 LLM
filled = prompt.invoke({
    "domain": "Python 编程",
    "style": "简洁专业",
    "question": "装饰器有什么用？"
})
print("填充后的消息:", filled)
```

### Step 4：Chain——用管道 `|` 组合组件（核心！）

```python
# ── 4. LCEL：LangChain Expression Language ───────────────
# 用 | 符号将组件串联，就像 Unix 管道
chain = prompt | llm

# 一行代码完成：模板填充 → 调用 LLM → 返回结果
result = chain.invoke({
    "domain": "Python 编程",
    "style": "简洁专业",
    "question": "装饰器有什么用？"
})
print("Chain 输出:", result.content)
```

### Step 5：加入 OutputParser——完整管道

```python
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from pydantic import BaseModel, Field
from typing import List

# 方式 A：字符串解析器（最简单）
str_chain = prompt | llm | StrOutputParser()
text_result = str_chain.invoke({
    "domain": "Python 编程",
    "style": "简洁专业",
    "question": "列举 3 个常用的内置装饰器"
})
print(type(text_result))  # <class 'str'> — 直接是字符串，不再是 AIMessage

# 方式 B：JSON 解析器（结合 Day 9 的知识）
class CodeExample(BaseModel):
    topic: str = Field(description="主题")
    code: str = Field(description="代码示例")
    explanation: str = Field(description="代码说明")

json_parser = JsonOutputParser(pydantic_object=CodeExample)

json_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个编程助手。{format_instructions}"),
    ("human", "给一个 {topic} 的代码示例"),
])

json_chain = json_prompt | llm | json_parser

json_result = json_chain.invoke({
    "topic": "Python 装饰器",
    "format_instructions": json_parser.get_format_instructions(),
})
print("JSON 输出:", json_result)
print(f"  主题: {json_result['topic']}")
print(f"  代码: {json_result['code'][:50]}...")
```

---

## 三、Chain 组合的威力：多步骤流水线（15 分钟）

### 一个真实场景：翻译 + 摘要

```python
# ── 多步骤 Chain：翻译后再总结 ────────────────────────────
translate_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业翻译。将用户输入的英文翻译为中文。只输出翻译结果。"),
    ("human", "{english_text}"),
])

summarize_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个摘要助手。用 3 个要点总结以下内容。"),
    ("human", "{text}"),
])

# 管道 1：英文 → 中文
translate_chain = translate_prompt | llm | StrOutputParser()

# 管道 2：中文 → 摘要（注意输入 key 的映射）
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

full_chain = (
    {"english_text": RunnablePassthrough()}
    | translate_chain
    | (lambda translated: {"text": translated})
    | summarize_prompt
    | llm
    | StrOutputParser()
)

english = """
LangChain is a framework for developing applications powered by large language models.
It provides modular components for building chains, agents, and retrieval systems. 
The framework supports multiple LLM providers and offers tools for prompt management,
memory, and output parsing. LangChain uses LCEL (LangChain Expression Language) for
composing chains with a simple pipe syntax.
"""

if __name__ == "__main__":
    final_result = full_chain.invoke(english)
    print("翻译 + 摘要结果：")
    print(final_result)
```

> **观察要点**：思考如果用原生 SDK 实现同样的"翻译 → 摘要"流水线需要多少代码。Chain 的组合能力在任务步骤增多时优势呈指数级增长。

---

## 四、关键要点总结

| # | 要点 | 说明 |
|---|------|------|
| 1 | LangChain 的核心价值是组合能力 | 单独调 LLM 它没太大优势，组合多步骤时价值显现 |
| 2 | LCEL 管道语法 `\|` 是核心范式 | `prompt \| llm \| parser` 就是一条完整的处理链 |
| 3 | PromptTemplate 实现 Prompt 复用 | 比字符串拼接更安全、更可维护 |
| 4 | OutputParser 衔接 AI 输出与代码逻辑 | 实现从"文本"到"对象"的桥梁 |

---

## 五、自检清单

- [ ] 已安装 `langchain`、`langchain-openai`、`langchain-core` 并验证可导入
- [ ] 能用 `ChatOpenAI` 成功调用 DeepSeek API
- [ ] 能手写一个 `ChatPromptTemplate` 并用 `invoke()` 填充变量
- [ ] 能用 LCEL 管道语法将 `prompt | llm | parser` 串联成 Chain
- [ ] 理解 `StrOutputParser` 和 `JsonOutputParser` 的区别和使用场景

---

## 六、明日预告

> 明天将学习 **LangChain Tools & Agents**，使用 LangChain 的内置工具和自定义工具，用 `create_react_agent` 复现 Week 1 手写的 ReAct Agent。建议回顾 Week 1 Day 7 的 ReAct Agent 实现，思考哪些部分的代码是可以被框架替代的模板代码。

---