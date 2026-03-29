# 传统软件工程师 → Agent 开发工程师 三个月转型计划

> **时间投入**：每周 14 小时  
> 周一至周五：每日 1 小时（碎片化理论 + 代码练习）  
> 周六：3 小时（综合实践）  
> 周日：6 小时（项目开发 / 深度研究）  
> **总计**：12 周 × 14 小时 = **168 小时**

---

## 四大里程碑总览

| 节点 | 时间 | 阶段性成果 |
|------|------|-----------|
| **里程碑 1** | 第 1 周末 | 完成首个可运行的 Agent Demo，能独立调用 LLM API |
| **里程碑 2** | 第 3 周末 | 掌握主流框架，独立开发出具备工具调用与对话记忆的单一 Agent |
| **里程碑 3** | 第 6 周末（一个半月） | 完成 RAG 知识库问答 Agent，掌握 Memory 机制，能独立设计 Agent 架构 |
| **里程碑 4** | 第 12 周末（三个月） | 完成 1-2 个生产级 Agent 项目，具备独立承担 Agent 开发工作的核心竞争力 |

---

## 第一阶段：认知建构与快速入门（第 1-3 周）

### 学习目标
- 理解 LLM、Prompt、Agent、Tool Use 等核心概念
- 完成开发环境搭建，跑通第一个 Agent
- 掌握 Prompt Engineering 基础与主流框架入门

---

### 第 1 周（14 小时）—— 概念破冰 + 第一个 Agent

| 天 | 时长 | 内容 |
|----|------|------|
| 周一 | 1h | **AI/LLM 基础**：LLM 工作原理、Token、Temperature、上下文窗口；理解 Agent 与传统软件的本质差异（响应式 vs 主动规划） |
| 周二 | 1h | **API 入门**：注册 OpenAI / 通义千问 / DeepSeek API，用 curl/Postman 完成第一次 Chat Completion 调用，理解 messages 结构 |
| 周三 | 1h | **Prompt Engineering 基础**：Zero-shot、Few-shot、Chain of Thought，实验不同 Prompt 对输出的影响 |
| 周四 | 1h | **Function Calling / Tool Use**：理解 LLM 如何调用外部工具，阅读官方 tools 参数文档并手写一个简单示例 |
| 周五 | 1h | **环境搭建**：搭建 Python 开发环境，安装 openai / anthropic SDK，配置 `.env` 管理 API Key |
| 周六 | 3h | **实践**：用原生 SDK（不借助框架）实现一个带工具调用的简单 ChatBot —— 工具：查询当前时间、计算器 |
| 周日 | 6h | **深度研究**：阅读 ReAct 论文（ [arXiv:2210.03629](https://arxiv.org/abs/2210.03629) ）理解推理-行动循环；在上述 ChatBot 基础上实现 ReAct 循环（思考→工具调用→观察→再思考），不使用框架，纯手写 |

#### 里程碑 1 交付物（第 1 周末）
- [ ] 一个可运行的 ReAct 风格 Agent（纯 SDK，无框架）
- [ ] 该 Agent 能够：接收自然语言提问 → 推理需要哪个工具 → 调用工具 → 综合结果作答
- [ ] 一份个人笔记：LLM vs 传统程序的思维转变总结（500 字以上）

---

### 第 2 周（14 小时）—— Prompt 进阶 + 框架认知

| 天 | 时长 | 内容 |
|----|------|------|
| 周一 | 1h | **System Prompt 设计**：角色设定、输出格式约束、安全边界；练习写一个生产级 System Prompt |
| 周二 | 1h | **结构化输出**：JSON Mode / Structured Outputs，用 Pydantic 定义输出 Schema |
| 周三 | 1h | **LangChain 快速入门**：Chain、LLM、PromptTemplate 核心概念，跑通官方 5 分钟入门示例 |
| 周四 | 1h | **LangChain Tools & Agents**：内置工具、自定义工具，使用 `create_react_agent` 复现第 1 周手写 Agent |
| 周五 | 1h | **对比与思考**：手写 Agent vs 框架 Agent 的优劣分析；了解 LlamaIndex 定位与 LangChain 的差异 |
| 周六 | 3h | **实践**：用 LangChain 构建一个能搜索网页（SerpAPI 或 DuckDuckGo Tool）的研究助手 Agent |
| 周日 | 6h | **深度实践**：为工作场景设计一个实用 Agent（如：代码审查助手 / 需求文档生成 Agent），完成 v0.1 版本 |

---

### 第 3 周（14 小时）—— 单 Agent 完整能力

| 天 | 时长 | 内容 |
|----|------|------|
| 周一 | 1h | **Memory 机制**：ConversationBufferMemory、ConversationSummaryMemory、窗口记忆；理解短期与长期记忆的区别 |
| 周二 | 1h | **错误处理与重试**：LLM 输出解析失败的处理策略，OutputFixingParser，Agent 最大迭代次数控制 |
| 周三 | 1h | **流式输出（Streaming）**：streaming=True 实现打字机效果，提升用户体验 |
| 周四 | 1h | **Agent 调试技巧**：LangSmith Tracing 配置，查看 Agent 推理链路，定位工具调用错误 |
| 周五 | 1h | **代码复盘**：整理第 1-3 周代码，规范项目结构，写 README |
| 周六 | 3h | **实践**：为第 2 周的工作场景 Agent 添加 Memory 和 Streaming，完善错误处理 |
| 周日 | 6h | **里程碑 2 项目冲刺**：完成一个功能完整的单 Agent：具备工具调用（至少 3 个工具）、对话记忆、流式输出、异常处理，并录制一个 3 分钟 Demo 视频 |

#### 里程碑 2 交付物（第 3 周末）
- [ ] 一个完整的单 Agent 项目（GitHub 仓库，含 README）
  - 至少 3 个自定义工具
  - 支持多轮对话记忆
  - 流式输出
  - 完善的异常处理
- [ ] LangSmith 中可查看的完整 Trace 记录
- [ ] 3 分钟功能演示视频 / GIF

---

## 第二阶段：核心技能构建（第 4-6 周）

### 学习目标
- 掌握 RAG（Retrieval-Augmented Generation）系统设计与实现
- 理解向量数据库原理，能选型并落地
- 完成具备长期知识记忆的 Agent 系统

---

### 第 4 周（14 小时）—— RAG 基础

| 天 | 时长 | 内容 |
|----|------|------|
| 周一 | 1h | **RAG 原理**：为什么需要 RAG；检索增强 vs 微调的适用场景；RAG 完整流程（Indexing → Retrieval → Generation） |
| 周二 | 1h | **Embedding 模型**：文本向量化原理，OpenAI text-embedding-3-small vs 本地 BGE 模型对比，动手生成向量并计算余弦相似度 |
| 周三 | 1h | **向量数据库选型**：Chroma（本地开发）/ Qdrant（生产）/ FAISS（纯 Python）的适用场景；本地安装 Chroma 并完成增删查操作 |
| 周四 | 1h | **文档处理**：Document Loader（PDF/Markdown/网页）、文本分割策略（递归分割 vs 语义分割）、Chunk Size 选择原则 |
| 周五 | 1h | **检索策略**：相似度搜索 vs MMR（最大边际相关性）、元数据过滤、混合检索（向量 + 关键词） |
| 周六 | 3h | **实践**：搭建一个个人技术文档问答系统，索引自己的笔记/项目文档，实现语义搜索 |
| 周日 | 6h | **深度实践**：将 RAG 与 Agent 结合，实现一个能回答"基于公司内部文档"问题的 Agent，支持引用来源 |

---

### 第 5 周（14 小时）—— RAG 进阶 + 评估体系

| 天 | 时长 | 内容 |
|----|------|------|
| 周一 | 1h | **高级检索**：Multi-Query Retriever（同一问题多角度扩展）、HyDE（假设文档嵌入）、父子文档检索 |
| 周二 | 1h | **Reranker**：Cross-Encoder 重排序原理，BGE Reranker 实践，检索质量提升策略 |
| 周三 | 1h | **RAG 评估**：RAGAS 框架介绍，Faithfulness / Answer Relevancy / Context Recall 三大指标 |
| 周四 | 1h | **GraphRAG 概念**：知识图谱辅助检索的思路，了解 Microsoft GraphRAG 项目 |
| 周五 | 1h | **Agentic RAG**：让 Agent 自主决策何时检索、检索什么，实现 Self-Query Retriever |
| 周六 | 3h | **实践**：用 RAGAS 对上周的文档问答系统进行评估，根据评估结果优化检索策略 |
| 周日 | 6h | **综合项目**：构建一个完整的"代码仓库问答 Agent"：索引 GitHub 仓库代码 → 理解代码结构 → 回答"这个函数做什么/为什么这样实现"类问题 |

---

### 第 6 周（14 小时）—— Memory 系统 + Agent 架构设计

| 天 | 时长 | 内容 |
|----|------|------|
| 周一 | 1h | **长期记忆设计**：将重要对话摘要持久化到向量数据库，实现跨会话记忆 |
| 周二 | 1h | **外部存储**：Redis / PostgreSQL 作为 Agent 记忆后端，了解 mem0 / Zep 等记忆框架 |
| 周三 | 1h | **Agent 规划能力**：Plan-and-Execute 模式，LangGraph 中的规划节点设计 |
| 周四 | 1h | **LangGraph 入门**：Graph、Node、Edge、State 四大核心概念，实现一个简单的状态机 Agent |
| 周五 | 1h | **架构设计思维**：给定一个真实业务场景，尝试独立设计 Agent 系统架构（画图 + 文字说明） |
| 周六 | 3h | **实践**：将第 4-5 周的 RAG Agent 升级，添加持久化长期记忆 |
| 周日 | 6h | **里程碑 3 项目冲刺**：完成一个"智能知识库 Agent" —— RAG + 长期记忆 + LangGraph 状态管理 + RAGAS 评估报告 |

#### 里程碑 3 交付物（第 6 周末 / 一个半月）
- [ ] 一个"智能知识库 Agent"完整项目（GitHub 仓库）
  - RAG 检索（含 Reranker）
  - 跨会话长期记忆（持久化到 DB）
  - LangGraph 状态管理
  - RAGAS 评估报告（量化指标）
- [ ] 一份 Agent 架构设计文档（针对一个真实业务场景）
- [ ] 技术总结博客文章（掘金/CSDN/个人博客）

---

## 第三阶段：多 Agent 与生产化（第 7-9 周）

### 学习目标
- 掌握多 Agent 协作框架
- 理解 Agent 生产化所需的工程能力
- 具备评估、优化、安全加固的完整工程意识

---

### 第 7 周（14 小时）—— 多 Agent 系统

| 天 | 时长 | 内容 |
|----|------|------|
| 周一 | 1h | **多 Agent 设计模式**：Supervisor/Worker 模式、流水线模式、辩论模式；理解何时需要多 Agent |
| 周二 | 1h | **LangGraph Multi-Agent**：Supervisor Agent 实现，动态路由到子 Agent |
| 周三 | 1h | **AutoGen 框架**：ConversableAgent、GroupChat，与 LangGraph 的对比 |
| 周四 | 1h | **CrewAI**：Role-based Agent，任务分配与结果汇总，适合流程化业务 |
| 周五 | 1h | **框架选型决策树**：整理何时用 LangGraph / AutoGen / CrewAI / 手写的判断标准 |
| 周六 | 3h | **实践**：用 LangGraph 实现一个"代码生成-审查-测试"三 Agent 流水线 |
| 周日 | 6h | **深度项目**：设计并实现一个多 Agent 协作的业务场景（如：市场调研 Agent 团队，分工完成竞品分析报告） |

---

### 第 8 周（14 小时）—— 生产化工程能力

| 天 | 时长 | 内容 |
|----|------|------|
| 周一 | 1h | **成本控制**：Token 计费原理，Prompt 压缩策略（LLMLingua），模型降级策略，缓存（Redis semantic cache） |
| 周二 | 1h | **延迟优化**：并行工具调用、Speculative Execution、流式输出、模型路由 |
| 周三 | 1h | **可观测性**：集成 LangSmith / Langfuse，添加自定义 Span，构建监控 Dashboard |
| 周四 | 1h | **Agent 安全**：Prompt Injection 攻防实践，工具权限最小化，输入输出过滤，幻觉检测 |
| 周五 | 1h | **测试策略**：单元测试（Mock LLM）、集成测试、端到端评估，CI/CD 中的 Agent 测试 |
| 周六 | 3h | **实践**：为第 7 周的多 Agent 项目添加完整的可观测性和成本监控 |
| 周日 | 6h | **深度实践**：对现有项目进行安全审查，补充 Prompt Injection 防护 + 输入验证，编写测试套件 |

---

### 第 9 周（14 小时）—— MCP 协议与生态工具

| 天 | 时长 | 内容 |
|----|------|------|
| 周一 | 1h | **MCP（Model Context Protocol）**：理解 MCP 的设计目标，Server/Client 架构，与传统 API 的区别 |
| 周二 | 1h | **MCP 实践**：搭建一个 MCP Server（基于 Filesystem / Database），在 Claude Desktop 中连接并测试 |
| 周三 | 1h | **OpenAI Assistants API** vs **自建 Agent** 的工程权衡分析 |
| 周四 | 1h | **向量数据库生产选型**：Qdrant / Weaviate / Pinecone 性能对比，集群部署注意事项 |
| 周五 | 1h | **Agent 部署方案**：FastAPI 封装 Agent 为 REST 服务，WebSocket 支持流式输出 |
| 周六 | 3h | **实践**：将一个 Agent 打包为 FastAPI 服务，添加认证、限流、健康检查 |
| 周日 | 6h | **综合复盘**：整理第 7-9 周知识，将多 Agent 项目补充完整文档和测试，准备第四阶段综合项目 |

---

## 第四阶段：综合项目实战（第 10-12 周）

### 学习目标
- 完成 1-2 个有实际价值的生产级 Agent 项目
- 覆盖完整的产品开发生命周期（需求 → 设计 → 开发 → 测试 → 部署）
- 形成可展示的作品集，具备转型求职竞争力

---

### 推荐综合项目方向（选 1-2 个）

| 方向 | 核心技术 | 难度 |
|------|----------|------|
| **智能代码助手** | RAG（代码索引）+ 多工具 Agent（代码执行/测试/文档生成）+ LangGraph | ★★★★ |
| **企业知识问答系统** | RAG + 权限控制 + 多轮对话 + 引用溯源 + 生产部署 | ★★★☆ |
| **自动化数据分析 Agent** | Code Interpreter + 图表生成 + 自然语言 → SQL + 报告生成 | ★★★★ |
| **智能运维 Agent** | 监控告警接入 + 根因分析 + 自动修复建议 + Runbook 执行 | ★★★★ |

---

### 第 10 周（14 小时）—— 项目启动 + 核心功能

| 天 | 时长 | 内容 |
|----|------|------|
| 周一 | 1h | 需求分析，系统设计文档（数据流、Agent 拓扑图、技术选型） |
| 周二 | 1h | 项目脚手架搭建（目录结构、依赖管理、配置文件、CI 流水线） |
| 周三 | 1h | Core Agent 逻辑 v0.1 |
| 周四 | 1h | 核心工具开发（第 1-2 个） |
| 周五 | 1h | 核心工具开发（第 3-4 个）+ 单元测试 |
| 周六 | 3h | 核心功能集成，完成端到端 Happy Path |
| 周日 | 6h | 完善核心功能，添加错误处理，达到 v0.5 |

---

### 第 11 周（14 小时）—— 功能完善 + 质量提升

| 天 | 时长 | 内容 |
|----|------|------|
| 周一 | 1h | 边界情况处理，异常 Case 复现与修复 |
| 周二 | 1h | 性能优化（并行工具调用、缓存策略） |
| 周三 | 1h | 安全加固（输入验证、Prompt Injection 防护） |
| 周四 | 1h | 集成可观测性（Langfuse/LangSmith），添加业务指标埋点 |
| 周五 | 1h | 编写集成测试套件，达到核心路径测试覆盖 |
| 周六 | 3h | Docker 容器化，编写 docker-compose.yml |
| 周日 | 6h | 部署到云服务器（如腾讯云轻量/阿里云 ECS），确保服务稳定运行，完成 v1.0 |

---

### 第 12 周（14 小时）—— 收尾、总结与展示

| 天 | 时长 | 内容 |
|----|------|------|
| 周一 | 1h | 性能基准测试，记录延迟 P50/P99，Token 消耗，成本估算 |
| 周二 | 1h | 撰写 README（项目介绍、架构图、快速启动、API 文档） |
| 周三 | 1h | 录制项目演示视频（5-10 分钟，讲清楚解决了什么问题、如何实现） |
| 周四 | 1h | 总结技术博客，发布到掘金/知乎/CSDN |
| 周五 | 1h | 整理 GitHub Profile，完善各项目 README 和 Stars |
| 周六 | 3h | 复盘三个月学习历程，更新简历（Agent 开发相关技能栈和项目经验） |
| 周日 | 6h | **里程碑 4 冲刺**：准备技术面试题库（Agent 设计类问题），完整过一遍所有项目，确保能流畅讲解每一个技术决策 |

#### 里程碑 4 交付物（第 12 周末 / 三个月）
- [ ] 1-2 个生产级 Agent 项目（已部署，可在线访问）
- [ ] 完整 GitHub 作品集（含 README、架构图、演示视频）
- [ ] 2-3 篇技术博客文章
- [ ] 更新后的简历（突出 Agent 开发经验）
- [ ] 30 道 Agent 技术面试题 + 参考答案

---

## 核心技术栈速查

### 必学框架
| 类别 | 工具 | 优先级 |
|------|------|--------|
| Agent 框架 | LangChain + LangGraph | ★★★★★ 必学 |
| 多 Agent | AutoGen / CrewAI | ★★★★ 重要 |
| 向量数据库 | Chroma（开发）/ Qdrant（生产） | ★★★★★ 必学 |
| 记忆系统 | mem0 / Zep | ★★★ 了解 |
| 可观测性 | LangSmith / Langfuse | ★★★★ 重要 |
| 协议标准 | MCP | ★★★★ 重要 |
| 服务化 | FastAPI + WebSocket | ★★★★ 重要 |
| 部署 | Docker + 云服务器 | ★★★★ 重要 |

### 推荐学习资源
- **官方文档**：LangChain Docs、LangGraph Docs（最权威，优先阅读）
- **论文**：ReAct（2022）、Toolformer（2023）、HuggingGPT（2023）
- **课程**：DeepLearning.AI 《LangChain for LLM Application Development》（免费）
- **社区**：LangChain Discord、r/LocalLLaMA

---

## 时间管理建议

### 工作日 1 小时（高效利用碎片时间）
- 前 5 分钟：回顾昨天内容
- 40 分钟：学习新知识 / 写代码
- 10 分钟：笔记整理，记录遗留问题
- 5 分钟：规划明天内容

### 周六 3 小时（综合实践）
- 60 分钟：整合本周理论，解决遗留问题
- 90 分钟：动手编写完整功能
- 30 分钟：代码 Review，整理笔记

### 周日 6 小时（深度时间）
- 分成两段：上午 3 小时 + 下午 3 小时
- 上午：深度理解某个关键概念，读源码 / 论文
- 下午：项目推进，朝里程碑目标冲刺

---

## 衡量转型成功的标准

到第 12 周末，你应该能够：

1. **独立设计** 一个 Agent 系统的架构（画出数据流、工具列表、状态管理方案）
2. **独立开发** 具备 RAG、Memory、Tool Use、多 Agent 协作能力的生产级应用
3. **独立评估** Agent 系统的质量（RAGAS 指标、延迟、成本、安全）
4. **独立部署** Agent 服务到生产环境并保证高可用
5. **清晰表达** 技术选型背后的权衡（为什么用 LangGraph 而不是 AutoGen？为什么用 Qdrant 而不是 Pinecone？）
