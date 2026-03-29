# Week 1 · Day 3 — Prompt Engineering 基础

> **目标**：掌握 Zero-shot、Few-shot、Chain of Thought 三种核心 Prompting 技术，通过动手实验亲身感受不同 Prompt 写法对 LLM 输出的影响。  
> **时间**：1 小时  
> **前置条件**：已完成 Day 2，拥有可用的 DeepSeek API Key，能通过 Postman 或 Python 发出 API 请求。

---

## 一、核心概念速览（10 分钟）

Prompt Engineering 本质上是**通过精心设计输入来控制 LLM 输出**。LLM 没有"设置"功能键，你传入什么，它就在此基础上预测接下来最可能的文字。因此，Prompt 的每一个字都是"指令"。

### 三大基础技术对比

| 技术 | 原理 | 适用场景 |
|------|------|---------|
| **Zero-shot** | 直接描述任务，不给任何示例 | 任务描述清晰、模型本身知识足够时 |
| **Few-shot** | 在 Prompt 中先给 1-5 个输入→输出示例 | 需要特定格式/风格/规范时 |
| **Chain of Thought (CoT)** | 要求模型"逐步推理"，附加 *"Let's think step by step"* 或直接给出推理示例 | 数学、逻辑推理、多步骤问题 |

---

## 二、实验环境准备（5 分钟）

本节开始使用 Python 脚本进行实验，比 Postman 更高效地批量测试 Prompt。

### 安装依赖（如尚未安装）

```powershell
pip install openai python-dotenv
```

### 创建实验脚本框架

在 `Week1/` 目录下新建文件 `day3_prompt_experiments.py`，粘贴以下基础代码：

```python
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
```

> **关于 `.env` 文件**：在 `Week1/` 目录下创建 `.env` 文件，内容为：
> ```
> DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxx
> ```
> 将 `sk-xxx` 替换为你的真实 Key。`.env` 文件不要提交到 Git（加入 `.gitignore`）。

---

## 三、实验 1：Zero-shot Prompting（10 分钟）

零样本提示——不给任何示例，直接告诉模型做什么。

### 核心观察：描述精度影响输出质量

在 `day3_prompt_experiments.py` 末尾追加以下代码并运行：

```python
# ── 实验 1：Zero-shot ──────────────────────────────────────

# 1a：模糊指令
experiment(
    title="1a - Zero-shot（模糊）",
    system="你是一个助手。",
    user="分析一下苹果公司。",
)

# 1b：精确指令
experiment(
    title="1b - Zero-shot（精确）",
    system="你是一位简洁的商业分析师，只输出要点，不写废话。",
    user=(
        "用 3 个要点分析苹果公司 2024 年的核心竞争优势，"
        "每个要点不超过 30 字，用数字编号列出。"
    ),
)
```

**运行方式**：
```powershell
cd d:\Users\hanqiang.wang\source\repos\Agent\Week1
python day3_prompt_experiments.py
```

**预期观察**：
- `1a` 输出冗长、结构不一，可能写好几段通用介绍
- `1b` 输出简洁、格式固定，符合预期

**关键结论**：Zero-shot 的核心是**角色定义 + 格式约束 + 任务精确描述**，三者缺一不可。

---

## 四、实验 2：Few-shot Prompting（15 分钟）

少量样本提示——在 Prompt 里给出输入/输出示例，让模型学习期望的格式和风格。

### Few-shot 的两种写法

**写法 A：将示例嵌入 user 消息**（简单场景）

**写法 B：用 `assistant` 消息展示历史对话**（更自然，模型理解更稳定，推荐）

追加以下代码：

```python
# ── 实验 2：Few-shot ──────────────────────────────────────

# 2a：无示例（Zero-shot 对照组）
experiment(
    title="2a - 情感分析：Zero-shot（对照）",
    system="判断用户评论的情感倾向。",
    user="这款耳机戴久了耳朵疼，低音也不够劲，性价比感觉不高。",
)

# 2b：Few-shot，写法 B（多轮消息注入示例）
def chat_fewshot(examples: list[dict], user_prompt: str) -> str:
    """
    examples 格式：[{"user": "...", "assistant": "..."}, ...]
    """
    messages = [
        {"role": "system", "content": (
            "你是情感分析专家。对每条用户评论，"
            "输出格式严格为：\n情感：正面/负面/中性\n理由：一句话（15字以内）"
        )},
    ]
    # 注入 few-shot 示例
    for ex in examples:
        messages.append({"role": "user",      "content": ex["user"]})
        messages.append({"role": "assistant", "content": ex["assistant"]})
    # 最后追加真实问题
    messages.append({"role": "user", "content": user_prompt})

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        temperature=0.0,   # 分类任务设为 0，确保输出稳定
        max_tokens=64,
    )
    return response.choices[0].message.content


examples = [
    {
        "user": "物流超快，包装完好，手机颜色比图片更好看！",
        "assistant": "情感：正面\n理由：物流、包装、外观均满意",
    },
    {
        "user": "充电速度很慢，两个小时没充满，太失望了。",
        "assistant": "情感：负面\n理由：充电速度不达预期",
    },
    {
        "user": "东西收到了，和描述基本一致，没什么特别的。",
        "assistant": "情感：中性\n理由：符合描述但无亮点",
    },
]

test_review = "这款耳机戴久了耳朵疼，低音也不够劲，性价比感觉不高。"
print(f"\n{'='*60}")
print("实验：2b - 情感分析：Few-shot（3 个示例）")
print(f"{'='*60}")
print(f"[User]   {test_review}")
print("[输出]")
print(chat_fewshot(examples, test_review))
```

**预期观察**：
- `2a` 可能返回自由格式的句子，格式不稳定
- `2b` 严格按照 `情感：xxx\n理由：xxx` 格式输出，可直接解析

**关键结论**：Few-shot 最适合需要**固定输出格式**的任务（分类、抽取、翻译风格统一等）。示例数量 3-5 个通常足够，太多反而增加成本。

---

## 五、实验 3：Chain of Thought（CoT）（15 分钟）

链式思维——让模型"思考过程可见"，显著提升复杂推理的准确性。

### 为什么 CoT 有效？

LLM 是自回归模型，生成每个 Token 时只参考已生成的内容。当模型把推理步骤"写出来"之后，后续 Token 的生成就能参考这些中间步骤，等效于给模型提供了"草稿纸"。

### 触发 CoT 的两种方式

| 方式 | 写法 | 适用情况 |
|------|------|---------|
| **Zero-shot CoT** | 在 Prompt 末尾加 `"请逐步推理，然后给出最终答案。"` | 快速测试，无需示例 |
| **Few-shot CoT** | 示例中包含完整推理过程 | 对准确性要求高的场景 |

追加以下代码：

```python
# ── 实验 3：Chain of Thought ──────────────────────────────

SYSTEM_BASE = "你是一个严谨的逻辑推理助手。"

PROBLEM = (
    "一家工厂有三条流水线 A、B、C。"
    "A 每小时生产 120 件，B 每小时生产 80 件，C 每小时生产 60 件。"
    "工厂运行 8 小时后，因维修 A 停工 2 小时。"
    "请问 8 小时内工厂共生产多少件产品？"
)

# 3a：直接要答案（无 CoT）
experiment(
    title="3a - 无 CoT（直接要答案）",
    system=SYSTEM_BASE,
    user=PROBLEM + "\n\n直接给出最终数字。",
    temperature=0.0,
)

# 3b：Zero-shot CoT
experiment(
    title="3b - Zero-shot CoT",
    system=SYSTEM_BASE,
    user=PROBLEM + "\n\n请逐步推理，写出每一步计算过程，最后给出答案。",
    temperature=0.0,
)

# 3c：Few-shot CoT（提供一个带推理过程的示例）
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
```

**正确答案**：
- A 正常 8 小时 = 120×8 = 960；但 A 停工 2 小时，所以 A 实产 = 120×6 = 720
- B 全程 = 80×8 = 640
- C 全程 = 60×8 = 480
- **合计 = 720 + 640 + 480 = 1840 件**

**预期观察**：
- `3a` 很可能得到错误答案（忽略停工细节）
- `3b` / `3c` 因为展开了推理步骤，正确率显著更高

---

## 六、关键规律总结（5 分钟回顾）

运行完三组实验后，对照以下规律验证自己的观察：

| # | 规律 | 实验依据 |
|---|------|---------|
| 1 | **格式约束优先于内容约束**：想要固定格式，必须在 Prompt 中明确写出，否则模型自由发挥 | 实验 1a vs 1b |
| 2 | **角色设定影响语气和详细程度**：`"简洁的商业分析师"` 比 `"你是一个助手"` 产出更聚焦的内容 | 实验 1a vs 1b |
| 3 | **Few-shot 是格式的最佳锚点**：与其写 100 字描述输出格式，不如给 3 个示例 | 实验 2a vs 2b |
| 4 | **CoT 是推理准确性的关键**：对于多步骤问题，不让模型"想"，就不能期望它"算对" | 实验 3a vs 3b/3c |
| 5 | **Temperature 与任务类型强相关**：分类/计算用 `temperature=0`；创意写作用 `0.7~1.0` | 实验 2b、3a-3c |

---

## 七、自选挑战（剩余时间）

完成以上实验后，可尝试以下进阶练习巩固理解：

**挑战 A（简单）**：修改实验 2b 的示例数量，分别测试 1 个、2 个、5 个示例时格式稳定性的差异。

**挑战 B（中等）**：设计一个 Few-shot Prompt，让模型把一段口语化中文改写成正式商务邮件风格，要求输出只包含改写后的内容，不含任何解释。

**挑战 C（进阶）**：结合 Zero-shot CoT，让模型分析一段 Python 代码是否存在潜在的 Bug，并逐步说明推理依据。

---

## 八、今日笔记模板

> 完成实验后，用以下模板记录观察，为后续学习建立个人知识库。

```
日期：____
实验结论：
  - Zero-shot 最关键的要素：
  - Few-shot 何时必要：
  - CoT 触发方式建议：
让我感到意外的发现：
遗留问题（明天查）：
```

---

## 九、明日预告（Day 4）

**Function Calling / Tool Use**：理解 LLM 如何通过 `tools` 参数调用外部函数，为周六的 ChatBot 实践做准备。核心内容：`tools` 参数结构、`tool_calls` 响应解析、工具执行结果回传流程。
