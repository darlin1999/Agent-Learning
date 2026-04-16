# Week 3 · Day 18 — LangGraph 入门：Graph、Node、Edge、State 四大核心概念

> **目标**：理解 LangGraph 的核心抽象——Graph、Node、Edge、State，掌握状态机驱动 Agent 的设计思想，动手构建第一个 LangGraph 工作流并理解其相对手写循环的优势。  
> **时间**：1 小时  
> **前置条件**：已完成 Day 15-17（Memory、错误处理、流式输出），熟悉手写 ReAct 循环结构和 LangChain 基础用法（Day 10-11），理解 Agent 循环的 "思考→行动→观察" 模式。

---

## 一、为什么需要 LangGraph？（10 分钟）

回顾我们在 Day 7 手写的 ReAct Agent 和 Day 16 加入的错误处理逻辑——循环里的 `if/elif/else` 分支越来越多，逻辑藏在条件判断的嵌套中，很难一目了然地回答"Agent 当前在哪个步骤""下一步该去哪"。

LangGraph 的核心思想是：**把 Agent 的执行流程建模为一张有向图（Graph），每个步骤是一个节点（Node），步骤之间的转移是边（Edge），所有中间数据统一放在状态（State）里流转。**

### 核心概念

| 概念 | 对应编程概念 | 在 Agent 中的角色 | 要点 |
|------|-------------|-------------------|------|
| **State** | `TypedDict` / `dataclass` | Agent 的全部"工作记忆"——消息历史、中间结果、标志位 | 所有 Node 共享同一份 State，通过读写 State 传递信息 |
| **Node** | 普通 Python 函数 | Agent 的一个"动作步骤"——调用 LLM、执行工具、做判断 | 输入是 State，输出是要更新的 State 字段（字典） |
| **Edge** | 函数调用 / 跳转 | 步骤之间的连线——"做完 A 就做 B" | 分为普通 Edge（无条件跳转）和条件 Edge（根据 State 决定下一步） |
| **Graph** | 状态机 / 工作流引擎 | 把 Node 和 Edge 组装成完整的执行流程 | 编译后得到可执行的 `CompiledGraph`，调用 `.invoke()` 运行 |

> **重要认知转变**：手写 Agent 循环时，**控制流和业务逻辑混在一起**——循环条件、分支判断、错误重试全部写在同一个函数里。LangGraph 把它们分离了：每个 Node 只关心"做什么"，Edge 只关心"下一步去哪"，State 只关心"传递什么数据"。这种分离让复杂 Agent 的流程**可视化、可调试、可复用**。

### 手写循环 vs LangGraph 对比

| 维度 | 手写 `while` 循环 | LangGraph |
|------|-------------------|-----------|
| 流程表达 | 隐含在 `if/elif/else` 中 | 显式的 Node + Edge 图结构 |
| 可视化 | 需要人工画流程图 | 内置 `.get_graph().draw_mermaid()` |
| 状态管理 | 散落在各个变量中 | 统一的 `State` TypedDict |
| 条件路由 | `if condition:` 分支 | `add_conditional_edges()` 清晰声明 |
| 人机协同 | 手动实现断点很复杂 | 内置 `interrupt_before` / `interrupt_after` |
| 持久化 | 需自行实现 | 内置 Checkpointer（可恢复执行） |
| 适用复杂度 | 简单 Agent（3-5 步） | 中大型 Agent（多分支、多条件） |

---

## 二、动手构建第一个 LangGraph 工作流（25 分钟）

### Step 1：安装 LangGraph 并理解最小工作流

先安装依赖，然后构建一个**不涉及 LLM** 的纯逻辑工作流，专注理解 Graph 的运行机制。

```bash
pip install langgraph
```

```python
# Week3/practice/day18_langgraph_intro.py

from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# ========== 第一步：定义 State ==========
# State 就是在整个图中流转的"数据包"
# 所有 Node 共享这份数据，通过读写 State 通信

class GreetingState(TypedDict):
    """最简单的 State：只有两个字段"""
    user_name: str       # 输入：用户名
    greeting: str        # 输出：生成的问候语

# ========== 第二步：定义 Node ==========
# 每个 Node 是一个普通函数
# 输入：当前 State
# 输出：要更新的字段（字典），LangGraph 自动合并到 State

def greet(state: GreetingState) -> dict:
    """Node 1：生成问候语"""
    name = state["user_name"]
    return {"greeting": f"你好，{name}！欢迎学习 LangGraph。"}

# ========== 第三步：构建 Graph ==========
# 把 Node 和 Edge 组装成完整的工作流

workflow = StateGraph(GreetingState)

# 添加节点：名称 → 函数
workflow.add_node("greet", greet)

# 添加边：START → greet → END
workflow.add_edge(START, "greet")
workflow.add_edge("greet", END)

# 编译：得到可执行的 CompiledGraph
app = workflow.compile()

# ========== 第四步：运行 ==========
result = app.invoke({"user_name": "Agent学习者"})
print(result)
# 输出: {'user_name': 'Agent学习者', 'greeting': '你好，Agent学习者！欢迎学习 LangGraph。'}
```

**关键观察**：
- `StateGraph(GreetingState)` 声明了图中流转的数据结构
- `add_node("名称", 函数)` 注册一个步骤
- `add_edge(A, B)` 表示 "A 完成后无条件跳到 B"
- `START` 和 `END` 是内置的特殊节点，标记图的入口和出口
- Node 函数返回的字典会**合并**到 State 中（不是替换整个 State）

### Step 2：多节点 + 条件路由 —— Agent 决策的核心

真实 Agent 需要根据中间结果决定"下一步去哪"。这就是**条件边（Conditional Edge）** 的用武之地。

我们构建一个"数字分类器"工作流：接收一个数字 → 判断奇偶 → 走不同的处理分支。

```python
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END

class NumberState(TypedDict):
    number: int
    category: str    # "odd" 或 "even"
    result: str

def classify(state: NumberState) -> dict:
    """Node: 分类——判断奇偶"""
    category = "even" if state["number"] % 2 == 0 else "odd"
    print(f"  [classify] {state['number']} → {category}")
    return {"category": category}

def handle_even(state: NumberState) -> dict:
    """Node: 处理偶数"""
    result = f"{state['number']} 是偶数，除以 2 得 {state['number'] // 2}"
    print(f"  [handle_even] {result}")
    return {"result": result}

def handle_odd(state: NumberState) -> dict:
    """Node: 处理奇数"""
    result = f"{state['number']} 是奇数，乘以 3 加 1 得 {state['number'] * 3 + 1}"
    print(f"  [handle_odd] {result}")
    return {"result": result}

# --- 路由函数：根据 State 决定下一步 ---
def route_by_category(state: NumberState) -> Literal["handle_even", "handle_odd"]:
    """条件路由：返回下一个 Node 的名称"""
    return "handle_even" if state["category"] == "even" else "handle_odd"

# --- 构建图 ---
workflow = StateGraph(NumberState)

workflow.add_node("classify", classify)
workflow.add_node("handle_even", handle_even)
workflow.add_node("handle_odd", handle_odd)

workflow.add_edge(START, "classify")

# 关键：条件边 —— classify 之后根据 route_by_category 的返回值决定去哪
workflow.add_conditional_edges("classify", route_by_category)

workflow.add_edge("handle_even", END)
workflow.add_edge("handle_odd", END)

app = workflow.compile()

# 测试
print("=== 测试偶数 ===")
r1 = app.invoke({"number": 42})
print(f"  最终结果: {r1['result']}\n")

print("=== 测试奇数 ===")
r2 = app.invoke({"number": 7})
print(f"  最终结果: {r2['result']}")
```

**关键观察**：
- `add_conditional_edges("classify", route_by_category)` 声明了条件路由
- `route_by_category` 函数接收 State，返回下一个 Node 的**名称字符串**
- 类型标注 `Literal["handle_even", "handle_odd"]` 让 LangGraph 知道可能的目标节点
- 这就是 Agent 中"调用工具 vs 直接回答"决策的原型！

---

## 三、用 LangGraph 建模 Agent 循环（15 分钟）

现在把概念应用到真实的 Agent 场景：构建一个简化版的 "LLM 决策 → 工具调用" 循环，用 LangGraph 表达手写 ReAct 循环的等价逻辑（不调用真实 LLM，专注图结构）。

```python
from typing import TypedDict, Literal, Annotated
from langgraph.graph import StateGraph, START, END
import operator

class AgentState(TypedDict):
    """模拟 Agent 的状态"""
    input: str                                            # 用户输入
    messages: Annotated[list[str], operator.add]           # 消息历史（自动追加）
    tool_calls: list[str]                                  # 待调用的工具
    step_count: int                                        # 当前步数
    final_answer: str                                      # 最终答案

def llm_node(state: AgentState) -> dict:
    """
    模拟 LLM 节点：真实场景中这里调用 LLM API
    这里用简单逻辑模拟 LLM 的决策
    """
    step = state.get("step_count", 0) + 1
    user_input = state["input"]

    if step == 1 and "天气" in user_input:
        # 第一步：LLM 决定调用天气工具
        return {
            "messages": [f"[Step {step}] LLM 决定调用天气工具"],
            "tool_calls": ["get_weather"],
            "step_count": step,
        }
    else:
        # 不需要工具 / 工具结果已返回，直接回答
        return {
            "messages": [f"[Step {step}] LLM 生成最终答案"],
            "tool_calls": [],
            "step_count": step,
            "final_answer": f"根据工具结果，回答：关于「{user_input}」的信息已获取。",
        }

def tool_node(state: AgentState) -> dict:
    """
    模拟工具执行节点：真实场景中这里调用工具函数
    """
    tool_name = state["tool_calls"][0] if state["tool_calls"] else "unknown"
    result = f"[工具 {tool_name}] 返回结果：北京今天晴，25°C"
    return {
        "messages": [result],
        "tool_calls": [],  # 清空已处理的工具调用
    }

def should_continue(state: AgentState) -> Literal["tool_node", "__end__"]:
    """
    路由函数：决定是继续调用工具，还是结束
    这就是 ReAct 循环中 "有 action 就执行，否则输出 answer" 的等价表达
    """
    if state.get("tool_calls"):
        return "tool_node"
    return "__end__"

# --- 构建 Agent 图 ---
workflow = StateGraph(AgentState)

workflow.add_node("llm_node", llm_node)
workflow.add_node("tool_node", tool_node)

workflow.add_edge(START, "llm_node")

# LLM 之后：条件路由 —— 有工具调用 → tool_node，无 → 结束
workflow.add_conditional_edges("llm_node", should_continue)

# 工具执行完 → 回到 LLM（形成循环！）
workflow.add_edge("tool_node", "llm_node")

app = workflow.compile()

# 测试 1：需要工具调用的场景
print("=== 场景 1：需要工具调用 ===")
result = app.invoke({
    "input": "北京今天天气怎么样？",
    "messages": [],
    "tool_calls": [],
    "step_count": 0,
    "final_answer": "",
})
print(f"  消息轨迹: {result['messages']}")
print(f"  最终答案: {result['final_answer']}")

print()

# 测试 2：直接回答的场景
print("=== 场景 2：直接回答 ===")
result2 = app.invoke({
    "input": "1+1等于几？",
    "messages": [],
    "tool_calls": [],
    "step_count": 0,
    "final_answer": "",
})
print(f"  消息轨迹: {result2['messages']}")
print(f"  最终答案: {result2['final_answer']}")
```

> **关键发现**：注意 `tool_node` → `llm_node` 这条边形成了**循环**！这正是 ReAct 的 "思考→行动→观察→再思考" 循环。在手写代码中这是 `while True` + `break`，在 LangGraph 中是一条回边 + 条件出口。图结构表达循环比 `while` 更清晰，因为你可以**直接画出来**。

### Annotated 的秘密：State 字段的合并策略

注意上面 `messages` 字段的类型标注：

```python
messages: Annotated[list[str], operator.add]
```

`Annotated[类型, 合并函数]` 告诉 LangGraph：当 Node 返回 `{"messages": ["新消息"]}` 时，不是**替换**原来的 messages，而是用 `operator.add`（列表拼接）追加。这是 LangGraph 管理累积型状态（如消息历史）的关键机制。

| 合并策略 | 写法 | 效果 |
|---------|------|------|
| **替换**（默认） | `field: str` | Node 返回的值直接覆盖原值 |
| **追加** | `Annotated[list, operator.add]` | Node 返回的列表追加到原列表末尾 |
| **自定义** | `Annotated[T, custom_func]` | 用自定义函数合并旧值和新值 |

---

## 四、关键要点总结

| # | 要点 | 说明 |
|---|------|------|
| 1 | **State 是 Agent 的"共享黑板"** | 所有 Node 通过读写 State 通信，不直接传参。用 `TypedDict` 定义，字段类型清晰 |
| 2 | **Node 只返回要更新的字段** | Node 不需要返回完整 State，只需返回有变化的字段，LangGraph 自动合并 |
| 3 | **条件边是 Agent 决策的核心** | `add_conditional_edges()` 把 `if/elif` 抽取为独立的路由函数，流程更清晰 |
| 4 | **`Annotated` 控制合并策略** | 累积型字段（如消息历史）用 `Annotated[list, operator.add]` 实现自动追加 |
| 5 | **图可以有循环** | `tool_node → llm_node` 的回边 + 条件出口 = ReAct 循环的图结构表达 |

---

## 五、自检清单

- [ ] 已成功安装 `langgraph`（`pip install langgraph` 无报错）
- [ ] Step 1 的 `GreetingState` 工作流运行后输出了包含 `greeting` 字段的字典
- [ ] Step 2 的条件路由工作流对偶数和奇数分别走了不同的处理分支（观察到 `[handle_even]` 或 `[handle_odd]` 的打印）
- [ ] 第三节的模拟 Agent 循环中，场景 1（天气查询）经历了 `llm_node → tool_node → llm_node` 三步，场景 2 只经历了 `llm_node` 一步

---

## 六、笔记区

> 学完本节后，用自己的话回答以下问题，加深理解。

### Q1: LangGraph 中 State、Node、Edge 三者的关系是什么？为什么 Node 只需要返回"要更新的字段"而不是完整 State？

### Q2: 条件边 `add_conditional_edges()` 的路由函数和手写 `if/elif` 在功能上是等价的，那 LangGraph 的优势究竟体现在哪里？什么规模的 Agent 适合从手写循环切换到 LangGraph？

### Q3: `Annotated[list[str], operator.add]` 解决了什么问题？如果不用 `Annotated`，多个 Node 都往 `messages` 字段写入时会发生什么？

### Q4: 在第三节的模拟 Agent 图中，`tool_node → llm_node` 形成了循环。如果没有 `should_continue` 中的 `__end__` 出口，会发生什么？这和 Day 16 讲的哪个问题相关？

---

## 七、明日预告

> 明天将学习 **LangGraph 实践**——用 LangGraph 实现一个真正调用 LLM 的 ReAct 状态机 Agent，对比 Day 7 手写 `while` 循环的实现，体会 LangGraph 在实际 Agent 开发中的工程效率差异。建议提前回顾：Day 7 的 ReAct Agent 代码结构，以及 LangChain 的 `ChatOpenAI` 和 Tool 用法。