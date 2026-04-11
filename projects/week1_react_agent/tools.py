import json
from datetime import datetime

def get_current_time() -> str:
    now = datetime.now()
    return json.dumps({
        "datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
        "weekday": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][now.weekday()],
    }, ensure_ascii=False)


def calculate(expression: str) -> str:
    allowed = set("0123456789+-*/.() ")
    if not all(c in allowed for c in expression):
        return json.dumps({"error": "不支持的字符，仅允许数字和 +-*/().空格"}, ensure_ascii=False)
    try:
        result = eval(expression)
        return json.dumps({"expression": expression, "result": result}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": f"计算出错: {str(e)}"}, ensure_ascii=False)


def get_weather(city: str) -> str:
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

TOOL_DESCRIPTIONS = """
可用工具:
1. get_current_time: 获取当前日期、时间和星期几。无需参数。
    用法: Action: get_current_time[]
2. calculate: 计算数学表达式。参数为表达式字符串。
    用法: Action: calculate[表达式]
    示例: Action: calculate[(100 + 200) * 3]
3. get_weather: 获取指定城市的天气信息。参数为城市名。
    用法: Action: get_weather[城市名]
    示例: Action: get_weather[北京]
4. finish: 给出最终答案。参数为答案文本。
    用法: Action: finish[最终答案]
"""

tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "获取当前的日期和时间，包括星期几",
            "parameters": {
                "type": "object",
                "properties": {},
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
                        "description": "城市名称，例如: 北京、上海、深圳",
                    }
                },
                "required": ["city"],
            },
        },
    },
]

TOOL_FUNCTIONS = {
    "get_current_time": get_current_time,
    "calculate": calculate,
    "get_weather": get_weather,
}