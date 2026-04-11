# Week 2 · Day 11 — LangChain Tools & Agents：用框架复现 ReAct Agent

> **目标**：掌握 LangChain 的工具系统（内置工具 + 自定义工具），使用 `create_react_agent` 快速构建一个 ReAct Agent，并与 Week 1 手写版本进行对比。  
> **时间**：1 小时  
> **前置条件**：已完成 Day 10，理解 LangChain 的 Chain/LLM/PromptTemplate 核心概念，`langchain` 和 `langchain-openai` 已安装。

---

## 一、LangChain 工具系统概览（10 分钟）

Week 1 Day 4 中我们手写了 `tools` JSON Schema 来定义工具，Day 7 中又手写了工具调度逻辑（根据 LLM 返回的函数名查找并执行对应函数）。这些"胶水代码"在 LangChain 中已被封装好了。

### 核心概念

| 概念 | 说明 | 对应 Week 1 的手写代码 |
|------|------|----------------------|
| **Tool** | 一个可被 Agent 调用的工具（函数 + 描述） | Day 4 手写的 `tools` JSON Schema + 函数映射 |
| **@tool 装饰器** | 用 Python 装饰器快速定义自定义工具 | 省去手写 JSON Schema 的过程 |
| **Agent** | 拥有 LLM + Tools 的智能体，能自主决策调用哪个工具 | Day 7 手写的 ReAct 循环 |
| **AgentExecutor** | Agent 的运行时引擎，负责执行循环和异常处理 | Day 7 手写的 while 循环 + tool_calls 分发 |

> **重要认知转变**：LangChain 的工具系统不是简单的函数包装——它自动生成 JSON Schema、处理参数验证、管理错误重试。这些在手写时占了 30-50% 的代码量。

---

## 二、动手实践（30 分钟）

在 `Week2/` 目录下创建 `day11_langchain_agent.py`：

### Step 1：用 @tool 装饰器定义自定义工具

```python
import os
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

load_dotenv()

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
    temperature=0,
)

# ── 自定义工具定义 ────────────────────────────────────────

@tool
def get_current_time() -> str:
    """获取当前日期和时间。当用户问"现在几点""今天几号"等时间相关问题时使用。"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@tool
def calculator(expression: str) -> str:
    """计算数学表达式。输入一个合法的 Python 数学表达式（如 '2+3*4'），返回计算结果。
    
    Args:
        expression: 数学表达式字符串，如 '2+3*4', '100/7', '2**10'
    """
    try:
        # 安全限制：只允许数字和基本运算符
        allowed = set('0123456789+-*/.() ')
        if not all(c in allowed for c in expression):
            return "错误：表达式包含不允许的字符"
        result = eval(expression)  # 已做安全过滤
        return str(result)
    except Exception as e:
        return f"计算错误：{e}"

@tool
def search_knowledge(query: str) -> str:
    """搜索内部知识库。当用户问关于公司政策、技术文档等内部信息时使用。
    
    Args:
        query: 搜索关键词
    """
    # 模拟知识库（实际项目中对接向量数据库）
    knowledge_base = {
        "请假": "公司年假政策：入职满1年享受5天年假，满3年10天，满5年15天。请假需提前3天在OA系统申请。",
        "报销": "报销流程：填写报销单→附发票→部门经理审批→财务审核→打款（5个工作日内）。单笔500元以上需总监审批。",
        "技术栈": "公司主要技术栈：后端 Python/FastAPI，前端 React/TypeScript，数据库 PostgreSQL，部署 Docker/K8s。",
    }
    for key, value in knowledge_base.items():
        if key in query:
            return value
    return f"未找到与"{query}"相关的信息，请尝试其他关键词。"

# 查看工具的自动生成信息
tools = [get_current_time, calculator, search_knowledge]
for t in tools:
    print(f"工具名: {t.name}")
    print(f"  描述: {t.description}")
    print(f"  参数: {t.args_schema.model_json_schema()}")
    print()
```

对比 Week 1 手写的工具定义：

| 方面 | Week 1 手写 | LangChain @tool |
|------|------------|-----------------|
| Schema 定义 | 手写 JSON（10-20 行） | 自动从函数签名和 docstring 生成 |
| 参数验证 | 自己写 if-else | Pydantic 自动验证 |
| 函数映射 | 手写 `{name: func}` 字典 | 框架自动管理 |
| 错误处理 | 自己 try-except | 框架内置重试/降级机制 |

### Step 2：创建 ReAct Agent

```python
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# ── 方式 1：使用 LLM 原生的工具调用能力（推荐）───────────

# 绑定工具到 LLM
llm_with_tools = llm.bind_tools(tools)

# 创建 Agent Prompt
agent_prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一个智能助手，可以使用以下工具来帮助用户：
- get_current_time：查询当前时间
- calculator：进行数学计算
- search_knowledge：搜索内部知识库

请根据用户的问题，判断是否需要使用工具。如果需要，调用相应的工具获取信息后再回答。
如果不需要工具，直接回答即可。"""),
    MessagesPlaceholder(variable_name="chat_history", optional=True),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# ── 方式 2：使用 LangGraph 的 create_react_agent（新版推荐）
# 注意：langchain 新版推荐使用 langgraph 替代 AgentExecutor
# 这里我们先用经典方式熟悉概念，Week 6 再学 LangGraph

from langchain.agents import create_tool_calling_agent

agent = create_tool_calling_agent(llm, tools, agent_prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,  # 打印推理过程——对应 Week1 ReAct 的 Thought/Action/Observation
    max_iterations=5,  # 最大迭代次数，防止无限循环
    handle_parsing_errors=True,  # 自动处理输出解析错误
)
```

### Step 3：运行并观察 Agent 推理过程

```python
# ── 测试 Agent ────────────────────────────────────────────
if __name__ == "__main__":
    # 测试 1：需要工具的问题
    print("=" * 60)
    print("测试 1：时间查询")
    result = agent_executor.invoke({"input": "现在几点了？"})
    print(f"最终回答: {result['output']}")

    # 测试 2：数学计算
    print("\n" + "=" * 60)
    print("测试 2：数学计算")
    result = agent_executor.invoke({"input": "帮我计算 (15 + 27) * 3 - 18 / 2"})
    print(f"最终回答: {result['output']}")

    # 测试 3：知识库搜索
    print("\n" + "=" * 60)
    print("测试 3：知识库搜索")
    result = agent_executor.invoke({"input": "公司的请假政策是什么？"})
    print(f"最终回答: {result['output']}")

    # 测试 4：不需要工具的问题
    print("\n" + "=" * 60)
    print("测试 4：直接回答")
    result = agent_executor.invoke({"input": "Python 的 list comprehension 怎么用？"})
    print(f"最终回答: {result['output']}")

    # 测试 5：多工具组合
    print("\n" + "=" * 60)
    print("测试 5：多工具组合")
    result = agent_executor.invoke({
        "input": "现在几点了？另外帮我算一下如果每天工作8小时，一周工作5天，一个月工作多少小时？"
    })
    print(f"最终回答: {result['output']}")
```

> **观察要点**：打开 `verbose=True` 后，观察控制台输出中的 **Thought → Action → Observation** 循环。对比 Week 1 Day 7 手写的 ReAct 循环，框架帮你省略了哪些代码？

---

## 三、关键对比：手写 vs 框架（10 分钟）

运行以上代码后，回顾 Week 1 的实现，填写以下对比表：

| 维度 | Week 1 手写 ReAct | LangChain Agent |
|------|-------------------|-----------------|
| 工具定义 | 手写 JSON Schema（~20行/工具） | `@tool` + docstring（~5行/工具） |
| 推理循环 | while 循环 + 消息拼接（~30行） | `AgentExecutor` 内置 |
| 错误处理 | 自己实现 | `handle_parsing_errors=True` |
| 最大迭代控制 | 自己加计数器 | `max_iterations` 参数 |
| 推理过程可视化 | 自己 print | `verbose=True` |
| 模型切换 | 改 API 参数 | 换一个 ChatModel 类即可 |
| 灵活性 | ⭐⭐⭐⭐⭐ 完全控制 | ⭐⭐⭐ 受框架约束 |
| 开发效率 | ⭐⭐ 慢 | ⭐⭐⭐⭐⭐ 快 |

> **思考**：在什么场景下应该选择手写？什么场景下应该选择框架？答案明天揭晓。

---

## 四、关键要点总结

| # | 要点 | 说明 |
|---|------|------|
| 1 | `@tool` 装饰器是定义工具的最快方式 | 自动从函数签名生成 JSON Schema |
| 2 | `AgentExecutor` 封装了完整的 ReAct 循环 | 包含迭代控制、错误处理、输出解析 |
| 3 | `verbose=True` 是调试 Agent 的利器 | 可以看到每一步的思考和行动 |
| 4 | 框架提升效率但降低控制力 | 在理解底层后使用框架是最佳实践 |

---

## 五、自检清单

- [ ] 能用 `@tool` 装饰器定义至少 2 个自定义工具
- [ ] Agent 能成功调用正确的工具并返回有用的回答
- [ ] 在 `verbose=True` 模式下能读懂 Agent 的推理链路
- [ ] 能说出 `AgentExecutor` 的 `max_iterations` 和 `handle_parsing_errors` 参数的作用
- [ ] 能列举手写 Agent 和框架 Agent 各自的 2 个优势

---

## 六、明日预告

> 明天将进行 **对比与思考**，系统性地分析手写 Agent vs 框架 Agent 的优劣场景，并了解 LlamaIndex 的定位以及与 LangChain 的差异。建议提前浏览 [LlamaIndex 官网](https://www.llamaindex.ai/) 了解其定位。

---