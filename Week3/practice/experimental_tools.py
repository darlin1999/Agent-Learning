import re
from datetime import datetime

def tool_get_time(format: str = "%Y-%m-%d %H:%M:%S") -> str:
    return datetime.now().strftime(format)

def tool_calculator(expr: str) -> str:
    if not re.fullmatch(r"[\d+\-*/.()\s]+", expr):
        raise ValueError(f"不安全的表达式：{expr}")
    return str(eval(expr))

def tool_word_count(text: str) -> int:
    return len(text.split())

TOOLS = {
    "get_time": tool_get_time,
    "calculator": tool_calculator,
    "word_count": tool_word_count,
}

TOOL_DESCRIPTIONS = [
    {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "获取当前时间，可指定格式化字符串",
            "parameters": {
                "type": "object",
                "properties": {
                    "format": {
                        "type": "string",
                        "description": "时间格式化字符串，如 '%Y-%m-%d %H:%M:%S'",
                    }
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "计算数学表达式，支持加减乘除和括号",
            "parameters": {
                "type": "object",
                "properties": {
                    "expr": {
                        "type": "string",
                        "description": "数学表达式，如 '(3 + 5) * 2'",
                    }
                },
                "required": ["expr"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "word_count",
            "description": "统计文本中的单词数量（按空格分割）",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "需要统计单词数的文本",
                    }
                },
                "required": ["text"],
            },
        },
    },
]
