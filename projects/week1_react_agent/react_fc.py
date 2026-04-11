import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from tools import tools_schema, TOOL_FUNCTIONS
from colorama import init, Fore

load_dotenv()

init(autoreset=True)

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

MAX_ITERATIONS = 10  # 最大迭代次数，防止无限循环

SYSTEM_PROMPT = """你是一个通过推理和工具调用来回答问题的智能助手。

在每次回复中，请先在回复内容中说明你的思考过程（为什么需要调用这个工具，或者为什么现在可以直接回答），然后再决定是否调用工具。

格式示例：
- 需要工具时：先说明推理过程，然后调用对应工具
- 不需要工具时：说明推理过程，直接给出答案

请始终展示你的推理过程，这对于用户理解你的决策很重要。"""


def run_react(question: str) -> str:
    """执行一次完整的 ReAct 推理循环"""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Question: {question}"},
    ]

    for i in range(MAX_ITERATIONS):
        # 调用 LLM（带 tools 参数）
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            tools=tools_schema,
            temperature=0.0,
        )

        # 无论是否调用工具，打印 LLM 输出（推理过程）
        assistant_message = response.choices[0].message
        content = assistant_message.content
        print(Fore.YELLOW + f"\nThought: {content}")

        # 根据finish_reason判断是否调用工具
        finish_reason = response.choices[0].finish_reason
        if finish_reason not in ["tool_calls", "stop"]:
            print(Fore.RED + f"Finish reason: {finish_reason}")
            return content.strip()

        if finish_reason == "stop":
            # LLM 认为回答完成，直接输出回复
            return content.strip()

        # tool_calls
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
                result = func(**func_args)

            print(Fore.YELLOW + f"🔧 Action: {func_name}({func_args})")
            print(Fore.GREEN + f"📋 Observation: {result}")

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                }
            )

    return "（达到最大推理步数，强制终止）"


def main():
    print(Fore.CYAN + "=" * 40)
    print(Fore.CYAN + "🧠 ReAct Agent(Prompt 驱动)输入 quit 退出")
    print(Fore.CYAN + "=" * 40)

    while True:
        question = input(Fore.GREEN + "\nQuestion: ").strip()
        if question.lower() == "quit":
            print(Fore.CYAN + "再见！👋")
            break
        if not question:
            continue

        answer = run_react(question)
        print(Fore.CYAN + f"\n✅ 最终回答：{answer}")


if __name__ == "__main__":
    main()
