# Week {{WEEK_NUM}} · Day {{DAY_NUM}}（{{WEEKDAY}}）— {{TITLE}}

> **目标**：{{GOAL}}  
> **时间**：{{TIME}}  
> **前置条件**：{{PREREQUISITES}}

---

## 零、今日定位：{{POSITIONING_TITLE}}

{{POSITIONING_INTRO}}

| {{BEFORE_LABEL}} | {{AFTER_LABEL}} |
|-------------------|-----------------|
| {{BEFORE_1}} | {{AFTER_1}} |
| {{BEFORE_2}} | {{AFTER_2}} |
| {{BEFORE_3}} | {{AFTER_3}} |

{{POSITIONING_SUMMARY}}

<!--
说明：
- "零"节用于定位当天的学习在整个学习路径中的位置
- 用表格对比"之前做到的"和"今天要做到的"，让学习者清楚进步方向
- 如果是周日的深度研究，同时说明和周六实践的关系
-->

---

## 一、{{THEORY_SECTION_TITLE}}（{{THEORY_TIME}}）

### 1.1 {{THEORY_SUB_1_TITLE}}

{{THEORY_SUB_1_CONTENT}}

### 1.2 {{THEORY_SUB_2_TITLE}}

{{THEORY_SUB_2_CONTENT}}

### 1.3 {{THEORY_SUB_3_TITLE}}

{{THEORY_SUB_3_CONTENT}}

#### 核心概念对比

| 概念 | 说明 | 优点 | 局限 |
|------|------|------|------|
| {{CONCEPT_1}} | {{CONCEPT_1_DESC}} | {{CONCEPT_1_PRO}} | {{CONCEPT_1_CON}} |
| {{CONCEPT_2}} | {{CONCEPT_2_DESC}} | {{CONCEPT_2_PRO}} | {{CONCEPT_2_CON}} |

### 1.4 思考练习

{{THINKING_EXERCISES}}

<!--
说明：
- 理论/研究环节，周六建议 30-60 分钟，周日建议 1-2 小时
- 如果涉及论文精读，提供论文基本信息、带着问题去读的引导、核心要点总结
- 思考练习帮助内化理论，而非被动阅读
-->

---

## 二、{{DESIGN_SECTION_TITLE}}（{{DESIGN_TIME}}）

{{DESIGN_INTRO}}

### 方案对比

| 方面 | 方案 A：{{PLAN_A}} | 方案 B：{{PLAN_B}} |
|------|--------------------|--------------------|
| 原理 | {{PLAN_A_HOW}} | {{PLAN_B_HOW}} |
| 优点 | {{PLAN_A_PRO}} | {{PLAN_B_PRO}} |
| 缺点 | {{PLAN_A_CON}} | {{PLAN_B_CON}} |

### 今日选择

{{DESIGN_DECISION}}

### 项目结构规划

```
projects/{{PROJECT_DIR}}/
├── {{FILE_1}}      ← {{FILE_1_DESC}}
├── {{FILE_2}}      ← {{FILE_2_DESC}}
├── {{FILE_3}}      ← {{FILE_3_DESC}}
└── README.md       ← 项目说明
```

<!--
说明：
- 设计/规划环节，建议 10-20 分钟
- 如果只有一种实现方案，可简化为直接描述设计思路
- 项目结构规划帮助学习者建立工程化意识
-->

---

## 三、Step 1：{{STEP1_TITLE}}（{{STEP1_TIME}}）

{{STEP1_INTRO}}

### 3.1 {{STEP1_SUB_1_TITLE}}

{{STEP1_SUB_1_CONTENT}}

```{{CODE_LANG}}
{{STEP1_CODE_1}}
```

### 3.2 {{STEP1_SUB_2_TITLE}}

{{STEP1_SUB_2_CONTENT}}

```{{CODE_LANG}}
{{STEP1_CODE_2}}
```

<!--
说明：
- 每个 Step 是一个完整的编码任务（如实现一个模块、一个功能）
- 提供代码骨架（带 TODO 注释），让学习者自行填充核心逻辑
- 代码骨架的完整度根据难度调节：越难给越多骨架，越简单给越少
-->

---

## 四、Step 2：{{STEP2_TITLE}}（{{STEP2_TIME}}）

{{STEP2_INTRO}}

### 4.1 核心思路

{{STEP2_CORE_IDEA}}

### 4.2 与 Step 1 的差异

| 方面 | Step 1 | Step 2 |
|------|--------|--------|
| {{DIFF_ASPECT_1}} | {{STEP1_DIFF_1}} | {{STEP2_DIFF_1}} |
| {{DIFF_ASPECT_2}} | {{STEP1_DIFF_2}} | {{STEP2_DIFF_2}} |

### 4.3 代码骨架

```{{CODE_LANG}}
{{STEP2_CODE}}
```

### 4.4 预期运行效果

```
{{STEP2_EXPECTED_OUTPUT}}
```

### 4.5 需要注意的坑

**坑 1：{{PIT_1_TITLE}}**
{{PIT_1_CONTENT}}

**坑 2：{{PIT_2_TITLE}}**
{{PIT_2_CONTENT}}

<!--
说明：
- Step 2 通常在 Step 1 基础上进阶（另一种实现、功能增强等）
- "注意的坑"来自实际踩坑经验，提前预警
- 预期运行效果作为自检参照
- 如果只需要一个 Step，可以删除本节，将编号调整
-->

---

## 五、Step 3：{{STEP3_TITLE}}（{{STEP3_TIME}}）

{{STEP3_INTRO}}

### 5.1 {{STEP3_SUB_1_TITLE}}

{{STEP3_SUB_1_CONTENT}}

### 5.2 自检清单

完成本 Step 后，验证：

- [ ] {{STEP3_CHECK_1}}
- [ ] {{STEP3_CHECK_2}}
- [ ] {{STEP3_CHECK_3}}
- [ ] {{STEP3_CHECK_4}}

<!--
说明：
- Step 3 通常是测试/对比/实验环节
- 自检清单帮助学习者确认是否达标
- 如果不需要第三个 Step，删除本节
- 根据实际需要，可以增加更多 Step（六、七...）
-->

---

## {{NEXT_SECTION_NUM}}、{{DELIVERABLE_OR_EXPERIMENT_TITLE}}（{{DELIVERABLE_TIME}}）

<!--
说明：对于周六文档，本节通常是"总结 + 代码整理"；
      对于周日文档，本节通常是"里程碑交付物"。
      根据转型计划判断当周是否有里程碑交付。
-->

### {{IF_MILESTONE}}里程碑 {{MILESTONE_NUM}} 交付物清单

- [ ] {{DELIVERABLE_1}}
- [ ] {{DELIVERABLE_2}}
- [ ] {{DELIVERABLE_3}}

### {{IF_MILESTONE}}交付物写作/制作指引

{{DELIVERABLE_GUIDANCE}}

### 项目 README.md

为 `projects/{{PROJECT_DIR}}/` 写一份 README，至少包含：

```markdown
# {{PROJECT_NAME}}

## 项目说明
{{PROJECT_DESC}}

## 实现方式
{{IMPLEMENTATIONS}}

## 运行方式
{{RUN_INSTRUCTIONS}}

## 工具/功能列表
{{FEATURE_LIST}}
```

---

## {{NEXT_SECTION_NUM_2}}、延伸思考（完成交付物后如有余力）

### {{EXTENSION_1_TITLE}}

{{EXTENSION_1_CONTENT}}

| 时间 | 进展 | 关联 |
|------|------|------|
| {{EXT_TIMELINE_1}} | {{EXT_EVENT_1}} | {{EXT_RELATION_1}} |
| {{EXT_TIMELINE_2}} | {{EXT_EVENT_2}} | {{EXT_RELATION_2}} |

### 下周预告

{{NEXT_WEEK_PREVIEW}}

<!--
说明：
- 延伸思考为可选内容，完成主要任务后再做
- 帮助学习者建立更广阔的技术视野
- 下周预告帮助建立连续性
-->

---

## {{LAST_SECTION_NUM}}、今日总结

| 时间段 | 内容 | 预计耗时 |
|--------|------|---------|
| {{PERIOD_1}} | {{CONTENT_1}} | {{DURATION_1}} |
| {{PERIOD_2}} | {{CONTENT_2}} | {{DURATION_2}} |
| {{PERIOD_3}} | {{CONTENT_3}} | {{DURATION_3}} |
| {{PERIOD_4}} | {{CONTENT_4}} | {{DURATION_4}} |
| {{PERIOD_5}} | {{CONTENT_5}} | {{DURATION_5}} |
| **合计** | | **{{TOTAL_TIME}}** |

---

> {{CLOSING_REMARK}}

<!--
=== 模板使用说明 ===

1. 适用范围：周六（3 小时）和周日（6 小时）的学习指导文档
2. 占位符替换：将所有 {{...}} 替换为当天实际内容
3. 周六 vs 周日差异：
   - 周六（3h）：偏实践，Step 通常 1-2 个，可省略"里程碑交付物"和"延伸思考"
   - 周日（6h）：理论+实践并重，Step 2-3 个，包含"里程碑交付物"（如该周有里程碑）和"延伸思考"
4. 条件性内容：
   - {{IF_MILESTONE}} 标记的板块仅在当周有里程碑交付时保留
   - "延伸思考"章节在周六文档中可省略
5. 节数调整：
   - 周六推荐 6-8 节（零 ~ 七）
   - 周日推荐 8-10 节（零 ~ 九/十）
   - 保持中文数字编号：零、一、二、三...
6. Step 数量：
   - 周六：1-2 个 Step
   - 周日：2-3 个 Step
   - 每个 Step 对应一个独立的编码任务
7. 代码骨架：
   - 提供带 TODO 注释的骨架代码，让学习者填写核心逻辑
   - 难度越高可提供越完整的骨架
8. 今日总结：必须包含时间分配表格，帮助学习者规划当天节奏
9. 闭合引言（CLOSING_REMARK）：一句话总结当天意义，承上启下

关键结构元素清单：
  ✅ 标题格式：# Week X · Day N（周X）— 标题
  ✅ 引用块：目标、时间、前置条件
  ✅ 零节：今日定位（含对比表格）
  ✅ 理论节：概念讲解 + 对比表格 + 思考练习
  ✅ 设计节：方案对比 + 项目结构
  ✅ Step 节：编码任务 + 代码骨架 + 预期效果 + 踩坑提醒
  ✅ 自检清单：可验证的能力点
  ✅ 交付/总结节：里程碑交付物/代码整理
  ✅ 延伸思考：技术视野拓展 + 下周预告
  ✅ 今日总结：时间分配表格

模板来源：基于 Week1 Day6-Day7 文档结构提炼
-->
