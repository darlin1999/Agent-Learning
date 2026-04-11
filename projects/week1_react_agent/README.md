# Week 1 ReAct Agent

## 项目说明
基于 ReAct 论文思想，用原生 DeepSeek SDK 实现的推理-行动 Agent。

## 两种实现
- `react_prompt.py`：纯 Prompt 驱动，通过文本解析实现 Thought-Action-Observation 循环
- `react_fc.py`：Function Calling + Thought 增强，结合 API 结构化工具调用和显式推理

## 运行方式
```powershell
cd D:\Users\hanqiang.wang\source\repos\Agent
.\.venv\Scripts\Activate.ps1
python projects\week1_react_agent\react_prompt.py
python projects\week1_react_agent\react_fc.py
```

## 工具列表
- get_current_time: 查询当前时间
- calculate: 数学计算
- get_weather: 查询天气（模拟数据）