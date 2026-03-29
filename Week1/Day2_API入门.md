# Week 1 · Day 2 — API 入门：完成第一次 Chat Completion 调用

> **目标**：注册 API 平台账号，拿到 API Key，用工具发出第一次真实的 LLM API 请求，亲眼看到模型返回结果。
> **时间**：1 小时

---

## 一、选哪个平台：DeepSeek ✅ 推荐

| 对比项 | DeepSeek | 通义千问（DashScope） |
|--------|----------|----------------------|
| 注册难度 | 手机号即可，平台简洁 | 需要阿里云账号，步骤更多 |
| API 风格 | **完全兼容 OpenAI 格式** | 也兼容 OpenAI 格式，但文档层级更深 |
| 后续 LangChain 接入 | 一行换 `base_url` 即可 | 同上，但配置略繁琐 |
| 费用 | 有免费额度；价格极低 | 有免费额度 |
| 社区资料 | 国内外教程极多 | 较多，但偏阿里云生态 |

**结论**：DeepSeek API 格式和 OpenAI 几乎一致，后续用 LangChain / LangGraph 开发时只需换一个 `base_url`，学习成本为零，优先选它。

---

## 二、注册 —— 要注册哪个？

> ⚠️ 关键区分：`chat.deepseek.com`（网页对话，类似 ChatGPT 网页版）和 `platform.deepseek.com`（开发者 API 平台）是**两个独立入口**。
>
> 网页版账号 **不能** 调用 API，必须在开发者平台单独注册并充值。

### 注册步骤

1. 浏览器打开 `https://platform.deepseek.com`
2. 点击右上角 **"注册"**，使用手机号 + 验证码完成注册（或用邮箱）
3. 登录后，进入左侧导航 **"API Keys"**
4. 点击 **"创建 API Key"**，给它起个名字（如 `learning`），复制并**妥善保存**这个 Key

   > ⚠️ API Key 只显示一次，关闭弹窗后无法再查看，务必保存到本地（后面会放进 `.env` 文件）

5. 进入 **"充值"** 页面，充值最小金额（通常 10 元），即可开始使用

---

## 三、工具选择：curl 还是 Postman？

| | curl | Postman |
|--|------|---------|
| 上手难度 | Windows PowerShell 下语法稍繁琐 | GUI 界面，参数可视化，更直观 |
| 理解 HTTP | 直接看到原始请求，理解更深 | 帮你封装了，理解略浅 |
| 后续迁移到 Python | 观念上更接近，方便类比 | 可一键导出 Python 代码 |

**推荐方案**：**先用 Postman 完成第一次调用**（直观看清楚 JSON 结构），然后**用 curl 重复一次**（理解底层 HTTP），两者都掌握。后续 Day 3 起全部切换到 Python SDK，这两个工具仅作"破冰"使用。

---

## 四、Step-by-Step：完成第一次 Chat Completion 调用

### Step 1：安装 Postman

前往 `https://www.postman.com/downloads/` 下载并安装 Windows 版（免费，无需登录也可使用）。

---

### Step 2：用 Postman 发出第一次请求

1. 打开 Postman，点击左上角 **"+"** 新建请求

2. 请求方法选 **`POST`**，URL 填写：
   ```
   https://api.deepseek.com/chat/completions
   ```

3. 切换到 **Headers** 标签，添加两条 Header：

   | Key | Value |
   |-----|-------|
   | `Content-Type` | `application/json` |
   | `Authorization` | `Bearer 你的API_KEY` |

   > 将 `你的API_KEY` 替换为刚才保存的 Key，注意 `Bearer ` 后面有一个空格

4. 切换到 **Body** 标签，选 **raw**，右侧下拉选 **JSON**，粘贴以下内容：

   ```json
   {
     "model": "deepseek-chat",
     "messages": [
       {
         "role": "system",
         "content": "你是一个帮助学习 AI 开发的助手，回答简洁清晰。"
       },
       {
         "role": "user",
         "content": "用一句话解释什么是 LLM？"
       }
     ],
     "temperature": 0.7,
     "max_tokens": 200
   }
   ```

5. 点击蓝色 **Send** 按钮

6. 下方 Response 区域应出现类似：
   ```json
   {
     "id": "...",
     "object": "chat.completion",
     "choices": [
       {
         "message": {
           "role": "assistant",
           "content": "LLM（大型语言模型）是一种通过海量文本数据训练的 AI 模型，能够理解和生成自然语言。"
         },
         "finish_reason": "stop"
       }
     ],
     "usage": {
       "prompt_tokens": 35,
       "completion_tokens": 28,
       "total_tokens": 63
     }
   }
   ```

---

### Step 3：理解响应结构（重要！）

| 字段 | 含义 | 为什么重要 |
|------|------|-----------|
| `choices[0].message.content` | 模型实际回答 | 写代码时取这个字段 |
| `choices[0].finish_reason` | 停止原因（`stop`=正常结束，`length`=超出 max_tokens） | 判断回答是否被截断 |
| `usage.prompt_tokens` | 输入消耗 Token 数 | 成本计算依据 |
| `usage.completion_tokens` | 输出消耗 Token 数 | 成本计算依据 |
| `model` | 实际使用的模型版本 | 确认是否用对了模型 |

---

### Step 4：用 PowerShell 脚本重复一次（加深理解）

#### 4.1 解除脚本执行限制（首次需要，一次永久生效）

Windows 默认禁止运行 `.ps1` 脚本文件。在 PowerShell 中执行以下命令解除限制：

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

弹出确认时输入 `Y` 回车。此命令只影响当前用户，含义是"本地写的脚本可以直接运行"。

#### 4.2 创建脚本文件

在 `Week1` 文件夹下新建 `first_call.ps1`，内容如下（将 `YOUR_API_KEY` 替换为真实 Key）：

```powershell
$headers = @{
    "Content-Type"  = "application/json"
    "Authorization" = "Bearer YOUR_API_KEY"
}

$body = @{
    model    = "deepseek-chat"
    messages = @(
        @{ role = "system"; content = "你是一个帮助学习 AI 开发的助手。" }
        @{ role = "user";   content = "用一句话解释什么是 LLM？" }
    )
    temperature = 0.7
    max_tokens  = 200
} | ConvertTo-Json -Depth 5

Invoke-RestMethod -Uri "https://api.deepseek.com/chat/completions" `
                  -Method POST `
                  -Headers $headers `
                  -Body $body
```

#### 4.3 执行脚本

```powershell
cd D:\Users\hanqiang.wang\source\repos\Agent\Week1
.\first_call.ps1
```

> **为什么用脚本文件而不是直接粘贴命令？**  
> 多行 PowerShell 代码直接粘贴到终端时，会被逐行拆开执行导致报错。  
> 保存为 `.ps1` 文件后整体执行，不会出现这个问题，也方便后续反复修改参数重跑。

> PowerShell 原生 `curl` 是 `Invoke-WebRequest` 的别名，语法与 Linux curl 不同。上面的 `Invoke-RestMethod` 写法是 PowerShell 惯用方式，等价效果。

---

### Step 5：试着修改参数，观察变化

完成基础调用后，逐一修改以下参数，观察输出变化，建立直觉：

| 修改内容 | 预期变化 | 理解目的 |
|----------|----------|---------|
| `temperature` 从 `0.7` 改为 `0.0` | 输出更稳定、确定 | 理解 temperature 控制随机性 |
| `temperature` 改为 `1.5` | 输出更发散、有时奇怪 | 温度过高的副作用 |
| `max_tokens` 改为 `10` | 回答被截断，`finish_reason` 变为 `length` | 理解 Token 限制 |
| 在 `messages` 中去掉 `system` | 模型没有角色设定，回答风格变化 | 理解 system prompt 的作用 |
| 把 `model` 改为 `deepseek-reasoner` | 回答前会显示思维链（`reasoning_content`） | 体验推理模型 vs 对话模型 |

---

## 五、今日任务清单

- [ ] 注册 DeepSeek 开发者平台账号（`platform.deepseek.com`）
- [ ] 创建并保存 API Key
- [ ] 充值最小金额
- [ ] 用 Postman 完成第一次 Chat Completion 调用，看到模型响应
- [ ] 用 PowerShell `Invoke-RestMethod` 命令重复一次相同调用
- [ ] 修改至少 2 个参数，记录观察到的变化
- [ ] 在本文件底部写下今天的学习笔记（3-5 句话）

---

## 六、今日笔记区

> 在这里记录你的观察和问题：

```
日期：2026/03/29

观察到的有趣现象：换用deepseek-reasoner模型后，确实加入了一些推导过程的细节，但我注意到额外的reasoning_tokens消耗

遗留问题：虽然调用powershell成功了，但是我用的windows的powershell对utf-8的支持不好，需要接收数据后转成utf-8BOM才行，希望后续使用python调用时能处理好这个问题
```

---

## 七、预告：Day 3

**Prompt Engineering 基础** —— 学习 Zero-shot、Few-shot、Chain of Thought 三种 Prompt 写法。
在 Postman 里直接实验，不需要写代码，用今天拿到的 API Key 就可以跑。
