# Week 1 · Day 5 — 环境搭建与项目规范化：为周末实战做好工程准备

> **目标**：回顾并规范化本周已搭建的开发环境，补齐虚拟环境、`requirements.txt`、`anthropic` SDK 等缺失项，建立正式的项目目录结构，确保周六的 ChatBot 综合实践零阻力启动。  
> **时间**：1 小时  
> **前置条件**：已完成 Day 2-4，拥有可用的 DeepSeek API Key，Python 环境已安装 `openai` 和 `python-dotenv`。

---

## 零、本日定位说明

> 你可能注意到，"环境搭建"这件事在 Day 2-4 已经**逐步完成了大半**：
> - Day 2：注册了 DeepSeek API，拿到 API Key，安装了 Postman
> - Day 3：安装了 `openai`、`python-dotenv`，创建了 `.env` 文件
> - Day 4：用 Python 成功跑通了 Function Calling 完整流程
>
> 所以今天不是"从零搭环境"，而是**回顾、补齐、规范化**——把"能跑"升级为"工程可维护"，同时为明天的 ChatBot 综合实践建立清晰的项目骨架。

---

## 一、环境现状盘点（5 分钟）

先确认目前已有什么、还缺什么：

| 项目 | 当前状态 | 今日操作 |
|------|---------|---------|
| Python 3.x | ✅ 已安装 | 确认版本 |
| `openai` SDK | ✅ 已安装 | 确认版本 |
| `python-dotenv` | ✅ 已安装 | 确认版本 |
| `.env` 文件 | ✅ 已创建（含 `DEEPSEEK_API_KEY`） | 检查并补充 |
| `.gitignore` | ✅ 已配置 | 检查是否覆盖完整 |
| 虚拟环境（venv） | ❌ 未使用 | **今日创建** |
| `requirements.txt` | ❌ 不存在 | **今日创建** |
| `anthropic` SDK | ❌ 未安装 | **今日安装** |
| 正式项目目录结构 | ❌ 文件散放在 Week1/ | **今日规划** |

### 确认当前环境的命令

```powershell
python --version
pip show openai python-dotenv
```

记录输出的版本号，后续写入 `requirements.txt`。

---

## 二、创建虚拟环境（10 分钟）

### 为什么需要虚拟环境？

| 场景 | 不用 venv | 用 venv |
|------|----------|---------|
| 装包 | 装到全局 Python，所有项目共享 | 装到项目独立目录，互不影响 |
| 依赖冲突 | 项目 A 要 `openai==1.0`，项目 B 要 `openai==2.0` → 冲突 | 各自独立，不冲突 |
| 复现环境 | "我电脑上能跑"综合症 | `pip install -r requirements.txt` 一键复现 |
| 清理 | 卸载时不知道哪些是哪个项目装的 | 删掉 `.venv` 文件夹即可 |

> **类比**：虚拟环境就像 Docker 容器的极简版——隔离依赖，保证项目间互不污染。

### Step 1：创建虚拟环境

在项目根目录执行：

```powershell
cd D:\Users\hanqiang.wang\source\repos\Agent
python -m venv .venv
```

这会在项目根目录创建 `.venv` 文件夹（已被 `.gitignore` 排除，不会提交到 Git）。

### Step 2：激活虚拟环境

```powershell
.\.venv\Scripts\Activate.ps1
```

激活后，终端提示符前面会出现 `(.venv)`，表示当前处于虚拟环境中：

```
(.venv) PS D:\Users\hanqiang.wang\source\repos\Agent>
```

> **注意**：如果遇到 "无法加载文件，因为在此系统上禁止运行脚本" 的错误，说明 Day 2 的执行策略设置未生效，重新执行：
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
> ```

### Step 3：在虚拟环境中安装依赖

激活 venv 后，之前全局安装的包不再可用，需要重新安装：

```powershell
pip install openai python-dotenv anthropic
```

### Step 4：验证安装

```powershell
pip list
```

确认输出中包含 `openai`、`python-dotenv`、`anthropic` 三个包。

---

## 三、创建 `requirements.txt`（5 分钟）

### 方法 A：自动生成（推荐）

```powershell
pip freeze > requirements.txt
```

这会把当前 venv 中所有已安装的包及其精确版本号导出。

### 方法 B：手动维护精简版

如果你希望 `requirements.txt` 只保留直接依赖（不含间接依赖），可以手动创建：

```
openai>=1.0
anthropic>=0.20
python-dotenv>=1.0
```

> **推荐做法**：两种方式都用。日常用方法 B 维护一份精简的 `requirements.txt`，部署时用 `pip freeze > requirements-lock.txt` 生成锁定版本（类似 npm 的 `package-lock.json`）。
>
> 本阶段学习为主，用方法 A 即可，不必过度工程化。

### 验证：从零复现环境

如果将来换电脑或分享给别人，只需要：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## 四、认识 `anthropic` SDK（10 分钟）

### 为什么要装 `anthropic`？

学习计划中会接触多家 LLM 提供商。提前安装 Anthropic SDK，了解不同 SDK 的接口差异，有助于后续快速切换模型。

| 对比项 | OpenAI SDK（DeepSeek 共用） | Anthropic SDK |
|--------|---------------------------|---------------|
| 安装包 | `openai` | `anthropic` |
| 调用风格 | `client.chat.completions.create()` | `client.messages.create()` |
| 消息格式 | `messages` 包含 `system` 角色 | `system` 是独立参数，不在 `messages` 中 |
| Tool Use | `tools` + `tool_calls` | `tools` + `tool_use` content block |

### 快速对比：同样的任务，两种 SDK 写法

**OpenAI SDK（你已经熟悉的）**：
```python
from openai import OpenAI

client = OpenAI(api_key="...", base_url="https://api.deepseek.com")
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "你是一个助手。"},
        {"role": "user", "content": "你好"},
    ],
)
print(response.choices[0].message.content)
```

**Anthropic SDK（了解即可，暂时不需要 API Key）**：
```python
from anthropic import Anthropic

client = Anthropic(api_key="...")
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system="你是一个助手。",            # system 是独立参数
    messages=[
        {"role": "user", "content": "你好"},
    ],
)
print(response.content[0].text)         # 取值路径不同
```

### 关键差异总结

| 差异点 | 影响 | 应对方式 |
|--------|------|---------|
| `system` 放置位置不同 | 切换模型时需要调整代码 | 封装一层统一接口（第 2 周会用 LangChain 自动处理） |
| 响应取值路径不同 | `.choices[0].message.content` vs `.content[0].text` | 同上 |
| Tool Use 字段名不同 | `tool_calls` vs `tool_use` | 理解概念相同，只是 API 表面差异 |

> **今日不需要**注册 Anthropic 账号或获取 API Key。安装 SDK 并了解接口差异即可。后续如果需要用 Claude，再注册不迟。

---

## 五、规划项目目录结构（10 分钟）

当前文件散放在 `Week1/` 中，周六要写一个带工具调用的 ChatBot，需要更清晰的结构。

### 推荐的目录结构

```
Agent/                              ← 项目根目录
├── .env                            ← API Keys（已有，Git 忽略）
├── .gitignore                      ← 忽略规则（已有）
├── .venv/                          ← 虚拟环境（今日创建，Git 忽略）
├── requirements.txt                ← 依赖清单（今日创建）
│
├── Learning Plan/                  ← 学习计划（已有）
│   └── 转型计划_...md
│
├── Week1/                          ← 第 1 周学习资料
│   ├── Day2_API入门.md
│   ├── Day3_Prompt_Engineering基础.md
│   ├── Day4_Function_Calling.md
│   ├── Day5_环境搭建与项目规范化.md  ← 今日文档
│   ├── day3_prompt_experiments.py
│   └── day4_function_calling.py
│
└── projects/                       ← 实战项目（今日创建）
    └── week1_chatbot/              ← 周六 ChatBot 项目
        ├── main.py                 ← 入口文件（周六编写）
        ├── tools.py                ← 工具函数定义（周六编写）
        └── README.md               ← 项目说明（周六编写）
```

### 创建目录

```powershell
cd D:\Users\hanqiang.wang\source\repos\Agent
New-Item -ItemType Directory -Path "projects\week1_chatbot" -Force
```

> **设计思路**：
> - `Week1/` 放学习笔记和实验脚本（按日期组织，侧重学习过程）
> - `projects/` 放独立项目（按功能组织，侧重工程实践）
> - 这种分离让学习资料和实战代码各归其位，互不干扰

---

## 六、`.env` 文件检查与规范化（5 分钟）

### 检查现有 `.env`

打开 `Week1/.env`，确认内容：

```
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxx
```

### 问题：`.env` 放在哪里？

当前 `.env` 在 `Week1/` 目录下。但 `projects/week1_chatbot/` 也需要读取 API Key。有两种方案：

| 方案 | 做法 | 优缺点 |
|------|------|--------|
| **A：根目录统一放** | 把 `.env` 移到项目根目录 `Agent/.env` | ✅ 一处管理所有 Key<br>⚠️ 需要在代码中指定 `.env` 路径 |
| **B：每个目录各放一份** | 每个子目录放自己的 `.env` | ✅ 代码不需要指定路径<br>❌ Key 分散，改一个要改多处 |

**推荐方案 A**：将 `.env` 统一放在项目根目录。

### 操作步骤

1. 将 `Week1/.env` 移动到项目根目录（如果已经存在则跳过这一步）：

```powershell
cd D:\Users\hanqiang.wang\source\repos\Agent

# 检查根目录是否已有 .env
Test-Path .\.env

# 如果根目录没有 .env，从 Week1 复制过来
# Copy-Item .\Week1\.env .\.env
```

2. 修改代码中的 `load_dotenv()` 调用，确保能找到根目录的 `.env`：

```python
from dotenv import load_dotenv
from pathlib import Path

# 向上查找 .env 文件（dotenv 默认行为就是从当前目录逐级向上搜索）
load_dotenv()
```

> `python-dotenv` 的 `load_dotenv()` 默认会从**当前工作目录**开始查找 `.env`。只要你从项目根目录运行脚本（VS Code 默认行为），就能自动找到。如果从子目录运行，可以显式指定路径：
> ```python
> load_dotenv(Path(__file__).resolve().parent.parent / ".env")
> ```

### 补充 `.env` 内容（预留字段）

```
# DeepSeek API（已有）
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxx

# Anthropic API（预留，暂不需要填）
# ANTHROPIC_API_KEY=sk-ant-xxxxxxxx

# OpenAI API（预留，暂不需要填）
# OPENAI_API_KEY=sk-xxxxxxxx
```

注释掉的行不会被 `load_dotenv` 加载，仅作为备忘。

---

## 七、环境健康检查（10 分钟）

完成上述所有步骤后，运行以下检查脚本确认一切就绪。

### 创建检查脚本

在 `Week1/` 下新建 `day5_env_check.py`：

```python
"""
Day 5 环境健康检查
确认所有依赖和配置均已就绪，为周六实践做准备。
"""
import sys
import os


def check(name: str, condition: bool, detail: str = ""):
    status = "✅" if condition else "❌"
    msg = f"  {status} {name}"
    if detail:
        msg += f"  →  {detail}"
    print(msg)
    return condition


print("=" * 50)
print("Day 5 环境健康检查")
print("=" * 50)

all_ok = True

# 1. Python 版本
v = sys.version_info
all_ok &= check("Python 版本", v >= (3, 9), f"{v.major}.{v.minor}.{v.micro}")

# 2. 虚拟环境
in_venv = sys.prefix != sys.base_prefix
all_ok &= check("虚拟环境已激活", in_venv, sys.prefix if in_venv else "未检测到 venv")

# 3. openai SDK
try:
    import openai
    all_ok &= check("openai SDK", True, openai.__version__)
except ImportError:
    all_ok &= check("openai SDK", False, "未安装，请执行 pip install openai")

# 4. anthropic SDK
try:
    import anthropic
    all_ok &= check("anthropic SDK", True, anthropic.__version__)
except ImportError:
    all_ok &= check("anthropic SDK", False, "未安装，请执行 pip install anthropic")

# 5. python-dotenv
try:
    import dotenv
    all_ok &= check("python-dotenv", True, dotenv.__version__)
except ImportError:
    all_ok &= check("python-dotenv", False, "未安装，请执行 pip install python-dotenv")

# 6. .env 文件存在
from dotenv import load_dotenv
load_dotenv()
env_exists = os.getenv("DEEPSEEK_API_KEY") is not None
all_ok &= check(".env 中 DEEPSEEK_API_KEY", env_exists,
                 "已配置" if env_exists else "未找到，请检查 .env 文件位置")

# 7. API 可用性（实际调用一次）
if env_exists:
    try:
        from openai import OpenAI
        client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com",
        )
        resp = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": "回复OK"}],
            max_tokens=5,
        )
        got_reply = resp.choices[0].message.content is not None
        all_ok &= check("DeepSeek API 连通性", got_reply, "调用成功")
    except Exception as e:
        all_ok &= check("DeepSeek API 连通性", False, str(e))

# 8. 项目目录
proj_dir = os.path.join(os.path.dirname(__file__), "..", "projects", "week1_chatbot")
all_ok &= check("projects/week1_chatbot/ 目录", os.path.isdir(proj_dir), "已创建")

# 9. requirements.txt
req_file = os.path.join(os.path.dirname(__file__), "..", "requirements.txt")
all_ok &= check("requirements.txt", os.path.isfile(req_file), "已创建")

print("\n" + "=" * 50)
if all_ok:
    print("🎉 全部通过！环境已就绪，周六可以直接开始写 ChatBot。")
else:
    print("⚠️  部分检查未通过，请根据上方提示修复后重新运行此脚本。")
print("=" * 50)
```

### 运行检查

```powershell
cd D:\Users\hanqiang.wang\source\repos\Agent
.\.venv\Scripts\Activate.ps1
python Week1\day5_env_check.py
```

### 预期输出（全部通过）

```
==================================================
Day 5 环境健康检查
==================================================
  ✅ Python 版本  →  3.13.x
  ✅ 虚拟环境已激活  →  D:\...\Agent\.venv
  ✅ openai SDK  →  1.x.x
  ✅ anthropic SDK  →  0.x.x
  ✅ python-dotenv  →  1.x.x
  ✅ .env 中 DEEPSEEK_API_KEY  →  已配置
  ✅ DeepSeek API 连通性  →  调用成功
  ✅ projects/week1_chatbot/ 目录  →  已创建
  ✅ requirements.txt  →  已创建

==================================================
🎉 全部通过！环境已就绪，周六可以直接开始写 ChatBot。
==================================================
```

> 如果有 ❌ 项，按提示修复后重新运行，直到全部 ✅。

---

## 八、VS Code 配置优化（5 分钟）

### 8.1 选择 Python 解释器

VS Code 需要知道使用 venv 中的 Python，而不是全局 Python：

1. 按 `Ctrl + Shift + P`，输入 `Python: Select Interpreter`
2. 选择 `.\.venv\Scripts\python.exe`（列表中通常标注为 "('.venv': venv)"）

设置后，VS Code 的终端、代码提示、调试器都会使用 venv 中的解释器和包。

### 8.2 推荐的 VS Code 扩展

如果尚未安装，建议安装以下扩展提升开发效率：

| 扩展 | 用途 |
|------|------|
| **Python**（Microsoft） | Python 语言支持、调试、代码提示 |
| **Pylance**（Microsoft） | 更强大的类型推断和自动补全 |
| **GitHub Copilot** | AI 辅助编程（你已经在用了） |

---

## 九、本周知识回顾与整理（剩余时间）

趁环境搭建的空隙，快速回顾本周学到的核心概念：

| Day | 核心概念 | 一句话总结 |
|-----|---------|-----------|
| Day 1 | LLM 基础 | LLM 是基于概率的文本生成器，Token 是最小处理单位，Temperature 控制随机性 |
| Day 2 | API 调用 | LLM 通过 HTTP API 交互，核心参数是 `messages`（对话历史）和 `model` |
| Day 3 | Prompt Engineering | Zero-shot 靠描述精度，Few-shot 靠示例示范，CoT 靠引导推理，三者可叠加 |
| Day 4 | Function Calling | LLM 是"路由器"不是"执行器"，通过 `tools` 参数声明能力，LLM 自主决策调用 |
| Day 5 | 工程规范 | venv 隔离依赖，`requirements.txt` 锁定版本，`.env` 管理密钥，项目结构清晰 |

### 为周六做的准备清单

明天（周六）要用 3 小时实现一个带工具调用的 ChatBot，确保以下条件已满足：

- [ ] 虚拟环境创建并激活
- [ ] `openai`、`python-dotenv`、`anthropic` 已安装
- [ ] `requirements.txt` 已生成
- [ ] `.env` 中 `DEEPSEEK_API_KEY` 可访问
- [ ] `projects/week1_chatbot/` 目录已创建
- [ ] `day5_env_check.py` 全部 ✅ 通过
- [ ] VS Code 已选择 venv 解释器

---

## 十、关键规律总结

| # | 规律 | 说明 |
|---|------|------|
| 1 | **venv 是 Python 项目的标配** | 不用 venv 的项目迟早会遇到依赖冲突，这是低成本高回报的最佳实践 |
| 2 | **密钥永远不进代码** | `.env` + `.gitignore` 是最低成本的密钥管理方案，生产环境用 Vault/Secret Manager |
| 3 | **`requirements.txt` 是可复现的基础** | 没有依赖清单的项目，换台电脑就可能跑不起来 |
| 4 | **不同 SDK 接口不同，概念相同** | OpenAI 和 Anthropic 的 API 表面不同，但 messages/tools/streaming 的概念一致 |
| 5 | **项目结构越早规范越好** | 文件散放的"原型代码"很快就会变成"技术债" |

---

## 十一、今日笔记模板

```
日期：2026/03/30
核心理解：
  - 虚拟环境的作用：隔离项目依赖，避免全局污染，实现环境可复现
  - requirements.txt 的作用：记录项目依赖，一条命令即可在新环境中还原
  - OpenAI SDK vs Anthropic SDK 的主要差异：
    1. system prompt 放置位置不同（messages 内 vs 独立参数）
    2. 响应取值路径不同（choices[0].message.content vs content[0].text）
    3. Tool Use 字段名不同（tool_calls vs tool_use）
  - .env 文件应放在项目根目录，统一管理所有 API Key
环境状态：day5_env_check.py 检查结果全部 ✅
明日重点：用原生 SDK 实现带工具调用的 ChatBot（查时间 + 计算器），3 小时
```

---

## 十二、明日预告（周六 · 3 小时实践）

**综合实践**：用原生 SDK（不借助框架）实现一个带工具调用的简单 ChatBot：
- 支持多轮对话（用户可以连续提问）
- 集成工具：查询当前时间、计算器
- 实现完整的 Function Calling 循环
- 在 Day 4 单次调用的基础上，升级为交互式对话循环

> 这是本周的核心交付物之一，所有 Day 1-5 学到的知识都会用上。
