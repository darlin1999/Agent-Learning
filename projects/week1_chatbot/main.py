import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from tools import tools, TOOL_FUNCTIONS
from colorama import init, Fore

load_dotenv()


client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)


def get_assistant_reply(messages):
    while True:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            tools=tools,
            temperature=0.0,
        )

        assistant_message = response.choices[0].message
        finish_reason = response.choices[0].finish_reason

        if finish_reason == "tool_calls":
            # LLM 认为需要调用工具，处理工具调用
            messages.append(assistant_message)
            tool_calls = response.choices[0].message.tool_calls
            for tool_call in tool_calls:
                func_name = tool_call.function.name
                func_args = json.loads(tool_call.function.arguments)
                func = TOOL_FUNCTIONS.get(func_name)
                if func is None:
                    result = json.dumps(
                        {"error": f"未知工具: {func_name}"}, ensure_ascii=False
                    )
                else:
                    print(Fore.YELLOW + f"执行工具: {func_name}，参数: {func_args}")
                    result = func(**func_args)

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result,
                    }
                )

        if finish_reason == "stop":
            # LLM 认为回答完成，直接输出回复
            return assistant_message

        if finish_reason not in ["tool_calls", "stop"]:
            # 其他 finish_reason，直接返回当前消息（可能包含部分回复）
            return assistant_message


def chat_loop():
    """主对话循环"""
    init(autoreset=True)
    messages = [
        {
            "role": "system",
            "content": "你是一个有用的助手，可以查询时间、计算数学表达式、查询天气，也可以与用户进行常规对话。请根据用户问题判断是否需要使用工具。",
        }
    ]

    print("=" * 40)
    print("🤖 Week1 ChatBot（输入 quit 退出）")
    print("=" * 40)

    while True:
        user_input = input(Fore.GREEN + "\nYou: ")
        if user_input.strip().lower() == "quit":
            print(Fore.CYAN + "ChatBot: Bye~")
            break
        if not user_input.strip():
            continue

        messages.append({"role": "user", "content": user_input})
        assistant_message = get_assistant_reply(messages)
        print(Fore.CYAN + f"ChatBot: {assistant_message.content}")
        messages.append(assistant_message)


if __name__ == "__main__":
    chat_loop()
