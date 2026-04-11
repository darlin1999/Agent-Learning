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
| **里程碑 4** | 第 12 周末（三个月） | 完成标书生成 Agent v1.0，具备实际生产使用能力 |

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
| 周日 | 6h | **深度实践**：标书生成 Agent v0.1 —— 分析标书需求结构，用 LangChain + python-docx 实现「输入招标要求 → 生成标书大纲 → 输出 Word 文档」的基础原型 |

---

### 第 3 周（14 小时）—— 单 Agent 完整能力

| 天 | 时长 | 内容 |
|----|------|------|
| 周一 | 1h | **Memory 机制**：ConversationBufferMemory、ConversationSummaryMemory、窗口记忆；理解短期与长期记忆的区别 |
| 周二 | 1h | **错误处理与重试**：LLM 输出解析失败的处理策略，OutputFixingParser，Agent 最大迭代次数控制 |
| 周三 | 1h | **流式输出（Streaming）**：streaming=True 实现打字机效果，提升用户体验 |
| 周四 | 1h | **Agent 调试技巧**：LangSmith Tracing 配置，查看 Agent 推理链路，定位工具调用错误 |
| 周五 | 1h | **代码复盘**：整理第 1-3 周代码，规范项目结构，写 README |
| 周六 | 3h | **实践**：为标书生成 Agent 添加 Memory（记住标书上下文和公司信息）和 Streaming，完善错误处理 |
| 周日 | 6h | **里程碑 2 项目冲刺**：标书生成 Agent v0.2 —— 具备工具调用（网络搜索、标书模板选择、大纲生成）、对话记忆（标书需求上下文）、流式输出、异常处理，并录制一个 3 分钟 Demo 视频 |

#### 里程碑 2 交付物（第 3 周末）
- [ ] 标书生成 Agent v0.2（GitHub 仓库，含 README）
  - 至少 3 个自定义工具（网络搜索、标书模板选择、大纲生成）
  - 支持多轮对话记忆（标书需求上下文）
  - 流式输出
  - 完善的异常处理
  - Word 文档输出能力（python-docx）
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
| 周六 | 3h | **实践**：搭建标书知识库 —— 索引内部已中标标书范本、公司资质文档、常用条款库，实现语义搜索 |
| 周日 | 6h | **深度实践**：将 RAG 与标书 Agent 结合 —— 检索历史标书中的相关章节作为参考，生成新标书内容时引用来源，支持「参照XX项目标书的技术方案部分」 |

---

### 第 5 周（14 小时）—— RAG 进阶 + 评估体系

| 天 | 时长 | 内容 |
|----|------|------|
| 周一 | 1h | **高级检索**：Multi-Query Retriever（同一问题多角度扩展）、HyDE（假设文档嵌入）、父子文档检索 |
| 周二 | 1h | **Reranker**：Cross-Encoder 重排序原理，BGE Reranker 实践，检索质量提升策略 |
| 周三 | 1h | **RAG 评估**：RAGAS 框架介绍，Faithfulness / Answer Relevancy / Context Recall 三大指标 |
| 周四 | 1h | **GraphRAG 概念**：知识图谱辅助检索的思路，了解 Microsoft GraphRAG 项目 |
| 周五 | 1h | **Agentic RAG**：让 Agent 自主决策何时检索、检索什么，实现 Self-Query Retriever |
| 周六 | 3h | **实践**：用 RAGAS 对标书知识库的检索质量进行评估，优化分块策略和检索参数，确保能精准匹配相关标书段落 |
| 周日 | 6h | **综合项目**：标书内容生成 Pipeline —— 多路检索（历史标书 + 公司资质 + 网络信息）→ Reranker 重排序 → 按章节生成标书内容 → 引用标注 → 输出结构化 Word 文档 |

---

### 第 6 周（14 小时）—— Memory 系统 + Agent 架构设计

| 天 | 时长 | 内容 |
|----|------|------|
| 周一 | 1h | **长期记忆设计**：将重要对话摘要持久化到向量数据库，实现跨会话记忆 |
| 周二 | 1h | **外部存储**：Redis / PostgreSQL 作为 Agent 记忆后端，了解 mem0 / Zep 等记忆框架 |
| 周三 | 1h | **Agent 规划能力**：Plan-and-Execute 模式，LangGraph 中的规划节点设计 |
| 周四 | 1h | **LangGraph 入门**：Graph、Node、Edge、State 四大核心概念，实现一个简单的状态机 Agent |
| 周五 | 1h | **架构设计思维**：给定一个真实业务场景，尝试独立设计 Agent 系统架构（画图 + 文字说明） |
| 周六 | 3h | **实践**：标书 Agent 添加持久化记忆 —— 记住公司基本信息、常用业绩案例、人员资质等，避免每次重复输入 |
| 周日 | 6h | **里程碑 3 项目冲刺**：标书生成 Agent v0.5 —— RAG 知识库检索 + 长期记忆 + LangGraph 工作流（需求分析→内容生成→格式化→输出 Word）+ RAGAS 评估报告 |

#### 里程碑 3 交付物（第 6 周末 / 一个半月）
- [ ] 标书生成 Agent v0.5 完整项目（GitHub 仓库）
  - RAG 检索标书知识库（含 Reranker）
  - 跨会话长期记忆（公司信息、业绩案例持久化）
  - LangGraph 工作流管理（需求分析→检索→生成→Word 输出）
  - RAGAS 评估报告（检索质量量化指标）
- [ ] 标书生成 Agent 架构设计文档
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
| 周六 | 3h | **实践**：用 LangGraph 实现标书生成三 Agent 流水线 —— 需求分析 Agent → 内容撰写 Agent → 格式审核 Agent |
| 周日 | 6h | **深度项目**：完整多 Agent 标书生成系统 —— 研究 Agent（网络调研 + 知识库检索）+ 撰写 Agent（按章节生成内容）+ 格式化 Agent（Word 排版 + 表格 + 目录）+ 审核 Agent（合规性检查 + 查漏补缺） |

---

### 第 8 周（14 小时）—— 生产化工程能力

| 天 | 时长 | 内容 |
|----|------|------|
| 周一 | 1h | **成本控制**：Token 计费原理，Prompt 压缩策略（LLMLingua），模型降级策略，缓存（Redis semantic cache） |
| 周二 | 1h | **延迟优化**：并行工具调用、Speculative Execution、流式输出、模型路由 |
| 周三 | 1h | **可观测性**：集成 LangSmith / Langfuse，添加自定义 Span，构建监控 Dashboard |
| 周四 | 1h | **Agent 安全**：Prompt Injection 攻防实践，工具权限最小化，输入输出过滤，幻觉检测 |
| 周五 | 1h | **测试策略**：单元测试（Mock LLM）、集成测试、端到端评估，CI/CD 中的 Agent 测试 |
| 周六 | 3h | **实践**：为标书生成多 Agent 系统添加完整的可观测性和成本监控（标书生成全链路 Trace） |
| 周日 | 6h | **深度实践**：标书 Agent 安全审查 + 质量保证 —— Prompt Injection 防护、输入验证、标书内容准确性测试套件、幻觉检测（确保生成内容不编造资质和业绩） |

---

### 第 9 周（14 小时）—— MCP 协议与生态工具

| 天 | 时长 | 内容 |
|----|------|------|
| 周一 | 1h | **MCP（Model Context Protocol）**：理解 MCP 的设计目标，Server/Client 架构，与传统 API 的区别 |
| 周二 | 1h | **MCP 实践**：搭建一个 MCP Server（基于 Filesystem / Database），在 Claude Desktop 中连接并测试 |
| 周三 | 1h | **OpenAI Assistants API** vs **自建 Agent** 的工程权衡分析 |
| 周四 | 1h | **向量数据库生产选型**：Qdrant / Weaviate / Pinecone 性能对比，集群部署注意事项 |
| 周五 | 1h | **Agent 部署方案**：FastAPI 封装 Agent 为 REST 服务，WebSocket 支持流式输出 |
| 周六 | 3h | **实践**：将标书生成 Agent 封装为 FastAPI 服务，添加认证、限流、健康检查，支持 WebSocket 流式输出生成进度 |
| 周日 | 6h | **综合复盘**：整理第 7-9 周知识，完善标书 Agent 多 Agent 系统文档和测试，准备第四阶段生产化冲刺 |

---

## 第四阶段：综合项目实战（第 10-12 周）

### 学习目标
- 将标书生成 Agent 打磨为可在公司内部实际使用的生产级工具
- 覆盖完整的产品开发生命周期（模板系统 → Word输出增强 → 审核流程 → Web UI → 部署上线）
- 形成可展示的作品集，具备转型竞争力

---

### 综合项目：标书生成 Agent（生产化）

> 前 9 周已迭代至多 Agent 版本，第 10-12 周聚焦生产化打磨，使其成为可在公司内部实际使用的工具。

**核心能力清单**：

| 能力 | 技术实现 | 状态 |
|------|----------|------|
| 标书知识库检索 | RAG + Reranker + 向量数据库 | v0.5 已有 |
| 多 Agent 协作生成 | LangGraph + Supervisor 模式 | v0.5 已有 |
| Word 文档输出 | python-docx（支持表格、目录、页眉页脚） | 需增强 |
| 网络信息调研 | Web Search Tool + 内容摘要 | 需增强 |
| 公司信息记忆 | 持久化长期记忆 | v0.5 已有 |
| 标书模板管理 | 模板库 + 动态填充 | 待开发 |
| 审核与修改 | 审核 Agent + 人机协同修改 | 待开发 |
| Web UI | Streamlit / Gradio 前端 | 待开发 |

---

### 第 10 周（14 小时）—— 标书 Agent 生产化：Word 输出与模板系统

| 天 | 时长 | 内容 |
|----|------|------|
| 周一 | 1h | 梳理真实标书结构：封面、目录、技术方案、商务报价、业绩案例、资质证明等章节规范 |
| 周二 | 1h | python-docx 进阶：样式系统、多级标题、表格、页眉页脚、目录域代码 |
| 周三 | 1h | 设计标书模板管理系统：模板注册、章节配置、动态填充逻辑 |
| 周四 | 1h | 实现标书模板引擎 v1 —— 支持 2-3 种常用标书格式模板 |
| 周五 | 1h | 网络调研工具增强 —— 企业信息查询、政策法规检索、行业数据采集 |
| 周六 | 3h | 端到端集成：招标文件输入 → 需求解析 → 内容生成 → Word 输出完整流程 |
| 周日 | 6h | 标书 Agent v0.8 —— 完善 Word 排版质量，支持表格自动生成、业绩案例自动填充，处理边界情况 |

---

### 第 11 周（14 小时）—— 审核流程 + Web UI + 质量提升

| 天 | 时长 | 内容 |
|----|------|------|
| 周一 | 1h | 设计人机协同审核流程：Agent 生成 → 人工审核标注 → Agent 修改 → 定稿循环 |
| 周二 | 1h | 实现审核反馈机制：审核意见解析、定向修改、版本对比 |
| 周三 | 1h | Streamlit / Gradio Web UI 搭建：标书生成界面、参数配置、进度展示 |
| 周四 | 1h | Web UI 完善：章节预览、在线编辑、一键导出 Word |
| 周五 | 1h | 性能优化 —— 并行章节生成、检索缓存、长标书分段处理 |
| 周六 | 3h | Docker 容器化，编写 docker-compose.yml（含向量数据库、Redis、Web 服务） |
| 周日 | 6h | 集成测试 + 用真实标书场景端到端验证，修复问题，达到 v1.0 |

---

### 第 12 周（14 小时）—— 部署上线、收尾与展示

| 天 | 时长 | 内容 |
|----|------|------|
| 周一 | 1h | 部署到内部服务器 / 云服务器，配置域名和认证，确保团队可访问 |
| 周二 | 1h | 撰写用户手册 + 技术文档（架构图、部署指南、API 文档） |
| 周三 | 1h | 内部试用 —— 邀请 2-3 位同事用真实标书需求测试，收集反馈 |
| 周四 | 1h | 根据反馈快速修复 Top 3 问题 |
| 周五 | 1h | 录制项目演示视频（5-10 分钟），撰写技术博客 |
| 周六 | 3h | 复盘三个月学习历程，整理 GitHub 作品集，更新简历 |
| 周日 | 6h | **里程碑 4 冲刺**：标书 Agent v1.0 最终打磨，准备内部推广方案，整理 Agent 开发知识体系 |

#### 里程碑 4 交付物（第 12 周末 / 三个月）
- [ ] 标书生成 Agent v1.0（已部署，团队可使用）
  - 支持多种标书格式模板
  - RAG 知识库（历史标书 + 公司资质 + 网络调研）
  - 多 Agent 协作（研究→撰写→格式化→审核）
  - Word 文档输出（专业排版）
  - Web UI 操作界面
  - 人机协同审核流程
- [ ] 完整 GitHub 作品集（含 README、架构图、演示视频）
- [ ] 用户手册 + 技术文档
- [ ] 1-2 篇技术博客文章
- [ ] 更新后的简历（突出 Agent 开发经验）

---

## 核心技术栈速查

### 必学框架
| 类别 | 工具 | 优先级 |
|------|------|--------|
| Agent 框架 | LangChain + LangGraph | ★★★★★ 必学 |
| 多 Agent | AutoGen / CrewAI | ★★★★ 重要 |
| 向量数据库 | Chroma（开发）/ Qdrant（生产） | ★★★★★ 必学 |
| 文档生成 | python-docx（Word 输出） | ★★★★★ 必学 |
| 记忆系统 | mem0 / Zep | ★★★ 了解 |
| 可观测性 | LangSmith / Langfuse | ★★★★ 重要 |
| 协议标准 | MCP | ★★★★ 重要 |
| 服务化 | FastAPI + WebSocket | ★★★★ 重要 |
| 前端 UI | Streamlit / Gradio | ★★★★ 重要 |
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
