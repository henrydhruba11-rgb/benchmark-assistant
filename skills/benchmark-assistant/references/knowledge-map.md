# Knowledge Map（溯源骨架）

本文件是 skill 的溯源索引：每个主题标注「源 ID + 小节」，供回答时标注来源、按需定位原文。
源 ID 见 spec §7.1：chapter6 / chapter12 / guidebook / chang-survey / yehudai-survey。

> 所有映射的小节标题与行号均已核对 `sources/<id>.md` 实际文本，并由 `tools/check_citations.py` 持续校验（含行号锚点）。两份 survey（chang-survey、yehudai-survey）自 2026-08-10 起改用 pymupdf4llm 转换，含规范 Markdown 标题、无拆字乱码；此前 pypdf 版本的空格拆字（如 `3W H A T T O E V A L U A T E`）已消除。chapter6 中的「过程指标」「Rubric 四准则」等为加粗小标题而非独立 `###` 节，已在映射中标注所属父节。

## A. 评估对象

- LLM 能力 vs agent vs harness 解耦
  - yehudai-survey §7 Discussion > Decoupling LLM & Harness Evaluation（line 240；§2 Agent Capabilities Evaluation 开篇 line 24 亦点明 backbone LLM vs agent harness；本主题贯穿全文讨论，非五核心维度之一）
  - chapter6 §引言（章首 line 15：评估的对象不应只是模型，而应是模型与 Harness 的组合体；模型替换实验 model swap；区分模型能力不足 vs Harness 设计缺陷）

## B. 评什么（能力维度）

- LLM 能力分类（NLU/推理/NLG/多语言/事实性、鲁棒/伦理/偏见/可信）
  - chang-survey §3 WHAT TO EVALUATE（line 149；含 §3.1 NLP Tasks / §3.2 Robustness, Ethics, Bias, and Trustworthiness / §3.3-§3.7 等下游领域）
- agent 四核心能力（规划/工具/自我反思/记忆）
  - yehudai-survey §2 Agent Capabilities Evaluation（line 23；含 §2.1 Planning and Multi-Step Reasoning / §2.2 Function Calling & Tool Use / §2.3 Self-Reflection / §2.4 Memory）
- 工具调用/通用能力/数据生成质量
  - chapter12 §12.2 BFCL：工具调用能力评估（line 161）/ §12.3 GAIA：通用 AI 助手能力评估（line 986）/ §12.4 数据生成质量评估（line 1832）
- 多智能体（覆盖薄，仅辅助）
  - chapter12 §12.1.2 主流评估基准概览（line 54；多智能体协作评估 line 74，略提 ChatEval line 78 / SOTOPIA line 79）
- 通用能力维度（知识/数学/代码/长上下文/指令遵循/助手任务）
  - guidebook §Benchmarks to know in 2025（line 253；含 REASONING AND COMMONSENSE / KNOWLEDGE / MATH / CODE / LONG CONTEXT / INSTRUCTION FOLLOWING / TOOL-CALLING / ASSISTANT TASKS 等子节）

## C. 怎么评（范式）

- 评估环境：工具调用型/人机交互型、静态/动态、gym-like
  - chapter6 §自动评估环境（line 67；含 §工具调用型评估环境 line 87 / §人机交互型评估环境 line 106）
  - yehudai-survey §5 Core Benchmark Dimensions > Environment（line 134：static vs dynamic environments）+ §6 Frameworks for Agent Evaluation > Gym-like Environments（line 208）
- 评估粒度：最终回答/逐步/轨迹 × 参考有无
  - yehudai-survey §6 Frameworks for Agent Evaluation（line 161；含 Final-response evaluation line 171 / Stepwise Evaluation line 175 / Trajectory-Based Assessment line 179（同段含 Reference-Based 与 Reference-Free 两类））
- log-likelihood vs generative
  - guidebook §Two main evaluation approaches（line 181；含 §LOG-LIKELIHOOD EVALUATIONS line 189 / §GENERATIVE EVALUATIONS line 223）

## D. 数据集设计

- 五挑战（明确vs开放/真实vs可控/多样vs系统/成本vs覆盖/防泄漏）
  - chapter6 §任务数据集设计的核心挑战（line 164，属 `## 评估任务数据集的设计`）
- 任务描述精确性、难度层次化、可验证性、分布系统性
  - chapter6 §任务描述的精确性设计（line 176）/ §任务复杂度的层次化设计（line 194）/ §可验证性与客观性保障（line 202）/ §任务分布的系统性设计（line 220）
- 质量控制与迭代
  - chapter6 §数据质量控制与迭代改进（line 224）
  - chapter12 §12.2.6 扩展与优化建议（line 898；含渐进式评估 gating：5->50->全量、overall_accuracy > 0.8 阈值，代码示例 line 921-928）+ §12.4 数据生成质量评估（line 1832，整体即数据生成的质量验证流程）

## E. 指标体系

- 过程指标（行动合法率/路径效率/检索覆盖率/成本延迟）
  - chapter6 §评估指标体系（line 236；过程指标为加粗小标题 line 240）
- 结果指标（任务成功率、Pass@k/Pass^k/Best@k）
  - chapter6 §评估指标体系（line 236；结果与质量指标为加粗小标题 line 248，含 Pass@k/Pass^k/Best@k 定义）
- 安全合规与鲁棒性
  - chapter6 §评估指标体系（line 236；安全与合规指标为加粗小标题 line 265，鲁棒性为加粗小标题 line 267）
- 四类自动指标（准确/校准/公平/鲁棒）
  - chang-survey §5.1 Automatic Evaluation（line 707；Table 9 Key Metrics of Automatic Evaluation 列四组：Accuracy / Calibrations / Fairness / Robustness）
- 采样指标（pass@k/maj@n/cot@n/avg@n）
  - guidebook §SAMPLING（line 1087）

## F. 评分方法

- 自动匹配指标（EM/BLEU/ROUGE/TER/BLEURT）
  - guidebook §Evaluation's main challenge: Scoring free form text（line 936）> §METRICS（line 944）
- functional scorer（IFEval 式可编程验证）
  - guidebook §FUNCTIONAL SCORERS（line 1117）
- LLM-as-judge（偏见：长度/位置/自我偏好...；缓解；多源;jury）
  - guidebook §With judge models（line 1165）/ §PROS AND CONS OF USING JUDGE-LLMS（line 1183，含 Self-Preference/Position Bias/Verbosity Bias/Format Bias 等偏见列表）/ §DESIGNING YOUR EVALUATION PROMPT（line 1301）+ §EVALUATING YOUR EVALUATOR（line 1357，缓解与校准）
  - chapter6 §LLM-as-a-Judge：自动化评估的核心（line 281；含同源模型问题与多源评判，line 364）
- Rubric 四准则（专家指导/全面覆盖/权重与否决/自包含）
  - chapter6 §LLM-as-a-Judge：自动化评估的核心（line 281）> Rubric 四准则（加粗小标题 line 289，Scale AI "Rubrics as Rewards"）
- 配对比较与 Elo/Bradley-Terry
  - chapter6 §配对比较与模型排名（line 398）
  - guidebook §WHAT ABOUT REWARD MODELS?（line 1412；含 Bradley-Terry model line 1416）
- 人工评估（3H+六准则、vibe-check/arena/系统标注）
  - chang-survey §5.2 Human Evaluation（line 770）
  - guidebook §With humans（line 1137）
- 奖励模型
  - guidebook §WHAT ABOUT REWARD MODELS?（line 1412；含 How do I use a Reward Model for Evaluation line 1430 / Pros and Cons of Reward Models line 1444）

## G. 统计与成本

- 统计显著性（标准误/置信区间/配对分析/McNemar/多重比较）
  - chapter6 §评估结果的统计显著性（line 522）
  - guidebook §Statistical validity（line 1510）
- 成本构成与优化、预算-能力曲线
  - chapter6 §评估驱动的模型选型（line 419）> §选型的关键维度（line 423，含预算-能力曲线加粗小标题 line 440）+ §Agent 系统的成本分析（line 444，含成本构成要素/成本优化策略/成本监控与预算控制）
  - guidebook §Cost and efficiency（line 1518）

## H. 可复现性

- 代码库/实现/加载/prompt/模板/种子差异
  - guidebook §So, you can't reproduce reported model scores?（line 485；含 §DIFFERENT CODE BASE line 489 / §SUBTLE IMPLEMENTATION OR LOADING DIFFERENCE line 499 / §DIFFERENT PROMPT line 529 / Model loading affects reproducibility line 517 / Few-shots samples line 574 / Parameters line 580）
- 归一化、结构化生成
  - guidebook §So, you can't reproduce reported model scores?（line 485，含 Different normalization line 513）+ §Constraining model outputs（line 1472，结构化生成）+ §METRICS（line 944）内 Normalization 说明（line 1077，预测文本归一化比较）

## I. 从评估到改进

- 报告解读、假设-实验-验证闭环
  - chapter6 §从 Benchmark 报告到系统改进（line 565；含 §读懂 Benchmark 报告 line 575 / §从数据到假设 line 587 / §从结果到决策 line 597 / §持续迭代 line 611）
- 内部评估基础设施（消融/AB/特性开关/提示词敏感性）
  - chapter6 §从外部评估到内部评估：生产级 Agent 的评估基础设施（line 634；含 §消融基础设施 line 638 / §AB 测试方法论 line 644 / §双层特性开关系统 line 656 / §提示词敏感性评估 line 666）
- 评估作为学科
  - chang-survey §7 GRAND CHALLENGES AND OPPORTUNITIES FOR FUTURE RESEARCH（line 876；摘要 line 31 亦提 "evaluation should be treated as an essential discipline"）
- 饱和与污染（saturation / contamination 概念定义）
  - guidebook §Important concepts（line 241；saturation 定义 line 245 / contamination 定义 line 249）；污染缓解手段见 guidebook §MANAGING CONTAMINATION

## J. benchmark 速查

- 见 references/benchmarks.md（本文件不重复罗列，只指向）
