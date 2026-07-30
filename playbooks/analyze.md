# Playbook · 梳理他人 benchmark

用户给论文 / repo / 名称，按 5 部分框架（F1-F5）拆解他人 benchmark，产出结构化梳理笔记。
引导规则：先确认要梳理的对象（必要时 Read 用户指向的文件或链接），再按框架逐部分填；每条关键判断标来源（源 ID + 小节，可对照 `references/knowledge-map.md`）；关键论断标原则编号，可对照 `references/design-principles.md`。若是已知 benchmark，F1 先查 `references/benchmarks.md` 作对照，避免重述速查表已收录的要点。

> 每部分格式：**提取什么**（该部分要拆解的维度）-> **依据**（原则编号 + 源 ID / 小节，可指向 knowledge-map 章节或 benchmarks.md 条目）。F5 为外推判断，依据指向元层级方法论而非具体维度。

---

## 框架（逐部分拆解）

### F1. 测什么

- **提取什么:**能力维度（对齐 knowledge-map §B：LLM 能力分类 / agent 四核心能力 / 工具调用 / 通用能力维度 / 多智能体）；评估对象（LLM 能力 / agent 整体 / harness，是否做模型替换实验 model swap 区分瓶颈来源）。
- **依据:**knowledge-map §B（chang-survey §3 WHAT TO EVALUATE；yehudai-survey §2 Agent Capabilities Evaluation 四核心能力；guidebook §Benchmarks to know in 2025 通用维度）；评估对象解耦见原则 1（chapter6 §引言；yehudai-survey §7 Discussion > Decoupling LLM & Harness Evaluation）。已知 benchmark 先查 `references/benchmarks.md`（如 GAIA / τ-bench / BFCL / OSWorld / SWE-bench Verified / AndroidWorld 等条目均标注了「测什么」与来源）。

### F2. 怎么测

- **提取什么:**
  - 评估环境（工具调用型 / 人机交互型、静态 / 动态、是否 gym-like；对齐 knowledge-map §C）。
  - 数据集设计（五挑战如何取舍：明确 vs 开放 / 真实 vs 可控 / 多样 vs 系统 / 成本 vs 覆盖 / 防泄漏；对应原则 2-6）。
  - 指标（过程指标 / 结果指标；采样用 Pass@k 测能力上限还是 Pass^k 测稳定性、Best@k 测质量上限；对应原则 12）。
  - 评分方法（自动匹配 EM/BLEU/ROUGE、functional scorer、LLM-as-judge + Rubric、配对比较 Elo/Bradley-Terry、人工评估；对齐 knowledge-map §F）。
- **依据:**knowledge-map §C（chapter6 §自动评估环境；yehudai-survey §5 Core Benchmark Dimensions > Environment + §6 Frameworks for Agent Evaluation > Gym-like Environments）；原则 2-6（chapter6 §任务数据集设计的核心挑战；原则 6 防泄漏另见 guidebook §MANAGING CONTAMINATION）；原则 11、12（chapter6 §评估指标体系，结果与质量指标含 Pass@k / Pass^k / Best@k；guidebook §SAMPLING 采样指标 pass@k / maj@n / cot@n / avg@n）；knowledge-map §F（guidebook §METRICS / §FUNCTIONAL SCORERS / §With judge models；chapter6 §LLM-as-a-Judge：自动化评估的核心 > Rubric 四准则 + 同源模型问题与多源异构评判；chapter6 §配对比较与模型排名）。Rubric 设计遵循原则 9，judge 偏见遵循原则 10。

### F3. 设计取舍

- **提取什么:**明确 vs 开放如何权衡（任务描述精确到可复现但不死板）；真实 vs 可控如何平衡（分层筛选、人工核验、沙盒化）；防泄漏手段（答案独特性 / 附件文件 / 动态参数生成 / 时间新鲜度 / canary GUID）；可验证性如何保证（代码可执行 / 状态检查 / functional scorer 优于模糊匹配）。
- **依据:**原则 2-7（chapter6 §任务数据集设计的核心挑战 / §任务描述的精确性设计 / §任务复杂度的层次化设计 / §可验证性与客观性保障；原则 6 防泄漏另见 guidebook §MANAGING CONTAMINATION；原则 7 可验证性另见 guidebook §FUNCTIONAL SCORERS）。范例：SWE-Bench Verified 用人工筛选平衡真实与可控（benchmarks.md 条目；原则 3），AndroidWorld 参数化模板 + 能力标签矩阵兼顾多样与系统（benchmarks.md 条目；原则 4）。

### F4. 局限与陷阱

- **提取什么:**是否饱和（性能过人类基线、失去区分力）？是否污染（公开数据进训练集、分数虚高）？复现性如何（prompt / 模板 / 归一化 / 种子 / 模型加载细节是否透明）？已知问题（如 OSWorld 的 300+ 问题被 Verified 修复、WebVoyager 性能估计偏乐观、同源 judge 被钻空子）。
- **依据:**原则 14 可复现性（guidebook §So, you can't reproduce reported model scores?，含 Different code base / Subtle implementation or loading difference / Different prompt / Different normalization）；饱和与污染概念见 guidebook §Important concepts（saturation / contamination 定义）+ §MANAGING CONTAMINATION（缓解手段）；数据质量控制与迭代见 chapter6 §数据质量控制与迭代改进；OSWorld-Verified 修 300+ 问题见 benchmarks.md OSWorld 条目（chapter6 §评估任务数据集的设计；yehudai-survey §4 Generalist Agent Evaluation）；WebVoyager 偏乐观见 benchmarks.md WebAgents 条目；同源 judge 偏见见原则 10。

### F5. 可借鉴与外推边界

- **提取什么:**对用户自己项目有何启示（可复用的设计模式 / 可避开的陷阱 / 可借鉴的指标与评分）？结论能外推到哪些场景（同类能力维度 / 同类环境 / 同类评估对象）？不能外推到哪里（不同领域 / 不同 harness / 不同采样口径 / 已饱和或已污染的结论不可外推）？
- **依据:**chapter6 §引言（本章导读：评估体系的首要价值是跟上模型演进，line 23——静态评估集会饱和，评估须嵌入决策闭环）；chang-survey §7 GRAND CHALLENGES AND OPPORTUNITIES FOR FUTURE RESEARCH（Evaluation as a new discipline，line 1525-1528——评估是持续学科，非一次性考试）；持续迭代闭环见原则 16（chapter6 §从 Benchmark 报告到系统改进 > §持续迭代；chang-survey §7）。

---

## 产出模板：结构化梳理笔记

```markdown
# 梳理笔记：<benchmark 名称>

## 对象
- 名称 / 来源（论文 / repo / 链接）：
- 是否已知 benchmark（查 references/benchmarks.md）：☐ 是（条目：____）  ☐ 否
- 评估对象：☐ LLM 能力  ☐ agent 整体  ☐ harness
- 是否做 model swap 区分瓶颈：☐ 是  ☐ 否  ☐ 未说明

## F1. 测什么
- 能力维度（对齐 knowledge-map §B）：
  | 维度 | 覆盖情况 | 来源 |
  |------|----------|------|
  |      |          |      |
- 评估对象说明：

## F2. 怎么测
- 评估环境（knowledge-map §C）：☐ 工具调用型 ☐ 人机交互型 ☐ 静态 ☐ 动态（gym-like）
- 数据集设计（五挑战，原则 2-6）：
  | 挑战 | 取舍方式 | 来源 |
  |------|----------|------|
  | 明确 vs 开放（原则 2） |  |  |
  | 真实 vs 可控（原则 3） |  |  |
  | 多样 vs 系统（原则 4） |  |  |
  | 成本 vs 覆盖（原则 5） |  |  |
  | 防泄漏（原则 6） |  |  |
- 指标（原则 12）：
  - 过程指标：
  - 结果指标：采样 ☐ Pass@k ☐ Pass^k ☐ Best@k（测的是：☐ 能力上限 ☐ 稳定性 ☐ 质量上限）
  - 安全 / 鲁棒性否决项：
- 评分方法（knowledge-map §F）：☐ EM/BLEU/ROUGE ☐ functional scorer ☐ LLM-as-judge + Rubric（原则 9/10）☐ 配对比较（Elo/Bradley-Terry）☐ 人工评估

## F3. 设计取舍
- 明确 vs 开放（原则 2）：
- 真实 vs 可控（原则 3）：
- 防泄漏手段（原则 6）：☐ 答案独特性 ☐ 附件文件 ☐ 动态参数生成 ☐ 时间新鲜度 ☐ canary GUID
- 可验证性（原则 7）：☐ 代码可执行 ☐ 状态检查 ☐ 关键词搜索 ☐ functional scorer
- 其他取舍（难度层次化原则 8、分布系统性等）：

## F4. 局限与陷阱
- 饱和（guidebook §Important concepts）：☐ 已饱和 ☐ 部分饱和（如 GAIA L1）☐ 未饱和 ☐ 未知
- 污染（guidebook §MANAGING CONTAMINATION）：☐ 已污染 ☐ 有缓解手段 ☐ 未知
- 复现性（原则 14）：prompt / 模板 / 归一化 / 种子 / 模型加载是否透明？
- 已知问题（如 OSWorld 300+ 问题被 Verified 修、WebVoyager 偏乐观、同源 judge 偏见原则 10）：

## F5. 可借鉴与外推边界
- 可借鉴（设计模式 / 指标 / 评分 / 防泄漏）：
- 可外推到：
- 不可外推到（不同领域 / harness / 采样口径 / 已饱和或污染的结论）：
- 对自己项目的启示（评估须嵌入决策闭环，原则 16；chapter6 §引言）：

> 每条关键判断标来源（源 ID + 小节，可附原则编号）。
```
