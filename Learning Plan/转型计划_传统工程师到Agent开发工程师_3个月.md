# Agent 核心原理与开发 — 12 周学习计划

> **定位**：系统学习 Agent 核心原理与开发能力（非转行目标），掌握 Agent 时代的核心技术栈  
> **方法论**：  
> - **核心内容**：原理优先 — 先用原生 SDK 手写理解原理，主流框架（LangChain / LangGraph）作为效率工具  
> - **非核心内容**：能简则简 — 一个接口搞定的不拆分，专注 Agent 本身  
> **主线项目**：内部知识库问答 Agent — 最经典的 Agent 应用场景，天然覆盖 RAG + 工具调用 + 记忆 + 多 Agent 全部核心能力  
>  
> **时间投入**：每周 14 小时  
> 周一至周五：每日 1 小时（碎片化理论 + 代码练习）  
> 周六：3 小时（综合实践）  
> 周日：6 小时（项目开发 / 深度研究）  
> **总计**：12 周 × 14 小时 = **168 小时**

---

## 学习原则

| # | 原则 | 说明 |
|---|------|------|
| 1 | **原理优先** | 核心内容先用原生 SDK 手写理解原理，再用框架提效 |
| 2 | **主流才用** | 框架只在业界主流时使用（LangChain/LangGraph ✅），非主流仅了解思想（AutoGen/CrewAI） |
| 3 | **聚焦 Agent** | 非核心内容（UI、部署、文档格式）能简则简，不喧宾夺主 |
| 4 | **项目驱动** | 所有学习围绕「知识库问答 Agent」展开，避免零散练习 |
| 5 | **质量可验** | 每个阶段有量化评估指标（RAGAS 分数、Trace 分析） |

---

## 四大里程碑总览

| 节点 | 时间 | 阶段性成果 |
|------|------|-----------|
| **里程碑 1** | 第 1 周末 | ✅ 完成首个可运行的 ReAct Agent（纯 SDK，无框架） |
| **里程碑 2** | 第 5 周末 | 掌握 RAG 完整流程，知识库问答 Agent v0.2（原生 SDK + Reranker + 评估体系） |
| **里程碑 3** | 第 8 周末 | 多 Agent + MCP + 安全加固，知识库问答 Agent v0.5（LangGraph 工作流） |
| **里程碑 4** | 第 12 周末 | 知识库问答 Agent v1.0（服务化 + 完整评估 + 前沿能力探索） |

---

## 第一阶段：认知建构与快速入门（第 1-2 周） ✅ 已完成

### 学习目标
- ✅ 理解 LLM、Prompt、Agent、Tool Use 等核心概念
- ✅ 完成开发环境搭建，跑通第一个 Agent
- ✅ 掌握 Prompt Engineering 基础与主流框架入门

---

### 第 1 周 ✅ —— 概念破冰 + 第一个 Agent

| 天 | 时长 | 内容 | 状态 |
|----|------|------|------|
| Day1（周一） | 1h | AI/LLM 基础：工作原理、Token、Temperature、上下文窗口 | ✅ |
| Day2（周二） | 1h | API 入门：Chat Completion 调用，messages 结构 | ✅ |
| Day3（周三） | 1h | Prompt Engineering 基础：Zero-shot、Few-shot、CoT | ✅ |
| Day4（周四） | 1h | Function Calling / Tool Use：LLM 调用外部工具 | ✅ |
| Day5（周五） | 1h | 环境搭建：Python + SDK + .env 配置 | ✅ |
| Day6（周六） | 3h | 原生 SDK 实现带工具调用的 ChatBot | ✅ |
| Day7（周日） | 6h | ReAct 论文精读 + 手写 ReAct 循环（纯 SDK，无框架） | ✅ |

#### 里程碑 1 交付物 ✅
- [x] 可运行的 ReAct 风格 Agent（纯 SDK，无框架）
- [x] Agent 能：接收自然语言 → 推理工具选择 → 调用工具 → 综合结果作答

---

### 第 2 周 ✅ —— Prompt 进阶 + 框架认知

| 天 | 时长 | 内容 | 状态 |
|----|------|------|------|
| Day8（周一） | 1h | System Prompt 设计：角色设定、输出约束、安全边界 | ✅ |
| Day9（周二） | 1h | 结构化输出：JSON Mode / Pydantic Schema | ✅ |
| Day10（周三） | 1h | LangChain 快速入门：Chain、LLM、PromptTemplate | ✅ |
| Day11（周四） | 1h | LangChain Tools & Agents：`create_react_agent` 复现 | ✅ |
| Day12（周五） | 1h | 对比与思考：手写 vs 框架的优劣分析 | ✅ |
| Day13（周六） | 3h | LangChain 构建研究助手 Agent（搜索工具） | ✅ |
| Day14（周日） | 6h | 整理 Week1-2 代码与笔记，重新规划后续学习路线 | ✅ |

---

## 第二阶段：Agent 核心能力建设（第 3-5 周）

### 学习目标
- 掌握 Memory 机制、流式输出等 Agent 工程能力
- 掌握 LangGraph 状态机编排
- 掌握 RAG 完整流程（Indexing → Retrieval → Generation）
- 完成知识库问答 Agent v0.2

---

### 第 3 周（14 小时）—— 单 Agent 完整能力 + LangGraph

| 天 | 时长 | 内容 |
|----|------|------|
| 周一 | 1h | **Memory 机制**：Buffer / Summary / Window 三种记忆策略；短期 vs 长期记忆的区别与适用场景 |
| 周二 | 1h | **错误处理与重试**：LLM 输出解析失败的处理策略，Agent 最大迭代次数控制，优雅降级 |
| 周三 | 1h | **流式输出（Streaming）**：原生 SDK 实现 streaming=True 打字机效果，理解 SSE 流式协议 |
| 周四 | 1h | **LangGraph 入门**：Graph、Node、Edge、State 四大核心概念，理解状态机 Agent 的优势 |
| 周五 | 1h | **LangGraph 实践**：用 LangGraph 实现一个简单的 ReAct 状态机 Agent，对比纯手写的差异 |
| 周六 | 3h | **实践**：手写完整对话 Agent（原生 SDK）—— 带 Memory（对话历史管理）+ 工具调用 + 流式输出 |
| 周日 | 6h | **深度实践**：用 LangGraph 重构上述 Agent —— 状态管理、条件路由、人机协同（Human-in-the-loop）；深入对比手写 vs LangGraph 的工程效率差异 |

---

### 第 4 周（14 小时）—— RAG 基础

| 天 | 时长 | 内容 |
|----|------|------|
| 周一 | 1h | **RAG 原理**：为什么需要 RAG；检索增强 vs 微调的适用场景；RAG 完整流程（Indexing → Retrieval → Generation） |
| 周二 | 1h | **Embedding 模型**：文本向量化原理，余弦相似度手动计算；OpenAI text-embedding-3-small vs 本地 BGE 模型对比 |
| 周三 | 1h | **向量数据库**：Chroma（本地开发）/ FAISS（纯 Python）安装与增删查操作，理解索引结构 |
| 周四 | 1h | **文档处理**：Document Loader（PDF / Markdown / 网页）、文本分割策略（递归分割 vs 语义分割）、Chunk Size 选择原则 |
| 周五 | 1h | **检索策略**：相似度搜索 vs MMR（最大边际相关性）、元数据过滤、混合检索（向量 + 关键词） |
| 周六 | 3h | **实践**：用原生 SDK + Chroma 从零搭建文档问答系统（不用框架，手写 RAG 每一步：加载→分块→嵌入→检索→生成） |
| 周日 | 6h | **深度实践**：知识库问答 Agent v0.1 —— 索引内部文档（Markdown / PDF），实现完整 RAG 链路：问答时检索相关段落 + 引用来源标注，纯 SDK 实现 |

---

### 第 5 周（14 小时）—— RAG 进阶 + 评估体系

| 天 | 时长 | 内容 |
|----|------|------|
| 周一 | 1h | **高级检索**：Multi-Query Retriever（同一问题多角度扩展）、HyDE（假设文档嵌入）；理解何时用哪种策略 |
| 周二 | 1h | **Reranker**：Cross-Encoder 重排序原理，BGE Reranker 实践，检索质量提升策略 |
| 周三 | 1h | **RAG 评估**：RAGAS 框架介绍，Faithfulness / Answer Relevancy / Context Recall 三大指标 |
| 周四 | 1h | **Agentic RAG**：让 Agent 自主决策何时检索、检索什么；Self-Query Retriever 原理 |
| 周五 | 1h | **GraphRAG 概念**：知识图谱辅助检索的思路，了解 Microsoft GraphRAG 项目（仅了解，不深入） |
| 周六 | 3h | **实践**：用 RAGAS 评估 v0.1 的检索质量，优化分块策略和检索参数，对比优化前后指标变化 |
| 周日 | 6h | **里程碑 2 冲刺**：知识库问答 Agent v0.2 —— 多路检索 + Reranker 重排序 + Agentic RAG（Agent 自主判断是否需要检索 / 直接回答）+ RAGAS 评估报告 |

#### 里程碑 2 交付物（第 5 周末）
- [ ] 知识库问答 Agent v0.2（GitHub 仓库，含 README）
  - 完整 RAG 流程（索引 → 检索 → 生成）
  - Reranker 重排序提升检索精度
  - Agentic RAG（Agent 自主决策检索策略）
  - RAGAS 评估报告（检索质量量化指标 + 优化前后对比）
- [ ] RAG 核心原理与实践总结笔记

---

## 第三阶段：高级 Agent 模式（第 6-8 周）

### 学习目标
- 掌握 Agent 架构设计与规划能力
- 掌握多 Agent 协作系统设计与实现
- 理解 MCP 协议、Agent 安全与可观测性

---

### 第 6 周（14 小时）—— Agent 架构设计 + Memory 系统

| 天 | 时长 | 内容 |
|----|------|------|
| 周一 | 1h | **长期记忆设计**：将对话摘要持久化到向量数据库，实现跨会话记忆 |
| 周二 | 1h | **记忆框架了解**：mem0 / Zep 等记忆框架的设计思路（了解思想，不深入使用） |
| 周三 | 1h | **Plan-and-Execute 模式**：Agent 先规划再执行的架构，LangGraph 中的规划节点设计 |
| 周四 | 1h | **LangGraph 深入**：条件路由、子图（Subgraph）、Human-in-the-loop 断点 |
| 周五 | 1h | **架构设计练习**：给定业务场景，独立设计 Agent 系统架构（画图 + 文字说明） |
| 周六 | 3h | **实践**：为知识库 Agent 添加持久化长期记忆 —— 记住用户偏好、常见问答对、历史查询模式 |
| 周日 | 6h | **深度实践**：知识库问答 Agent v0.3 —— LangGraph 工作流（意图识别 → 检索策略选择 → 多路检索 → 生成 → 自检）+ 跨会话记忆 + Plan-and-Execute 规划 |

---

### 第 7 周（14 小时）—— 多 Agent 系统

| 天 | 时长 | 内容 |
|----|------|------|
| 周一 | 1h | **多 Agent 设计模式**：Supervisor / Worker 模式、流水线模式、辩论模式；何时需要多 Agent vs 单 Agent |
| 周二 | 1h | **LangGraph Multi-Agent**：Supervisor Agent 实现，动态路由到子 Agent |
| 周三 | 1h | **Agent 间通信**：状态共享、消息传递、结果汇总策略 |
| 周四 | 1h | **AutoGen / CrewAI 概念**：了解设计思想与适用场景（仅了解，不深入使用） |
| 周五 | 1h | **框架选型决策**：整理 LangGraph / AutoGen / CrewAI / 手写的判断标准 |
| 周六 | 3h | **实践**：用 LangGraph 实现 Supervisor + Worker 模式原型（通用 Agent 编排） |
| 周日 | 6h | **深度实践**：知识库问答 Agent 多 Agent 版 —— 路由 Agent（意图分类 + 复杂度判断）+ 检索 Agent（知识库搜索 + 多路召回）+ 生成 Agent（答案组织 + 引用标注）+ 审核 Agent（幻觉检测 + 质量评分） |

---

### 第 8 周（14 小时）—— MCP + 安全 + 可观测性

| 天 | 时长 | 内容 |
|----|------|------|
| 周一 | 1h | **MCP 协议**：理解 MCP 的设计目标，Server / Client 架构，Resources / Tools / Prompts 三大原语，与传统 API 的本质区别 |
| 周二 | 1h | **MCP Server 实践**：将知识库问答能力封装为 MCP Server，在 Claude Desktop / VS Code 中连接测试 |
| 周三 | 1h | **Agent 安全**：Prompt Injection 攻防实践（直接注入 + 间接注入），工具权限最小化，输入输出过滤 |
| 周四 | 1h | **可观测性**：LangSmith / Langfuse 集成，添加自定义 Span，分析 Agent 推理链路 |
| 周五 | 1h | **成本控制**：Token 计费原理、Prompt 压缩策略、模型降级（大模型路由 + 小模型兜底）、语义缓存 |
| 周六 | 3h | **实践**：为知识库 Agent 添加 MCP 接口 + Prompt Injection 防护 + 全链路 Trace |
| 周日 | 6h | **里程碑 3 冲刺**：知识库问答 Agent v0.5 —— 多 Agent 架构（LangGraph）+ MCP Server 接口 + 安全防护 + 可观测性 + 成本监控 |

#### 里程碑 3 交付物（第 8 周末）
- [ ] 知识库问答 Agent v0.5（GitHub 仓库）
  - LangGraph 多 Agent 工作流（路由 → 检索 → 生成 → 审核）
  - RAG + Reranker + 跨会话长期记忆
  - MCP Server 接口（可被 Claude Desktop / VS Code 等调用）
  - Prompt Injection 防护
  - LangSmith / Langfuse 全链路 Trace
- [ ] Agent 架构设计文档（架构图 + 设计决策说明）

---

## 第四阶段：生产化与服务化（第 9-10 周）

### 学习目标
- 掌握 Agent 服务化的基本工程能力
- 完成知识库问答 Agent 的可使用版本
- **原则：能简则简，一个接口搞定的不拆分**

---

### 第 9 周（14 小时）—— 服务化 + 测试

| 天 | 时长 | 内容 |
|----|------|------|
| 周一 | 1h | **FastAPI 封装**：将 Agent 暴露为 REST API，支持流式响应（SSE） |
| 周二 | 1h | **WebSocket 流式**：实时推送生成进度与中间推理过程 |
| 周三 | 1h | **测试策略**：单元测试（Mock LLM）、集成测试、端到端评估 |
| 周四 | 1h | **向量数据库生产选型**：Qdrant / Weaviate / Pinecone 快速对比（了解即可） |
| 周五 | 1h | **Docker 基础**：编写 Dockerfile + docker-compose.yml（Agent 服务 + 向量数据库） |
| 周六 | 3h | **实践**：FastAPI + WebSocket 封装知识库 Agent，编写核心测试套件 |
| 周日 | 6h | **深度实践**：完整服务化 —— Docker 部署 + API 文档（自动生成）+ 测试通过 + 知识库管理 API（上传 / 删除文档） |

---

### 第 10 周（14 小时）—— 简易 UI + 部署 + v1.0

| 天 | 时长 | 内容 |
|----|------|------|
| 周一 | 1h | **Streamlit 快速搭建**：对话界面 + 知识库文档管理页面（能用就行） |
| 周二 | 1h | **UI 完善**：引用来源高亮展示、对话历史、检索过程可视化 |
| 周三 | 1h | **性能优化**：并行检索、结果缓存、长文档分段处理 |
| 周四 | 1h | **端到端测试**：用真实内部文档场景验证完整流程 |
| 周五 | 1h | **部署上线**：部署到服务器（或内网），配置基本认证 |
| 周六 | 3h | **集成测试 + 修复**：邀请同事测试，收集反馈，修复 Top 3 问题 |
| 周日 | 6h | **知识库问答 Agent v1.0**：最终修复 + 完善项目文档 + 录制 Demo 视频 |

---

## 第五阶段：前沿探索与知识体系（第 11-12 周）

### 学习目标
- 探索 Agent 前沿方向，建立技术视野
- 系统整理知识体系，形成可展示的作品集

---

### 第 11 周（14 小时）—— 前沿 Agent 话题

| 天 | 时长 | 内容 |
|----|------|------|
| 周一 | 1h | **Agent 最新进展**：近期重要论文与开源项目速览（Devin、OpenHands、SWE-Agent 等） |
| 周二 | 1h | **Code Agent 原理**：Coding Assistant 如何工作 —— 规划 + 工具调用 + 上下文管理 + 自我反思 |
| 周三 | 1h | **多模态 Agent**：视觉理解 + 工具调用，GPT-4V / Claude Vision 在 Agent 中的应用 |
| 周四 | 1h | **Agent 自我反思**：Reflexion、Self-Refine 模式 —— 让 Agent 审视并改进自己的输出 |
| 周五 | 1h | **Agent 编排前沿**：DSPy、Semantic Kernel 等新兴框架概览（了解趋势） |
| 周六 | 3h | **实践**：选一个感兴趣的前沿方向，为知识库 Agent 添加对应能力（如 Self-Refine 改进回答质量） |
| 周日 | 6h | **深度探索**：深入一个前沿方向完整实践（如给知识库 Agent 添加多模态理解：解析图片/表格中的信息） |

---

### 第 12 周（14 小时）—— 综合总结 + 知识体系

| 天 | 时长 | 内容 |
|----|------|------|
| 周一 | 1h | 代码整理 + 项目文档完善（README、架构图、API 文档） |
| 周二 | 1h | Agent 架构设计文档定稿（完整架构图 + 设计决策） |
| 周三 | 1h | 知识体系梳理：绘制 Agent 开发技能树 / 思维导图 |
| 周四 | 1h | 撰写技术博客（Agent 核心原理与实践总结） |
| 周五 | 1h | 录制项目演示视频（5 分钟）|
| 周六 | 3h | 项目最终打磨 + GitHub 作品集整理 |
| 周日 | 6h | **里程碑 4 冲刺**：知识库问答 Agent 最终版本 + 复盘 12 周学习历程 + 输出 Agent 开发知识体系文档 |

#### 里程碑 4 交付物（第 12 周末）
- [ ] 知识库问答 Agent v1.0（已部署可用）
  - RAG 知识库检索（+ Reranker + 多路召回）
  - 多 Agent 协作（路由 → 检索 → 生成 → 审核）
  - 跨会话长期记忆
  - MCP Server 接口
  - Agentic RAG（自主决策检索策略）
  - FastAPI 服务 + Streamlit UI
  - RAGAS 评估报告
  - Prompt Injection 防护 + 全链路 Trace
- [ ] 完整 GitHub 作品集（README、架构图、Demo 视频）
- [ ] Agent 开发知识体系文档（技能树 / 思维导图）
- [ ] 1 篇技术博客

---

## 主线项目：内部知识库问答 Agent 版本迭代路线

| 版本 | 周 | 核心能力 | 技术栈 |
|------|----|----------|--------|
| v0.1 | 第 4 周 | 基础 RAG 问答 + 来源引用 | 原生 SDK + Chroma |
| v0.2 | 第 5 周 | + Reranker + Agentic RAG + RAGAS 评估 | 原生 SDK + BGE Reranker |
| v0.3 | 第 6 周 | + LangGraph 工作流 + 跨会话记忆 + 规划能力 | LangGraph + 向量化记忆 |
| v0.4 | 第 7 周 | + 多 Agent 架构（路由/检索/生成/审核） | LangGraph Multi-Agent |
| v0.5 | 第 8 周 | + MCP 接口 + 安全防护 + 可观测性 | MCP + LangSmith |
| v0.8 | 第 9 周 | + FastAPI 服务化 + Docker + 测试 | FastAPI + Docker |
| v1.0 | 第 10 周 | + Streamlit UI + 部署上线 | Streamlit |

---

## 核心技术栈速查

### 必学（Agent 核心原理）

| 类别 | 工具 | 说明 |
|------|------|------|
| LLM API | OpenAI / DeepSeek SDK | 原生调用，理解底层原理 |
| Agent 框架 | LangChain + LangGraph | 主流框架，提升编排效率 |
| 向量数据库 | Chroma（开发）/ Qdrant（生产了解） | RAG 必备 |
| 评估框架 | RAGAS | RAG 质量量化，可验证优化效果 |
| 协议标准 | MCP | Agent 互操作标准，趋势明确 |
| 可观测性 | LangSmith / Langfuse | Agent 调试与推理链路分析 |

### 辅助（能简则简）

| 类别 | 工具 | 说明 |
|------|------|------|
| 服务化 | FastAPI | 一个文件暴露 REST API |
| 前端 UI | Streamlit | 最快的可视化方案，够用就行 |
| 部署 | Docker | 一条命令启动全部服务 |
| 多 Agent 思想 | AutoGen / CrewAI | 仅了解设计思想，不深入使用 |

### 明确不学

| 类别 | 原因 |
|------|------|
| python-docx / Word 模板 | 非 Agent 核心能力，分散注意力 |
| 复杂前端开发 | 与 Agent 学习无关，Streamlit 够用 |
| 标书业务逻辑 | 业务太重，喧宾夺主 |
| 复杂 DevOps | 基础 Docker 即可，不搞 K8s / CI/CD |

### 推荐学习资源
- **官方文档**：LangChain Docs、LangGraph Docs（最权威，优先阅读）
- **论文**：ReAct（2022）、Toolformer（2023）、HuggingGPT（2023）
- **实践参考**：LangChain RAG Tutorial、LangGraph Multi-Agent Examples
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
