# Week 1 · Day 7（周日）— 深度研究：ReAct 论文精读 + 手写 ReAct Agent

> **目标**：阅读 ReAct 论文理解推理-行动循环（Reasoning + Acting）的核心思想；在 Day 6 的 ChatBot 基础上，用纯原生 SDK（不借助任何框架）实现一个 ReAct 风格的 Agent，完成第 1 周里程碑交付。  
> **时间**：6 小时  
> **前置条件**：Day 6 的 ChatBot 可正常运行，包含 `get_current_time`、`calculate`、`get_weather` 三个工具。

---

## 零、今日定位：从"ChatBot"到"Agent"

Day 6 完成的 ChatBot 已经很强了——它能多轮对话、自动调工具、记忆上下文。但你可能注意到一个问题：

| Day 6 ChatBot | 今天的 ReAct Agent |
|----------------|-------------------|
| LLM 的"思考过程"对你不可见 | 每一步思考都显式输出，你能看到**推理链** |
| LLM 一次性决定调哪个工具 | LLM 先思考（Thought）→ 再决定行动（Action）→ 观察结果（Observation）→ 再思考 |
| 遇到复杂问题可能一步到位失败 | 通过多轮 Thought-Action-Observation 循环，逐步拆解复杂问题 |
| 本质上是 **Function Calling ChatBot** | 本质上是 **推理-行动 Agent** |

这就是 "ChatBot" 和 "Agent" 的核心区别——**Agent 具有自主推理和规划能力**。而 ReAct 正是实现这种能力最经典、最基础的框架。

---

## 一、ReAct 论文精读（1.5 小时）

### 1.1 论文基本信息

- **论文标题**：*ReAct: Synergizing Reasoning and Acting in Language Models*
- **arXiv 链接**：[https://arxiv.org/abs/2210.03629](https://arxiv.org/abs/2210.03629)
- **作者**：Shunyu Yao 等，Princeton / Google Brain
- **发表时间**：2022 年 10 月（这篇论文奠定了后续几乎所有 Agent 框架的理论基础）

### 1.2 带着问题去读

阅读论文前，先带上这几个问题，读完后尝试自己回答：

1. **"Reasoning Only" 和 "Acting Only" 各有什么局限？ReAct 如何同时解决这两个问题？**
2. **ReAct 的 Thought-Action-Observation 三步循环具体是如何工作的？**
3. **论文中 ReAct 和 Chain-of-Thought（CoT）的效果对比如何？在什么场景 ReAct 更有优势？**
4. **ReAct 有什么局限性？论文作者自己提到了哪些？**

### 1.3 论文核心要点总结

> 以下是帮助你理解论文的导读，**不能替代阅读原文**。请先花 40 分钟通读论文，再回来对照。

#### 核心洞察

传统的让 LLM 推理的方法（如 Chain-of-Thought）只有**内部推理**，没有与外部世界交互的能力：

```
用户问题 → LLM 推理 step1 → 推理 step2 → ... → 最终答案
                  ↑ 全程在"脑子里"完成，不能获取新信息
```

而传统的让 LLM 使用工具的方法（如 Function Calling）只有**行动**，缺乏显式的推理过程：

```
用户问题 → LLM 直接决定调用工具 → 得到结果 → 输出答案
                  ↑ 没有展示"为什么要用这个工具"的推理
```

ReAct 的核心贡献是**将两者交织在一起**：

```
用户问题
    → Thought: 我需要先确认xxx，可以用搜索工具
    → Action: search("xxx")
    → Observation: 搜索结果显示...
    → Thought: 现在我知道了xxx，但还需要确认yyy
    → Action: lookup("yyy")
    → Observation: 查到了...
    → Thought: 综合以上信息，我可以得出结论
    → Action: finish("最终答案")
```

#### 为什么"交织"如此重要？

| 机制 | 推理帮助行动 | 行动帮助推理 |
|------|-------------|-------------|
| **推理 → 行动** | "我需要确认日期" → 决定调用日历工具（而不是猜测） | — |
| **行动 → 推理** | — | 搜索返回了新信息 → 更新推理方向、修正之前的假设 |

这种交互使得 Agent 能够：
- **动态规划**：根据中间结果调整策略，而非一开始就定死执行路径
- **自我纠错**：如果某步行动的结果不符合预期，下一步推理可以修正方向
- **可解释**：每一步决策都有明确的推理记录，方便调试和审计

#### ReAct 的 Prompt 格式

论文中使用的是纯 Prompt 驱动（2022 年还没有大规模的 Function Calling API），核心模板是：

```
Question: 用户的问题
Thought 1: 我的推理...
Action 1: 工具名[参数]
Observation 1: 工具返回结果
Thought 2: 基于观察，我进一步推理...
Action 2: 工具名[参数]
Observation 2: ...
...
Thought N: 我现在可以回答了
Action N: finish[最终答案]
```

#### 论文中的关键实验结论

1. **HotpotQA（多跳问答）**：ReAct 比纯 CoT 更准确，因为它能通过搜索获取真实信息，而非凭记忆"幻觉"
2. **FEVER（事实验证）**：ReAct 通过查证能纠正 LLM 的错误记忆
3. **决策任务（ALFWorld / WebShop）**：ReAct 远超纯 Acting 方法，因为推理帮助 Agent 不走弯路
4. **局限**：ReAct 有时会陷入重复循环（反复搜索同一个东西），论文建议结合 CoT 做 fallback

### 1.4 思考练习（读完论文后）

用自己的话回答以下问题，写在纸上或笔记中（这将成为里程碑交付物的一部分）：

1. 你 Day 6 写的 ChatBot 用的是 DeepSeek 的 Function Calling API。它和论文中纯 Prompt 驱动的 ReAct 有什么异同？
2. Function Calling 本质上是 API 层面帮你实 "Action" 和 "Observation" 的标准化，但 "Thought" 呢？Day 6 的 ChatBot 有没有显式的 Thought？
3. 如果让你从零开始实现一个 ReAct Agent，你觉得用 Function Calling API 好，还是纯 Prompt 解析好？各有什么优缺点？

---

## 二、两种实现路线分析（15 分钟）

在动手写代码之前，先理解实现 ReAct Agent 有两条路线：

### 路线 A：纯 Prompt 驱动（论文原始方式）

```
System Prompt 中定义 Thought/Action/Observation 格式
    → LLM 生成文本，包含 "Thought: ..." 和 "Action: 工具名[参数]"
    → 你的代码用正则解析出 Action
    → 执行工具，把结果作为 "Observation: ..." 拼回 Prompt
    → 继续让 LLM 生成下一轮 Thought
```

**优点**：最接近论文原始思想，理解更深  
**缺点**：需要手写正则解析，LLM 输出格式不稳定时容易出错

### 路线 B：Function Calling + Thought 增强（现代实践方式）

```
System Prompt 中要求 LLM 在调用工具之前先输出推理过程
    → LLM 返回 content（Thought）+ tool_calls（Action）
    → 你的代码执行工具，结果作为 tool message 回传（Observation）
    → LLM 继续推理
```

**优点**：工具调用结构化、可靠，不需要正则解析  
**缺点**：Thought 依赖 LLM 是否遵循 System Prompt 的指示

### 今天的选择

**两条路线都要实现**。先实现路线 A（理解论文精髓），再实现路线 B（掌握现代实践）。

---

## 三、项目结构规划（10 分钟）

在已有的 `projects/` 目录下新建 `week1_react_agent/`：

```
projects/week1_react_agent/
├── react_prompt.py      ← 路线 A：纯 Prompt 驱动的 ReAct Agent
├── react_fc.py          ← 路线 B：Function Calling 增强的 ReAct Agent
├── tools.py             ← 工具函数（可复用 week1_chatbot 的，略作调整）
└── README.md            ← 项目说明
```

### 初始化

```powershell
cd D:\Users\hanqiang.wang\source\repos\Agent
mkdir projects\week1_react_agent
```

---

## 四、Step 1：准备工具模块 `tools.py`（15 分钟）

从 `week1_chatbot/tools.py` 复制过来并做一些调整。路线 A 需要工具以"纯文本"方式描述（给 LLM 看），路线 B 沿用 JSON Schema 格式。所以新的 `tools.py` 需要同时导出两种描述。

### 4.1 需要的导出内容

```python
# 工具函数
def get_current_time() -> str: ...
def calculate(expression: str) -> str: ...
def get_weather(city: str) -> str: ...

# 路线 A 使用：工具的纯文本描述（给 System Prompt 用）
TOOL_DESCRIPTIONS = """
可用工具：
1. get_current_time: 获取当前日期、时间和星期几。无需参数。
   用法：Action: get_current_time[]
2. calculate: 计算数学表达式。参数为表达式字符串。
   用法：Action: calculate[表达式]
   示例：Action: calculate[(100 + 200) * 3]
3. get_weather: 获取指定城市的天气信息。参数为城市名。
   用法：Action: get_weather[城市名]
   示例：Action: get_weather[北京]
4. finish: 给出最终答案。参数为答案文本。
   用法：Action: finish[最终答案]
"""

# 路线 A 使用：工具名 → 函数映射（不含 finish，finish 由主循环处理）
TOOL_FUNCTIONS = {
    "get_current_time": get_current_time,
    "calculate": calculate,
    "get_weather": get_weather,
}

# 路线 B 使用：JSON Schema 格式的 tools 列表（和 week1_chatbot 相同）
tools_schema = [ ... ]
```

### 4.2 关键变化

和 Day 6 的 `tools.py` 相比，新增了：
- `TOOL_DESCRIPTIONS`：一段文本，描述所有工具的名称、用途和调用格式。这是给 LLM 阅读的"工具说明书"
- `finish` 工具的概念：ReAct 循环中，LLM 用 `finish[答案]` 来表示推理结束。它不是真正的函数，而是循环终止信号

---

## 五、Step 2：路线 A — 纯 Prompt 驱动的 ReAct Agent（1.5 小时）

这是今天**最核心、最有学习价值**的部分。你将完全用 Prompt 控制 LLM 的推理行为，并用 Python 代码解析和执行。

### 5.1 System Prompt 设计

这是路线 A 的灵魂。你需要写一个 System Prompt，让 LLM 严格按照 Thought → Action → Observation 的格式输出。

参考结构（你需要根据实际效果调整措辞）：

```
你是一个智能助手，通过交替进行"思考"和"行动"来回答用户的问题。

你可以使用以下工具：
{TOOL_DESCRIPTIONS}

你必须严格按照以下格式逐步输出：

Thought: <你的推理过程，分析当前需要做什么>
Action: <工具名>[<参数>]

然后你会收到：
Observation: <工具执行的结果>

你可以重复 Thought/Action/Observation 循环多次。当你得到了足够的信息来回答用户问题时，使用：

Thought: 我现在可以回答了
Action: finish[<你的最终回答>]

重要规则：
1. 每次只输出一个 Thought 和一个 Action，然后停下来等待 Observation
2. 不要自行编造 Observation，Observation 只能由系统提供
3. Action 的格式必须严格为：工具名[参数]
4. 如果问题不需要工具就能回答，直接使用 finish
```

### 5.2 核心循环逻辑

路线 A 的主循环和 Day 6 有本质区别。Day 6 依赖 API 的 `tool_calls` 字段，路线 A 需要你自己**解析 LLM 输出的文本**：

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│  1. 用户输入问题                                              │
│          │                                                   │
│          ▼                                                   │
│  2. 拼接 prompt: system + 历史 + "Question: 用户问题"         │
│          │                                                   │
│          ▼                                                   │
│  3. 调用 LLM（不带 tools 参数！纯文本生成）                    │
│          │                                                   │
│          ▼                                                   │
│  4. 解析 LLM 输出：提取 Thought 和 Action                     │
│          │                                                   │
│     Action 是 finish?                                        │
│      │           │                                           │
│     是           否                                           │
│      │           │                                           │
│      ▼           ▼                                           │
│  5a. 提取答案  5b. 执行对应工具                                │
│      输出给用户  5b-2. 构造 "Observation: 结果"                │
│      结束本轮    5b-3. 追加到对话历史，回到步骤 3               │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### 5.3 文本解析的关键：正则表达式

你需要从 LLM 输出中提取 `Action: 工具名[参数]`。推荐使用正则：

```python
import re

def parse_action(text: str):
    """
    从 LLM 输出中解析 Action。
    匹配格式：Action: 工具名[参数]
    返回 (tool_name, tool_arg) 或 None
    """
    match = re.search(r'Action:\s*(\w+)\[(.+?)\]', text)
    if match:
        return match.group(1), match.group(2)
    return None
```

> ⚠️ 现实中 LLM 的输出格式可能不完全一致（比如多了空格、换了大小写）。今天先用简单正则，后续你会学到更健壮的输出解析策略（第 3 周的 OutputParser）。

### 5.4 需要注意的坑

**坑 1：LLM 自行编造 Observation**  
有时 LLM 会在输出 Action 后紧接着自己写一个 `Observation: ...`。你需要在代码中**只取第一个 Action**，截断后面的内容，然后由你的代码提供真正的 Observation。

**坑 2：LLM 不按格式输出**  
如果 LLM 不输出 `Action: ...` 而是直接给出文本回答，你需要处理这种情况——把它当作隐式的 `finish` 处理。

**坑 3：无限循环**  
设置最大迭代次数（如 10 次），超过后强制终止并提示用户。

**坑 4：不带 `tools` 参数**  
路线 A 的关键点：**调 API 时不要传 `tools` 参数**。你是通过 Prompt 告诉 LLM 有哪些工具的，不是通过 API 参数。如果加了 `tools`，LLM 会走 Function Calling 流程而非 ReAct 文本格式。

### 5.5 预期运行效果

```
========================================
🧠 ReAct Agent（Prompt 驱动）输入 quit 退出
========================================

Question: 今天是星期几？北京天气怎么样？

Thought 1: 用户问了两个问题：今天星期几和北京天气。我需要先查询当前时间。
Action 1: get_current_time[]
Observation 1: {"datetime": "2026-04-10 14:30:00", "weekday": "周五"}

Thought 2: 现在我知道今天是周五了。接下来查询北京天气。
Action 2: get_weather[北京]
Observation 2: {"city": "北京", "temperature": "22°C", "condition": "晴", "humidity": "45%"}

Thought 3: 我已经获得了所有需要的信息，可以回答了。
Action 3: finish[今天是周五（2026年4月10日）。北京当前天气晴，温度22°C，湿度45%。]

✅ 最终回答：今天是周五（2026年4月10日）。北京当前天气晴，温度22°C，湿度45%。
```

注意和 Day 6 的区别——**每一步思考过程都可见**，你能清楚看到 Agent 是如何一步步推理和决策的。

### 5.6 代码骨架

```python
"""
ReAct Agent — 路线 A：纯 Prompt 驱动
通过 System Prompt 控制 LLM 按 Thought/Action/Observation 格式输出
用正则解析 Action，手动执行工具并回传 Observation
"""
import os
import re
from openai import OpenAI
from dotenv import load_dotenv
from tools import TOOL_DESCRIPTIONS, TOOL_FUNCTIONS

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

MAX_ITERATIONS = 10  # 防止无限循环

SYSTEM_PROMPT = f"""你是一个智能助手...（按 5.1 的指引编写）
{TOOL_DESCRIPTIONS}
"""

def parse_action(text: str):
    """从 LLM 输出中解析 Action: 工具名[参数]"""
    # TODO: 实现正则解析

def run_react(question: str) -> str:
    """执行一次完整的 ReAct 推理循环"""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Question: {question}"},
    ]

    for i in range(MAX_ITERATIONS):
        # TODO: 调用 LLM（不带 tools 参数）
        # TODO: 打印 LLM 输出（Thought + Action）
        # TODO: 解析 Action
        # TODO: 如果是 finish，返回最终答案
        # TODO: 如果是其他工具，执行并构造 Observation
        # TODO: 将 LLM 输出和 Observation 追加到 messages
        pass

    return "（达到最大推理步数，强制终止）"

def main():
    print("=" * 40)
    print("🧠 ReAct Agent（Prompt 驱动）输入 quit 退出")
    print("=" * 40)

    while True:
        question = input("\nQuestion: ").strip()
        if question.lower() == "quit":
            print("再见！👋")
            break
        if not question:
            continue

        answer = run_react(question)
        print(f"\n✅ 最终回答：{answer}")

if __name__ == "__main__":
    main()
```

### 5.7 自检清单

完成路线 A 后，验证：

- [ ] 简单问题（如"你好"）：LLM 直接 `finish`，不调工具
- [ ] 单工具问题（如"现在几点"）：Thought → Action → Observation → finish
- [ ] 多工具问题（如"今天几号？帮我算 123*456"）：多轮 Thought-Action-Observation 循环
- [ ] 推理链可见：终端中能看到每一步的 Thought 和 Action
- [ ] 无限循环保护：最大迭代次数生效

---

## 六、Step 3：路线 B — Function Calling 增强的 ReAct Agent（1 小时）

路线 B 是现代 Agent 框架（LangChain、LlamaIndex）的底层实现方式。它结合了 Function Calling 的结构化可靠性和 ReAct 的显式推理能力。

### 6.1 核心思路

和 Day 6 的 ChatBot 相比，只有一个关键变化：**在 System Prompt 中要求 LLM 在决定调用工具之前，先在 `content` 中输出推理过程**。

```python
SYSTEM_PROMPT = """你是一个通过推理和工具调用来回答问题的智能助手。

在每次回复中，请先在回复内容中说明你的思考过程（为什么需要调用这个工具，或者为什么现在可以直接回答），然后再决定是否调用工具。

格式示例：
- 需要工具时：先说明推理过程，然后调用对应工具
- 不需要工具时：说明推理过程，直接给出答案

请始终展示你的推理过程，这对于用户理解你的决策很重要。"""
```

### 6.2 与 Day 6 ChatBot 的代码差异

| 方面 | Day 6 ChatBot | 路线 B ReAct Agent |
|------|--------------|-------------------|
| System Prompt | "你是一个有用的助手" | 明确要求先推理再行动 |
| 打印 content | 只在最终回答时打印 | **每次响应都打印** content（推理过程） |
| 工具调用循环 | 透明执行 | 每步都显示 Thought |

### 6.3 代码骨架

```python
"""
ReAct Agent — 路线 B：Function Calling + Thought 增强
利用 API 的 tools 参数进行结构化工具调用
通过 System Prompt 引导 LLM 输出显式推理过程
"""
import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from tools import tools_schema, TOOL_FUNCTIONS

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

MAX_ITERATIONS = 10

SYSTEM_PROMPT = """...（按 6.1 的指引编写）"""

def run_react_fc(question: str) -> str:
    """使用 Function Calling 的 ReAct 循环"""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]

    for i in range(MAX_ITERATIONS):
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            tools=tools_schema,
            temperature=0.0,
        )

        assistant_message = response.choices[0].message
        finish_reason = response.choices[0].finish_reason

        # ★ 关键区别：无论是否有 tool_calls，都打印 content（推理过程）
        if assistant_message.content:
            print(f"\n💭 Thought: {assistant_message.content}")

        if finish_reason == "stop":
            return assistant_message.content

        if finish_reason == "tool_calls":
            messages.append(assistant_message)
            for tool_call in assistant_message.tool_calls:
                # TODO: 执行工具函数
                # TODO: 打印 Action 和 Observation
                # TODO: 追加 tool result 到 messages
                pass

    return "（达到最大推理步数，强制终止）"

# TODO: main() 函数，交互循环
```

### 6.4 对比运行效果

同一个问题，路线 B 的输出类似：

```
Question: 今天星期几？北京天气怎么样？

💭 Thought: 用户问了今天星期几和北京天气，我需要先查询当前时间。
🔧 Action: get_current_time()
📋 Observation: {"datetime": "2026-04-10 14:30:00", "weekday": "周五"}

💭 Thought: 知道了今天是周五，接下来查北京天气。
🔧 Action: get_weather(city="北京")
📋 Observation: {"city": "北京", "temperature": "22°C", "condition": "晴", "humidity": "45%"}

💭 Thought: 信息齐全了，整理回答。

✅ 最终回答：今天是周五（2026年4月10日）。北京天气晴，气温22°C，湿度45%。
```

---

## 七、Step 4：路线 A vs B 对比实验（30 分钟）

用相同的问题分别测试两个 Agent，对比它们的表现：

### 7.1 测试用例

| # | 测试问题 | 考察点 |
|---|---------|--------|
| 1 | `你好，你是谁？` | 不需要工具的简单问题 |
| 2 | `现在几点了？` | 单工具调用 |
| 3 | `北京和上海今天天气分别怎么样？` | 同一工具连续调用两次 |
| 4 | `今天星期几？帮我算 (365 * 24) + 12` | 不同工具组合调用 |
| 5 | `先帮我算 100 * 55，再告诉我北京天气，最后告诉我现在几点` | 三工具连续调用，考验推理规划 |
| 6 | `如果北京温度超过25度，帮我算 温度*2，否则算 温度*3` | 条件推理 + 工具链（需要先看天气再决定算什么） |

### 7.2 记录对比

用表格记录每个测试用例两个 Agent 的表现：

| 问题 | 路线 A（Prompt 驱动） | 路线 B（FC 增强） | 谁更好？为什么？ |
|------|---------------------|-------------------|-----------------|
| #1 | | | |
| #2 | | | |
| ... | | | |

重点关注：
- 推理链的清晰度
- 工具调用的准确性
- 格式遵循的一致性
- 路线 A 是否有解析失败的情况

---

## 八、Step 5：里程碑 1 交付物（1 小时）

### 8.1 交付物清单

根据学习计划，第 1 周末需要完成以下交付物：

- [x] **一个可运行的 ReAct 风格 Agent（纯 SDK，无框架）**
  - 路线 A 和 路线 B 各一个实现（至少完成其中一个）
  - 能够：接收自然语言提问 → 推理需要哪个工具 → 调用工具 → 综合结果作答
  
- [ ] **一份个人笔记：LLM vs 传统程序的思维转变总结（500 字以上）**

### 8.2 思维转变总结写作指引

这份笔记是第一周最重要的"软性"交付物。不要流水账式地记录学了什么，而是深入思考这些核心问题：

**维度 1：控制流的变化**
- 传统程序：你写 `if/else/for`，控制流完全确定
- Agent 程序：LLM 决定走哪条路径，你写的是"可能被调用的工具"和"约束规则"
- 反思：你这周在编码时，哪个瞬间最强烈地感受到这种差异？

**维度 2：输入输出的变化**
- 传统程序：结构化输入 → 确定性输出
- Agent 程序：自然语言输入 → 概率性输出
- 反思：这对错误处理、测试策略有什么影响？

**维度 3：调试方式的变化**
- 传统程序：断点、日志、确定的复现路径
- Agent 程序：相同输入可能有不同的推理路径和工具调用顺序
- 反思：路线 A 的 ReAct Agent 中，"打印推理链"是不是一种新的调试手段？

**维度 4：架构思维的变化**
- 传统程序：模块化、封装、接口设计
- Agent 程序：Prompt 设计、工具抽象、推理链设计
- 反思：哪些传统软件工程的技能可以直接迁移？哪些需要"忘掉重来"？

### 8.3 README.md

为 `projects/week1_react_agent/` 写一份 README，至少包含：

```markdown
# Week 1 ReAct Agent

## 项目说明
基于 ReAct 论文思想，用原生 DeepSeek SDK 实现的推理-行动 Agent。

## 两种实现
- `react_prompt.py`：纯 Prompt 驱动，通过文本解析实现 Thought-Action-Observation 循环
- `react_fc.py`：Function Calling + Thought 增强，结合 API 结构化工具调用和显式推理

## 运行方式
（补充具体命令）

## 工具列表
- get_current_time: 查询当前时间
- calculate: 数学计算
- get_weather: 查询天气（模拟数据）
```

---

## 九、延伸思考（完成交付物后如有余力）

### 9.1 ReAct 的进化

ReAct 论文发表于 2022 年 10 月。此后 Agent 领域快速发展，了解这些后续演进能帮你建立全局视野：

| 时间 | 进展 | 与 ReAct 的关系 |
|------|------|-----------------|
| 2022.10 | ReAct 论文 | 奠基之作 |
| 2023.03 | Reflexion 论文 | 在 ReAct 基础上增加"反思"能力，Agent 能从失败中学习 |
| 2023.04 | AutoGPT 爆火 | ReAct 思想 + 自主循环 + 文件/网页工具 |
| 2023.08 | LangChain Agent 重构 | 底层实现从自定义 Agent 全面转向 ReAct 架构 |
| 2024+ | Multi-Agent 框架 | 多个 ReAct Agent 协作，如 CrewAI、AutoGen |

### 9.2 下周预告

下周你将进入**框架学习阶段**，用 LangChain 的 `create_react_agent` 来实现同样的功能。届时你会深刻体会到：

- 你今天手写的所有逻辑（解析 Action、循环执行工具、追加 Observation），框架帮你封装了
- 但正因为你手写过，才能真正理解框架在做什么，出了问题知道去哪里排查

---

## 十、今日总结

| 时间段 | 内容 | 预计耗时 |
|--------|------|---------|
| 上午 | 阅读 ReAct 论文 + 思考练习 | 1.5h |
| | 准备工具模块 | 0.25h |
| | 路线 A：纯 Prompt 驱动 ReAct Agent | 1.5h |
| 下午 | 路线 B：Function Calling 增强 ReAct Agent | 1h |
| | 对比实验 | 0.5h |
| | 里程碑交付物（笔记 + README）| 1h |
| | 延伸思考 | 余力 |
| **合计** | | **~5.75h** |

---

> 🎯 **第 1 周结束了**。你从零开始，经历了 API 调用 → Prompt Engineering → Function Calling → 环境搭建 → ChatBot → ReAct Agent 的完整旅程。下周开始进入框架学习，你会发现今天手写的一切都会在框架中找到对应的抽象。手写经验是理解框架的最佳基础。
