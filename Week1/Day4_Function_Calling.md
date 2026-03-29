# Week 1 · Day 4 — Function Calling / Tool Use：让 LLM 调用外部工具

> **目标**：理解 LLM 如何通过 `tools` 参数"调用"外部函数，掌握完整的 Function Calling 请求-响应-回传流程，手写一个可运行的工具调用示例。  
> **时间**：1 小时  
> **前置条件**：已完成 Day 2-3，拥有可用的 DeepSeek API Key，Python 环境已安装 `openai` 和 `python-dotenv`。

---

## 一、为什么需要 Function Calling？（5 分钟）

LLM 的核心能力是**生成文本**，但它有几个本质局限：

| 局限 | 具体表现 | 举例 |
|------|---------|------|
| **无法获取实时信息** | 训练数据有截止日期，不知道"现在" | "今天天气怎么样？" → 只能编造 |
| **不擅长精确计算** | 基于概率预测，不是计算器 | "1234567 × 7654321 = ?" → 极易算错 |
| **无法操作外部系统** | 它只能输出文字，不能执行动作 | "帮我发一封邮件" → 只能写出邮件内容，不能真的发 |

**Function Calling 是解决方案**：让 LLM 不直接回答，而是告诉你"我需要调用某个函数来获取信息"，你在代码中执行这个函数，再把结果喂回给 LLM，由它组织最终回答。

### LLM 在 Function Calling 中的角色

> 重要认知转变：LLM **不会执行**任何函数，它只做两件事：
> 1. **决定**要不要调用、调用哪个函数、传什么参数
> 2. **综合**函数返回的结果，组织自然语言回答
>
> 所有函数的实际执行，都是你的代码完成的。LLM 本质上是一个"智能路由器"。

---

## 二、完整流程概览（5 分钟）

Function Calling 的完整交互分 **4 步**：

```
┌─────────────────────────────────────────────────────────────┐
│  你的代码                          LLM API                  │
│                                                             │
│  ① 发送请求（包含 tools 定义）  ──────►                     │
│                                                             │
│                               ◄──────  ② 返回 tool_calls   │
│                                       （函数名 + 参数）     │
│                                                             │
│  ③ 执行函数，得到结果                                       │
│                                                             │
│  ④ 把结果回传给 LLM            ──────►                      │
│                                                             │
│                               ◄──────  ⑤ 返回最终回答      │
└─────────────────────────────────────────────────────────────┘
```

| 步骤 | 谁做 | 做什么 |
|------|------|--------|
| ①  | 你的代码 | 把用户问题 + 可用工具列表发给 LLM |
| ②  | LLM | 分析问题，决定调用哪个工具及参数，返回 `tool_calls` |
| ③  | 你的代码 | 在本地执行对应函数，拿到真实结果 |
| ④  | 你的代码 | 把函数执行结果以 `tool` 角色消息回传给 LLM |
| ⑤  | LLM | 结合函数结果，组织自然语言回答返回给用户 |

---

## 三、`tools` 参数结构详解（10 分钟）

向 LLM 描述可用工具时，使用 `tools` 参数，它是一个数组，每个元素定义一个工具。格式遵循 JSON Schema 规范：

```json
{
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_current_weather",
        "description": "获取指定城市的当前天气信息",
        "parameters": {
          "type": "object",
          "properties": {
            "city": {
              "type": "string",
              "description": "城市名称，例如：北京、上海"
            },
            "unit": {
              "type": "string",
              "enum": ["celsius", "fahrenheit"],
              "description": "温度单位，默认摄氏度"
            }
          },
          "required": ["city"]
        }
      }
    }
  ]
}
```

### 各字段含义

| 字段 | 含义 | 注意事项 |
|------|------|---------|
| `type` | 固定为 `"function"` | 目前只支持 function 类型 |
| `function.name` | 函数名称 | LLM 返回时用这个名称标识要调用哪个函数 |
| `function.description` | 功能描述 | **极其重要**，LLM 根据这段描述决定何时调用此工具 |
| `function.parameters` | 参数定义（JSON Schema） | 定义参数名、类型、说明、是否必填 |
| `parameters.required` | 必填参数列表 | 不在列表中的参数 LLM 可能不传 |

> **关键理解**：`description` 字段的质量直接决定 LLM 能否正确判断何时使用该工具。写得模糊，LLM 就可能在不该调用时调用，或该调用时不调用。这本质上也是 Prompt Engineering。

---

## 四、`tool_calls` 响应结构（5 分钟）

当 LLM 决定调用工具时，返回的 `choices[0].message` 中会包含 `tool_calls` 字段：

```json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": null,
        "tool_calls": [
          {
            "id": "call_abc123",
            "type": "function",
            "function": {
              "name": "get_current_weather",
              "arguments": "{\"city\": \"北京\", \"unit\": \"celsius\"}"
            }
          }
        ]
      },
      "finish_reason": "tool_calls"
    }
  ]
}
```

### 关键点

| 字段 | 说明 |
|------|------|
| `tool_calls[].id` | 这次调用的唯一 ID，回传结果时必须带上 |
| `tool_calls[].function.name` | LLM 选择的函数名，对应你在 `tools` 中定义的 `name` |
| `tool_calls[].function.arguments` | JSON **字符串**（不是对象），需要 `json.loads()` 解析 |
| `content` | 通常为 `null`，因为 LLM 选择了调用工具而不是直接回答 |
| `finish_reason` | 值为 `"tool_calls"` 而非 `"stop"`，表示需要你执行工具后继续 |

> ⚠️ `arguments` 是字符串，不是字典！这是新手常见的坑。必须用 `json.loads()` 解析。

---

## 五、动手实验：完整的 Function Calling 示例（25 分钟）

### Step 1：创建实验脚本

在 `Week1/` 目录下新建 `day4_function_calling.py`，粘贴以下完整代码：

```python
"""
Day 4 实验：Function Calling 完整流程
演示 LLM 如何通过 tools 参数调用外部函数
"""
import os
import json
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)


# ──────────────────────────────────────────────
# 第一部分：定义本地函数（模拟外部工具）
# ──────────────────────────────────────────────

def get_current_time(timezone: str = "Asia/Shanghai") -> str:
    """获取当前时间（模拟）。"""
    now = datetime.now()
    return json.dumps({
        "timezone": timezone,
        "datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
        "weekday": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][now.weekday()],
    }, ensure_ascii=False)


def calculate(expression: str) -> str:
    """
    安全地计算数学表达式。
    仅允许数字和基本运算符，防止代码注入。
    """
    allowed = set("0123456789+-*/.() ")
    if not all(c in allowed for c in expression):
        return json.dumps({"error": "不支持的字符，仅允许数字和 +-*/()"}, ensure_ascii=False)
    try:
        result = eval(expression)  # 已通过白名单过滤，安全
        return json.dumps({"expression": expression, "result": result}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": f"计算出错: {str(e)}"}, ensure_ascii=False)


def get_weather(city: str) -> str:
    """获取天气信息（模拟数据，实际项目中会调用天气 API）。"""
    mock_data = {
        "北京": {"temp": 22, "condition": "晴", "humidity": 45},
        "上海": {"temp": 26, "condition": "多云", "humidity": 72},
        "深圳": {"temp": 30, "condition": "阵雨", "humidity": 85},
    }
    info = mock_data.get(city, {"temp": 25, "condition": "晴", "humidity": 50})
    return json.dumps({
        "city": city,
        "temperature": f"{info['temp']}°C",
        "condition": info["condition"],
        "humidity": f"{info['humidity']}%",
    }, ensure_ascii=False)


# ──────────────────────────────────────────────
# 第二部分：为 LLM 定义工具描述（JSON Schema）
# ──────────────────────────────────────────────

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "获取当前的日期和时间，包括星期几",
            "parameters": {
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "时区，例如 Asia/Shanghai、America/New_York",
                    }
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "计算数学表达式，支持加减乘除和括号",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "要计算的数学表达式，例如 (12 + 34) * 56",
                    }
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的当前天气信息，包括温度、天气状况和湿度",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称，例如：北京、上海、深圳",
                    }
                },
                "required": ["city"],
            },
        },
    },
]


# ──────────────────────────────────────────────
# 第三部分：函数名到实际函数的映射（调度器）
# ──────────────────────────────────────────────

TOOL_FUNCTIONS = {
    "get_current_time": get_current_time,
    "calculate": calculate,
    "get_weather": get_weather,
}


# ──────────────────────────────────────────────
# 第四部分：完整的 Function Calling 流程
# ──────────────────────────────────────────────

def run_with_tools(user_message: str):
    """
    完整的 Function Calling 流程：
    发送请求 → 判断是否需要调用工具 → 执行工具 → 回传结果 → 获取最终回答
    """
    print(f"\n{'='*60}")
    print(f"用户提问：{user_message}")
    print(f"{'='*60}")

    messages = [
        {"role": "system", "content": "你是一个有用的助手，可以查询时间、计算数学表达式、查询天气。请根据用户问题判断是否需要使用工具。"},
        {"role": "user", "content": user_message},
    ]

    # ── 第 1 次请求：发送用户问题 + 工具定义 ──
    print("\n>>> 第 1 步：发送请求（含 tools 定义）...")
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=tools,
        temperature=0.0,
    )

    assistant_message = response.choices[0].message
    print(f"    finish_reason = {response.choices[0].finish_reason}")

    # ── 判断：LLM 是否选择调用工具？ ──
    if not assistant_message.tool_calls:
        # LLM 认为不需要调用工具，直接回答
        print(f"\n[LLM 直接回答]：{assistant_message.content}")
        return

    # ── 第 2 步：LLM 返回了 tool_calls，逐个执行 ──
    print(f"\n>>> 第 2 步：LLM 请求调用 {len(assistant_message.tool_calls)} 个工具")

    # 把 assistant 的 tool_calls 消息加入对话历史（必须！）
    messages.append(assistant_message)

    for tool_call in assistant_message.tool_calls:
        func_name = tool_call.function.name
        func_args = json.loads(tool_call.function.arguments)

        print(f"    工具：{func_name}")
        print(f"    参数：{func_args}")

        # 执行对应的本地函数
        func = TOOL_FUNCTIONS.get(func_name)
        if func is None:
            result = json.dumps({"error": f"未知工具: {func_name}"}, ensure_ascii=False)
        else:
            result = func(**func_args)

        print(f"    结果：{result}")

        # ── 第 3 步：把工具执行结果回传（role="tool"）──
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,   # 必须与 tool_call.id 对应
            "content": result,
        })

    # ── 第 4 步：再次请求 LLM，让它基于工具结果生成最终回答 ──
    print("\n>>> 第 3 步：将工具结果回传，请求最终回答...")
    final_response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=tools,
        temperature=0.0,
    )

    final_answer = final_response.choices[0].message.content
    print(f"\n[最终回答]：{final_answer}")


# ──────────────────────────────────────────────
# 第五部分：运行实验
# ──────────────────────────────────────────────

if __name__ == "__main__":

    # 实验 1：需要查时间
    run_with_tools("现在几点了？今天星期几？")

    # 实验 2：需要计算
    run_with_tools("帮我算一下 (125 + 375) * 24 / 8 等于多少")

    # 实验 3：需要查天气
    run_with_tools("北京今天天气怎么样？")

    # 实验 4：不需要工具（LLM 应直接回答）
    run_with_tools("你好，请做一下自我介绍")

    # 实验 5：可能需要多个工具
    run_with_tools("现在几点了？另外帮我算一下 3.14 * 100")
```

### Step 2：运行脚本

```powershell
cd d:\Users\hanqiang.wang\source\repos\Agent\Week1
python day4_function_calling.py
```

### Step 3：逐段解读输出

#### 实验 1 预期输出

```
============================================================
用户提问：现在几点了？今天星期几？
============================================================

>>> 第 1 步：发送请求（含 tools 定义）...
    finish_reason = tool_calls

>>> 第 2 步：LLM 请求调用 1 个工具
    工具：get_current_time
    参数：{}
    结果：{"timezone": "Asia/Shanghai", "datetime": "2025-03-29 14:30:00", "weekday": "周六"}

>>> 第 3 步：将工具结果回传，请求最终回答...

[最终回答]：现在是 2025 年 3 月 29 日 14:30，今天是周六。
```

#### 实验 4 预期输出

```
============================================================
用户提问：你好，请做一下自我介绍
============================================================

>>> 第 1 步：发送请求（含 tools 定义）...
    finish_reason = stop

[LLM 直接回答]：你好！我是一个 AI 助手，可以帮你查询时间、计算数学表达式、查询天气……
```

> **关键观察**：当用户问题不需要工具时，LLM 不会强行调用，`finish_reason` 为 `stop` 而非 `tool_calls`。LLM **自主判断**是否需要使用工具。

---

## 六、核心代码逐行解析（回顾巩固）

### 6.1 为什么必须把 `assistant_message` 加入 messages？

```python
messages.append(assistant_message)
```

因为第二次请求时，LLM 需要"看到"自己曾经提出过工具调用请求。如果缺少这条消息，LLM 就不知道 `tool` 角色的消息是回应什么的，会报错或产生混乱。

### 6.2 `tool_call_id` 的作用

```python
{
    "role": "tool",
    "tool_call_id": tool_call.id,   # 对应关系
    "content": result,
}
```

当 LLM 同时调用多个工具时，`tool_call_id` 让 LLM 知道哪个结果对应哪个调用。这是一对一的映射关系。

### 6.3 `arguments` 是字符串不是字典

```python
func_args = json.loads(tool_call.function.arguments)
```

这是初学者最常踩的坑。`tool_call.function.arguments` 返回的是 JSON 格式的**字符串**，必须用 `json.loads()` 解析成 Python 字典后才能作为函数参数使用。

---

## 七、与传统 API 调用的对比思考

作为传统软件工程师，理解这个对比有助于建立正确的心智模型：

| 对比维度 | 传统 API 集成 | Function Calling |
|----------|--------------|-----------------|
| **调用决策** | 写 `if/else` 硬编码判断何时调用 | LLM 根据自然语言语义自主决定 |
| **参数提取** | 正则/表单解析，精确但僵硬 | LLM 从自然语言中提取参数，灵活但需验证 |
| **新增功能** | 加路由、加代码、加文档 | 在 `tools` 数组中加一个 JSON 定义 |
| **错误模式** | 404、参数校验失败 | LLM 可能选错工具、传错参数、幻觉参数 |

> **思维转变**：传统开发中你是"决策者"（代码决定调用什么），Function Calling 中 LLM 是"决策者"（LLM 决定调用什么），你是"执行者"（代码负责执行并返回结果）。

---

## 八、关键规律总结

| # | 规律 | 实验依据 |
|---|------|---------|
| 1 | **LLM 不执行函数，只输出调用意图**：理解 LLM 是"路由器"而非"执行器" | 全部实验 |
| 2 | **`description` 是工具被选中的关键**：写清楚工具能做什么、什么时候该用 | 实验 1-4 的工具选择准确性 |
| 3 | **`arguments` 是字符串**：必须 `json.loads()` 解析 | 代码第三部分 |
| 4 | **`tool_call_id` 不可省略**：多工具并行调用时是必要的对应标识 | 实验 5 |
| 5 | **LLM 会自主判断是否需要工具**：不需要工具时会直接回答，不会强行调用 | 实验 4 |
| 6 | **完整消息链必须保持**：assistant 的 tool_calls 消息和 tool 结果消息缺一不可 | 代码第四部分 |

---

## 九、自选挑战（剩余时间）

**挑战 A（简单）**：修改 `get_weather` 函数的 `description`，故意写得很模糊（如 "一个工具"），观察 LLM 是否还能正确选择它。体会 description 质量的影响。

**挑战 B（中等）**：新增一个工具 `translate`（翻译），接收 `text`（待翻译文本）和 `target_language`（目标语言）两个参数，在本地用简单的字典模拟翻译结果。测试 LLM 能否正确路由 "把'你好'翻译成英文" 这类请求。

**挑战 C（进阶）**：修改 `run_with_tools` 函数，支持**多轮**工具调用——即 LLM 第二次返回的 `finish_reason` 仍然是 `tool_calls` 时，继续执行工具并回传，直到 LLM 返回 `stop` 为止。这为周日实现 ReAct 循环做准备。

---

## 十、今日笔记模板

```
日期：____
核心理解：
  - Function Calling 的本质是：
  - 完整流程的 4 个步骤是：
  - arguments 字段需要注意：
  - description 的重要性体现在：
与传统开发的最大差异：
遗留问题（后续查）：
```

---

## 十一、明日预告（Day 5）

**环境搭建**：搭建正式的 Python 项目结构，安装 `openai` / `anthropic` SDK，配置 `.env` 管理 API Key，为周六的 ChatBot 综合实践做好工程准备。
