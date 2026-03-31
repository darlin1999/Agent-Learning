import sys
import os
from importlib.metadata import PackageNotFoundError, version


def check(name: str, condition: bool, detail: str = ""):
    status = "✅" if condition else "❌"
    msg = f"  {status} {name}"
    if detail:
        msg += f"  →  {detail}"
    print(msg)
    return condition


print("=" * 50)
print("Day 5 环境健康检查")
print("=" * 50)

all_ok = True

# 1. Python 版本
v = sys.version_info
all_ok &= check("Python 版本", v >= (3, 9), f"{v.major}.{v.minor}.{v.micro}")

# 2. 虚拟环境
in_venv = sys.prefix != sys.base_prefix
all_ok &= check("虚拟环境已激活", in_venv, sys.prefix if in_venv else "未检测到 venv")

# 3. openai SDK
try:
    import openai
    all_ok &= check("openai SDK", True, openai.__version__)
except ImportError:
    all_ok &= check("openai SDK", False, "未安装，请执行 pip install openai")

# 4. anthropic SDK
try:
    import anthropic
    all_ok &= check("anthropic SDK", True, anthropic.__version__)
except ImportError:
    all_ok &= check("anthropic SDK", False, "未安装，请执行 pip install anthropic")

# 5. python-dotenv
try:
    dotenv_version = version("python-dotenv")
    all_ok &= check("python-dotenv", True, dotenv_version)
except PackageNotFoundError:
    all_ok &= check("python-dotenv", False, "未安装，请执行 pip install python-dotenv")

# 6. .env 文件存在
from dotenv import load_dotenv
load_dotenv()
env_exists = os.getenv("DEEPSEEK_API_KEY") is not None
all_ok &= check(".env 中 DEEPSEEK_API_KEY", env_exists,
                 "已配置" if env_exists else "未找到，请检查 .env 文件位置")

# 7. API 可用性（实际调用一次）
if env_exists:
    try:
        from openai import OpenAI
        client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com",
        )
        resp = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": "回复OK"}],
            max_tokens=5,
        )
        got_reply = resp.choices[0].message.content is not None
        all_ok &= check("DeepSeek API 连通性", got_reply, "调用成功")
    except Exception as e:
        all_ok &= check("DeepSeek API 连通性", False, str(e))

# 8. 项目目录
proj_dir = os.path.join(os.path.dirname(__file__), "..", "projects", "week1_chatbot")
all_ok &= check("projects/week1_chatbot/ 目录", os.path.isdir(proj_dir), "已创建")

# 9. requirements.txt
req_file = os.path.join(os.path.dirname(__file__), "..", "requirements.txt")
all_ok &= check("requirements.txt", os.path.isfile(req_file), "已创建")

print("\n" + "=" * 50)
if all_ok:
    print("🎉 全部通过！环境已就绪，周六可以直接开始写 ChatBot。")
else:
    print("⚠️  部分检查未通过，请根据上方提示修复后重新运行此脚本。")
print("=" * 50)