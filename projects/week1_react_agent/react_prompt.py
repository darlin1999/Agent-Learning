import os
import re
from openai import OpenAI
from dotenv import load_dotenv
from tools import TOOL_DESCRIPTIONS, TOOL_FUNCTIONS

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

MAX_ITERATIONS = 10  # 最大迭代次数，防止无限循环

SYSTEM_PROMPT = f"""
你是一个智能助手，通过交替进行"思考"和"行动"来回答用户的问题。

你可以使用以下工具：
{TOOL_DESCRIPTIONS}

你必须严格按照以下格式逐步输出：

Thought: <你的推理过程，分析当前需要做什么>
Action: <工具名>[<参数>]

然后你会收到：
Observation: <工具执行的结果>

你可以重复 Thought/Action/Observation 循环多次。当你得到了足够的信息来回答用户问题时，使用：

Thought: 我现在可以回答了
Action: finish[<你的最终回答>]

重要规则：
1. 每次只输出一个 Thought 和一个 Action, 然后停下来等待 Observation
2. 不要自行编造 Observation, Observation 只能由系统提供
3. Action 的格式必须严格为：工具名[参数]
4. 如果问题不需要工具就能回答，直接使用 finish
"""


def parse_action(text: str):
    match = re.search(r"Action:\s*(\w+)\[([^\]]*)\]", text, re.DOTALL)
    if match:
        return match.group(1), match.group(2)
    return None


def run_react(question: str) -> str:
    """执行一次完整的 ReAct 推理循环"""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Question: {question}"},
    ]

    for i in range(MAX_ITERATIONS):
        # TODO: 调用 LLM（不带 tools 参数）
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            temperature=0.0,
        )

        # TODO: 打印 LLM 输出（Thought + Action）
        assistant_message = response.choices[0].message
        content = assistant_message.content
        print(f"\nLLM 输出:\n{content}")

        # TODO: 解析 Action
        action = parse_action(content)

        # 如果没有按格式输出，直接返回 LLM 输出作为最终答案
        if action is None:
            return content.strip()

        # TODO: 如果是 finish，返回最终答案
        if action and action[0] == "finish":
            return action[1]

        # TODO: 如果是其他工具，执行并构造 Observation
        observation = ""
        if action and action[0] in TOOL_FUNCTIONS:
            func = TOOL_FUNCTIONS[action[0]]
            try:
                if action[1].strip():
                    result = func(action[1])
                else:
                    result = func()
            except Exception as e:
                result = f"工具执行出错: {str(e)}"
            observation = f"工具 {action[0]} 的结果: {result}"
        else:
            observation = "未识别的工具调用，无法执行"
        print(f"Observation:\n{observation}")

        # TODO: 将 LLM 输出和 Observation 追加到 messages
        messages.append(assistant_message)
        messages.append({"role": "user", "content": f"Observation: {observation}"})

    return "（达到最大推理步数，强制终止）"


def main():
    print("=" * 40)
    print("🧠 ReAct Agent(Prompt 驱动)输入 quit 退出")
    print("=" * 40)

    while True:
        question = input("\nQuestion: ").strip()
        if question.lower() == "quit":
            print("再见！👋")
            break
        if not question:
            continue

        answer = run_react(question)
        print(f"\n✅ 最终回答：{answer}")


if __name__ == "__main__":
    main()
