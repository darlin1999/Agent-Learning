import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

load_dotenv()

# Case1: 首次使用 LangChain
print("\n=== Case1: 首次使用 LangChain ===")
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
    temperature=0.5,
)

response = llm.invoke("用一句话解释什么是 LangChain")
print(response.content)
print(f"Token 使用: {response.response_metadata.get('token_usage','N/A')}")

# Case2: 使用 ChatPromptTemplate 构建复杂提示词
print("\n=== Case2: 使用 ChatPromptTemplate 构建复杂提示词 ===")
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个{domain}领域的专家，用{style}的风格回答问题。"),
        ("human", "{question}"),
    ]
)

print("模板变量:", prompt.input_variables)

formatted_prompt = prompt.invoke(
    {"domain": "Python 编程", "style": "简洁", "question": "装饰器的作用是什么?"}
)

print(f"Formatted Prompt:{formatted_prompt}")

# Case3: LangChain 级联管道
print("\n=== Case3: LangChain 级联管道 ===")
chain = prompt | llm
response = chain.invoke(
    {"domain": "Python 编程", "style": "简洁", "question": "装饰器的作用是什么?"}
)
print(response.content)

# Case4: 带 OutputParser 的完整管道
print("\n=== Case4: 带 OutputParser 的完整管道 ===")


class CodeExample(BaseModel):
    topic: str = Field(description="主题")
    code: str = Field(description="代码示例")
    explanation: str = Field(description="代码说明")


json_parser = JsonOutputParser(pydantic_object=CodeExample)
json_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个编程助手。{format_instructions}"),
        ("human", "给一个 {topic} 的代码示例"),
    ]
)

json_chain = json_prompt | llm | json_parser
json_response = json_chain.invoke(
    {
        "format_instructions": json_parser.get_format_instructions(),
        "topic": "Python 装饰器",
    }
)

print("输出格式:", type(json_response))
print("   输出:", json_response)
print(f"  主题: {json_response['topic']}")
print(f"  代码: {json_response['code'][:50]}...")
print(f"  说明: {json_response['explanation'][:50]}...")

# Case5: 多步骤流水线
print("\n=== Case5: 多步骤流水线 ===")
translate_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个专业翻译。将用户输入的英文翻译为中文。只输出翻译结果。"),
        ("human", "{english_text}"),
    ]
)

summarize_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个摘要助手。用 3 个要点总结以下内容。"),
        ("human", "{text}"),
    ]
)

translate_chain = translate_prompt | llm | StrOutputParser()
summarize_chain = summarize_prompt | llm | StrOutputParser()
full_chain = (
    translate_chain | (lambda translated: {"text": translated}) | summarize_chain
)

english = """
LangChain is a framework for developing applications powered by large language models.
It provides modular components for building chains, agents, and retrieval systems. 
The framework supports multiple LLM providers and offers tools for prompt management,
memory, and output parsing. LangChain uses LCEL (LangChain Expression Language) for
composing chains with a simple pipe syntax.
"""

summary = full_chain.invoke({"english_text": english})
print(f"最终摘要:\n{summary}")
