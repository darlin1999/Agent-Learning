import os
from dotenv import load_dotenv
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_agent

load_dotenv()

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
    temperature=0,
)

# ── 自定义工具定义 ────────────────────────────────────────


@tool
def get_current_time() -> str:
    """获取当前日期和时间。当用户问"现在几点""今天几号"等时间相关问题时使用。"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@tool
def calculator(expression: str) -> str:
    """计算数学表达式。输入一个合法的 Python 数学表达式（如 '2+3*4'），返回计算结果。

    Args:
        expression: 数学表达式字符串，如 '2+3*4', '100/7', '2**10'
    """
    try:
        # 安全限制：只允许数字和基本运算符
        allowed = set("0123456789+-*/.() ")
        if not all(c in allowed for c in expression):
            return "错误：表达式包含不允许的字符"
        result = eval(expression)  # 已做安全过滤
        return str(result)
    except Exception as e:
        return f"计算错误：{e}"


@tool
def search_knowledge(query: str) -> str:
    """搜索内部知识库。当用户问关于公司政策、技术文档等内部信息时使用。

    Args:
        query: 搜索关键词
    """
    # 模拟知识库（实际项目中对接向量数据库）
    knowledge_base = {
        "请假": "公司年假政策: 入职满1年享受5天年假, 满3年10天, 满5年15天。请假需提前3天在OA系统申请。",
        "报销": "报销流程: 填写报销单→附发票→部门经理审批→财务审核→打款(5个工作日内)。单笔500元以上需总监审批。",
        "技术栈": "公司主要技术栈: 后端 Python/FastAPI, 前端 React/TypeScript, 数据库 PostgreSQL, 部署 Docker/K8s。",
    }
    for key, value in knowledge_base.items():
        if key in query:
            return value
    return f"未找到与{query}相关的信息, 请尝试其他关键词。"


# 查看工具的自动生成信息
tools = [get_current_time, calculator, search_knowledge]
for t in tools:
    print(f"工具名: {t.name}")
    print(f"  描述: {t.description}")
    print(f"  参数: {t.args_schema.model_json_schema()}")
    print()

SYSTEM_PROMPT = """你是一个智能助手，可以使用以下工具来帮助用户：
- get_current_time: 查询当前时间
- calculator: 进行数学计算
- search_knowledge: 搜索内部知识库

请根据用户的问题，判断是否需要使用工具。如果需要，调用相应的工具获取信息后再回答。
如果不需要工具，直接回答即可。"""

agent = create_agent(llm, tools, system_prompt=SYSTEM_PROMPT)

if __name__ == "__main__":
    from langchain_core.messages import HumanMessage

    def run_agent(query: str):
        """运行 agent 并提取最终回答"""
        result = agent.invoke({"messages": [HumanMessage(content=query)]})
        # 返回最后一条 AI 消息的内容
        return result["messages"][-1].content

    # 测试 1：需要工具的问题
    print("=" * 60)
    print("测试 1: 时间查询")
    print(f"最终回答: {run_agent('现在几点了？')}")

    # 测试 2：数学计算
    print("\n" + "=" * 60)
    print("测试 2: 数学计算")
    print(f"最终回答: {run_agent('帮我计算 (15 + 27) * 3 - 18 / 2')}")

    # 测试 3：知识库搜索
    print("\n" + "=" * 60)
    print("测试 3: 知识库搜索")
    print(f"最终回答: {run_agent('公司的请假政策是什么？')}")

    # 测试 4：不需要工具的问题
    print("\n" + "=" * 60)
    print("测试 4: 直接回答")
    print(f"最终回答: {run_agent('Python 的 list comprehension 怎么用？')}")

    # 测试 5：多工具组合
    print("\n" + "=" * 60)
    print("测试 5: 多工具组合")
    print(f"最终回答: {run_agent('现在几点了? 另外帮我算一下如果每天工作8小时, 一周工作5天, 一个工作月工作多少小时?')}")