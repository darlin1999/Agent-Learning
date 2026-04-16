import os
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageToolCall
from dotenv import load_dotenv
from typing import TypedDict, Literal, Annotated
from langgraph.graph import StateGraph, START, END
import operator
from experimental_tools import TOOLS, TOOL_DESCRIPTIONS
import json


class AgentState(TypedDict):
    input: str
    messages: Annotated[list[dict], operator.add]
    tool_calls: list[ChatCompletionMessageToolCall]
    final_answer: str


load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com"
)


def llm_node(state: AgentState) -> dict:
    messages = state["messages"]
    if not messages:
        messages = [
            {"role": "system", "content": "你是一个有用的助手，可以使用工具回答问题。"},
            {"role": "user", "content": state["input"]},
        ]

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=TOOL_DESCRIPTIONS,
        temperature=0.1,
    )

    assistant_message = response.choices[0].message

    if assistant_message.tool_calls:
        return {
            "messages": [assistant_message.model_dump()],
            "tool_calls": assistant_message.tool_calls,
        }
    else:
        return {
            "messages": [{"role": "assistant", "content": assistant_message.content}],
            "final_answer": assistant_message.content,
        }


def tool_node(state: AgentState) -> dict:
    tool_messages = []
    for tool_call in state["tool_calls"]:
        func_name = tool_call.function.name
        func_args = json.loads(tool_call.function.arguments)
        func = TOOLS.get(func_name)

        if func is None:
            result = json.dumps({"error": f"未知工具: {func_name}"}, ensure_ascii=False)
        else:
            result = str(func(**func_args))

        tool_messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            }
        )

    return {
        "messages": tool_messages,
        "tool_calls": [],
    }


def should_continue(state: AgentState) -> Literal["tool_node", "__end__"]:
    if state["tool_calls"]:
        return "tool_node"
    else:
        return "__end__"


workflow = StateGraph(AgentState)

workflow.add_node("llm_node", llm_node)
workflow.add_node("tool_node", tool_node)

workflow.add_edge(START, "llm_node")
workflow.add_conditional_edges("llm_node", should_continue)
workflow.add_edge("tool_node", "llm_node")

app = workflow.compile()

result = app.invoke(
    {
        "input": "句子'I my the bset of best'有几个单词？",
        "messages": [],
        "tool_calls": [],
        "final_answer": "",
    }
)

print(f"\n[最终回答]：{result['final_answer']}")
