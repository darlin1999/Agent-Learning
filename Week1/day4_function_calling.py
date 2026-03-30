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