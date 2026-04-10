# Week1 ChatBot

基于原生 OpenAI SDK 实现的命令行多轮对话机器人，支持工具调用。

## 运行方式

```powershell
cd D:\Users\hanqiang.wang\source\repos\Agent
.\.venv\Scripts\Activate.ps1
python projects\week1_chatbot\main.py
```

## 支持的功能

| 工具 | 描述 | 示例 |
|------|------|------|
| `get_current_time` | 查询当前日期、时间和星期 | "现在几点了？" |
| `calculate` | 计算数学表达式（支持 `+-*/` 和括号） | "帮我算 (100 + 200) * 3" |
| `get_weather` | 查询城市天气（模拟数据） | "北京今天天气怎么样？" |

输入 `quit` 退出程序。

## 项目结构

```
week1_chatbot/
├── main.py      # 对话循环 + 工具调度
├── tools.py     # 工具函数定义、tools 列表、TOOL_FUNCTIONS 映射
└── README.md
```

## 实现要点

- **多轮对话**：`messages` 列表贯穿整个会话，不在循环内重置，LLM 可理解上下文
- **工具调用循环**：内层 `while` 循环以 `finish_reason` 为判断条件，支持 LLM 连续调用多个工具
- **安全计算**：`calculate` 使用白名单字符集过滤输入，拒绝执行非法表达式
- **模块化**：新增工具只需修改 `tools.py`，`main.py` 无需改动
