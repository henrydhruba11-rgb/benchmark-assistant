# Benchmark 助手 Skill 设计文档

- **日期**:2026-07-30
- **状态**:已通过设计评审(含落地层修订),待实现
- **作者**:用户 + Claude(协作设计)

## 1. 背景与目标

做一个 Claude Code skill,充当大模型/智能体 benchmark(评估)的小助手。skill 的所有回答与引导都必须基于目录中的参考资料,提供三种能力:

1. **构建 benchmark**:用户从零设计评估时,给予头脑风暴式的引导
2. **复盘自己的项目**:用户已有 benchmark 项目时,给予交互式诊断建议
3. **梳理他人的 benchmark**:用户想理解现有 benchmark 时,及时给出结构化梳理

核心理念:评估是一门学科(chang-survey),skill 的首要价值不是替用户拍板,而是基于参考资料把设计/复盘/梳理的方法论讲清楚,让用户做出有据可循的决策。

## 2. 关键设计决策

| 决策点 | 选择 | 含义 |
|---|---|---|
| 目标受众 | 研究者(研究组 + 更广社区) | 面向做 benchmark 研究的人,术语不嫌专业;但 skill 内置受众推断,据此调深度 |
| 资料溯源 | 关键处标注来源 | 日常用自己话讲(内化自源),关键论断/争议处标源 ID+小节,按需引用原文 |
| 模式触发 | 启动菜单显式选 | skill 唤起后亮菜单,用户选模式;中途换需求可重新确认 |
| 产出边界 | 顾问 + 方法论文档 | 产出评估方案、数据集规范、Rubric 模板、复盘清单等文档;不写评估代码、不跑评测 |

## 3. 架构与文件职责

```
benchmark-skill/            # 项目根 = skill 目录(SKILL.md 在此)
  SKILL.md                  # 入口与路由
  references/
    knowledge-map.md        # 主题 -> 源ID+小节 索引(溯源骨架)
    design-principles.md    # 跨源提炼的设计原则(方法论核心)
    benchmarks.md           # 常见 benchmark 速查(测什么/设计要点/来源)
  playbooks/
    build.md                # 构建 benchmark 的引导流程+问题库
    review.md               # 复盘自己项目的检查清单+评审框架
    analyze.md              # 梳理他人 benchmark 的拆解框架
  sources/                  # 5 份知识来源(只读 .md,见 §7 归一化前置)
    chapter6.md
    chapter12.md
    guidebook.md
    chang-survey.md
    yehudai-survey.md
```

5 份源文件**归一化**为 `sources/` 下的纯 `.md`(原始 PDF / 嵌套 md / JSON 中间产物不在此,见 §7.2)。skill 只读 `sources/*.md`,忽略其他文件;knowledge-map.md 用「源 ID + 小节」定位,确保"按需 Read 源文件引用原文"对所有 5 份都可靠落地。

**SKILL.md**:name/description(决定自动触发;草案见下)、启动菜单(三选一)、受众推断规则、模式路由(按选择加载对应 playbook)、溯源规则、通用约束(始终基于参考资料、产出方法论文档、不写代码不跑评测)。

> name/description 草案:
> - name:`benchmark-assistant`
> - description:`大模型/智能体 benchmark(评估)助手。当用户想构建、复盘或梳理 benchmark/评估项目时使用,基于目录内参考资料给出可溯源的方法论引导。`
> (description 仅用于自动触发;三模式由启动菜单显式选,不靠 description 区分。)

**references/knowledge-map.md**:把评估方法论拆成主题树,每个主题标注「源 ID + 小节」。这是溯源骨架,确保"关键处标注来源"可落地。

**references/design-principles.md**:跨 5 份源提炼的核心原则,每条标来源(见 §5 知识图谱骨架)。

**references/benchmarks.md**:常见 benchmark 速查,分 LLM 评估与 agent 评估两类,每个标注测什么/设计要点/来源。

**playbooks/**:三个模式各自的流程与问题库,SKILL.md 按用户选择加载对应一个,避免全量加载。

## 4. 三个模式的工作流

### 4.1 模式 1 · 构建 benchmark(playbooks/build.md)

头脑风暴式引导,把"造一个 benchmark"拆成一串依次确认的决策,每步给参考依据:

1. **目标与受众**:测 LLM 还是 agent?为谁、发布还是内部用?(受众水平按「开工前询问」确定:推断为主、问为兜底;此步沿用其结论,发现偏差则修正)
2. **评估对象界定**:LLM 能力 / agent / harness 三者解耦--测的是模型还是脚手架?(yehudai-survey、chapter6)
3. **能力维度**:从 taxonomy 选要测的维度(chang-survey 的 What 分类 / yehudai-survey 四核心能力)
4. **数据集设计**:任务描述精确性、难度层次、多样性、防泄漏、可验证性(chapter6 五挑战)
5. **评估环境**:工具调用型/人机交互型、静态/动态(chapter6、yehudai-survey)
6. **指标体系**:过程/结果、Pass@k vs Pass^k vs Best@k、安全合规(chapter6);采样指标 pass@k/maj@n/avg@n(guidebook)
7. **评分方法**:精确匹配 / LLM-as-judge / Rubric 四准则 / 配对 Elo(guidebook、chapter6)
8. **统计与成本**:样本量、噪声带宽、成本预算(chapter6、guidebook)
9. **质量控制**:小样本 gating、金标校准、人工抽检(chapter12、chapter6)
10. **产出**:评估方案文档(可含数据集规范、Rubric 模板)

### 4.2 模式 2 · 复盘自己项目(playbooks/review.md)

交互式评审:用户给项目(文件或描述),skill 按检查清单逐维度诊断,指出问题+风险+改进建议(标来源),产出**按严重度排序的问题清单/复盘报告**。检查维度涵盖:评估对象是否解耦、能力覆盖、数据集五挑战、指标误用(如 Pass@k/Pass^k 混用)、Rubric 四准则、LLM-judge 偏见防范与校准、统计显著性、可复现性(prompt/模板/归一化/种子)、成本、质量迭代。

### 4.3 模式 3 · 梳理他人 benchmark(playbooks/analyze.md)

用户给论文/repo/名称,skill 按框架拆解,产出**结构化梳理笔记**。框架:测什么(能力维度+评估对象)-> 怎么测(环境/数据集/指标/评分)-> 设计取舍(明确vs开放、真实vs可控、防泄漏、可验证性)-> 局限与陷阱(饱和/污染/复现性)-> 可借鉴与外推边界(对你项目的启示)。必要时读用户指向的文件。

三个模式的引导都遵循:一次问一个(或一小簇)问题、多选优先、关键论断标来源、可按需引用原文。

## 5. 知识图谱骨架(references/ 的内容大纲)

统一 5 份源成一棵主题树,每条标来源(用 §7.1 的源 ID);既是 design-principles.md 的内容大纲,也是 knowledge-map.md 的索引结构:

- **A. 评估对象** -- LLM 能力 / agent / harness 解耦(chang-survey、yehudai-survey、chapter6)
- **B. 评什么(能力维度)** -- LLM:NLU/推理/NLG/多语言/事实性、鲁棒/伦理/偏见/可信(chang-survey);agent:规划/工具/自我反思/记忆(yehudai-survey)、工具调用/通用/数据生成(chapter12,多智能体仅 §12.1.2 略提 ChatEval,覆盖薄,作辅助源);通用:知识/数学/代码/长上下文/指令遵循/助手任务(guidebook)
- **C. 怎么评(范式)** -- 环境:工具调用型/人机交互型、静态/动态、gym-like(chapter6、yehudai-survey);粒度:最终回答/逐步/轨迹 × 参考有无(yehudai-survey);log-likelihood vs generative(guidebook)
- **D. 数据集设计** -- 五挑战(明确vs开放、真实vs可控、多样vs系统、成本vs覆盖、防泄漏)、任务描述精确性、难度层次化、可验证性、分布系统性、质量控制与迭代(chapter6、chapter12)
- **E. 指标体系** -- 过程(行动合法率/路径效率/成本延迟)、结果(任务成功率、Pass@k/Pass^k/Best@k)、安全合规、鲁棒性(chapter6);四类自动指标 准确/校准/公平/鲁棒(chang-survey);采样指标 pass@k/maj@n/avg@n(guidebook)
- **F. 评分方法** -- 自动指标(EM/BLEU/ROUGE/TER)、functional scorer(IFEval)、LLM-as-judge(偏见与缓解、多源、jury)、Rubric 四准则、配对 Elo/Bradley-Terry、人工(3H+六准则、arena)、奖励模型(guidebook、chapter6、chang-survey)
- **G. 统计与成本** -- 标准误/置信区间/配对分析/多重比较、成本构成与优化、预算-能力曲线(chapter6、guidebook)
- **H. 可复现性** -- 代码库/实现/加载/prompt/模板/种子差异、归一化、结构化生成(guidebook)
- **I. 从评估到改进** -- 报告解读、假设-实验-验证闭环、内部评估基础设施(消融/AB/特性开关/提示词敏感性)(chapter6)、评估作为学科(chang-survey)
- **J. benchmark 速查(benchmarks.md)** -- LLM:MMLU-Pro/GPQA/HLE/IFEval/AIME/MathArena/LiveCodeBench/SWE-bench/HELMET 等;agent:GAIA/GAIA2/tau-bench/BFCL/WebArena/Mind2Web/OSWorld/Terminal-Bench/SWE-bench Verified 等(yehudai-survey、guidebook、chapter6、chapter12)

每个叶子节点在 knowledge-map.md 里对应到「源 ID + 小节」。

## 6. 启动行为、溯源机制与边界

### 6.1 启动菜单 + 受众推断

skill 被唤起后先亮菜单:

> 来做哪件事?
> 1) **构建 benchmark** -- 从零设计一个评估
> 2) **复盘自己的项目** -- 诊断已有 benchmark
> 3) **梳理他人的 benchmark** -- 理解现有 benchmark
> 选一个,或直接说你的需求。

同时从用户首句话推断熟练度(熟练/中级/新手),据此调术语解释深度与节奏;**推断为主、推断不出则询问**(如"我先按你熟悉 Pass@k 来讲,需要展开吗?")。后续模式沿用其结论,发现偏差就地修正。

### 6.2 溯源机制(落地"关键处标注来源")

- 日常建议用自己话讲(内化自源);
- 关键论断/争议处,用 knowledge-map 定位并标注,如「来源:chapter6 §数据集设计」;
- 用户追问"依据/原文"时,Read `sources/<id>.md` 对应小节,引用原文片段(5 份均为 .md,见 §7.2);
- 引用前若发现乱码或明显笔误,跨源交叉印证或作最小清理,不照搬错误文字;
- 话题超出参考资料覆盖时,明说"参考资料未覆盖",不编造。

### 6.3 边界与异常处理

- 请求超出三模式 -> 归到最近模式,或作通用评估顾问应对;
- 话题不在参考资料内 -> 标注"无源",可给通用建议但不伪装有据;
- 用户要写评估代码/跑评测 -> 婉拒并说明边界,改产出方法论或伪代码级设计;
- 中途换需求 -> 重新确认模式;
- `sources/<id>.md` 缺失/读取失败 -> 提示用户检查 §7.2 归一化前置是否完成。

## 7. 参考资料清单与归一化前置

### 7.1 源 ID 与正本

skill 的知识全部来自以下 5 份资料。为路径稳定与溯源一致,定义规范源 ID,knowledge-map.md 全程用 ID 引用:

| 源 ID | 归一化后正本 | 原始文件 | 内容 | 主要贡献 |
|---|---|---|---|---|
| `chapter6` | `sources/chapter6.md` | `chapter6.md` | Agent 评估(中文教材章) | 评估环境、数据集设计、指标、LLM-as-judge、Rubric、Elo、模型选型、成本、统计显著性、可观测性、benchmark-to-improvement 闭环、内部评估基础设施 |
| `guidebook` | `sources/guidebook.md` | `the-llm-evaluation-guidebook/.../the-llm-evaluation-guidebook (1).md` | LLM 评估指南(HuggingFace) | 为什么评估、2025 benchmark 全景、如何审查 benchmark、可复现性、自建评估、评分方法、统计与成本 |
| `chapter12` | `sources/chapter12.md` | `第十二章 智能体性能评估.md` | Agent 评估(中文教材章) | 三层评估架构、BFCL、GAIA、数据生成质量评估、渐进式评估与质量门槛 |
| `chang-survey` | `sources/chang-survey.md` | `Chang 等 - 2024 - A survey on evaluation of large language models.pdf` | LLM 评估 survey | What/Where/How 三问、能力分类、自动(四类指标)+人工(3H+六准则)+新协议、七大挑战 |
| `yehudai-survey` | `sources/yehudai-survey.md` | `Yehudai 等 - 2026 - A survey on evaluation of LLM-based agents.pdf` | Agent 评估 survey | 五视角分类、四核心能力、五核心维度、三粒度×参考有无、静态vs动态、live benchmark、LLM-vs-harness 解耦、按领域选型(Appendix E) |

### 7.2 归一化前置条件(实现前必须完成)

原始资料形态不一(2 份 PDF、1 份三层嵌套 md、2 份根目录 md),且存在转换中间产物与乱码,直接用作知识源会让溯源断链、检索染噪。实现前必须归一化:

1. **PDF 转 md**:用 MinerU 等工具把 `chang-survey`、`yehudai-survey` 两份 PDF 转成 `.md`(保留小节标题,便于按小节定位)。理由:运行时裸读大 PDF 不可靠(实测会报 "model does not support pdf input" 等错),转 md 后"按需 Read 引用原文"才稳定可靠。
2. **路径拍平**:5 份正本统一放进 `sources/`,用 §7.1 的 ID 作文件名;原始嵌套 md、PDF、`auto/` 下的 `_content_list.json`/`_middle.json`/`_model.json` 等中间产物**不进 sources/**,skill 不读。
3. **乱码修复**:`guidebook` 现有转换产物里 emoji 与智能引号损坏(如 `## ? Takeaways`、`what��s`),需重新干净转换或人工修掉乱码,避免引用带出乱码。
4. **只读规则**:skill 只读 `sources/*.md`;`sources/` 之外的文件(含原始 PDF、JSON、images/)一律忽略。
5. **源数据质量提示**:源文件本身可能有微瑕(如 `chapter6` 第 250 行"两个常被混淆的指标"后实列三条 Pass@k/Pass^k/Best@k),skill 对单一来源的论断应尽量跨源交叉印证,不盲信单处文字。

## 8. 不在范围内(Out of scope)

- 不写评估代码、不执行评测、不调模型 API;
- 不负责把 PDF 转成 md / 清理目录(归一化由用户或实现前置完成,见 §7.2;skill 只消费 `sources/*.md`);
- 不维护动态更新的 benchmark 榜单(知识随 `sources/` 固定,资料更新由用户负责);
- 不替用户做主观判断(如"该测哪个能力"),而是给框架与依据,让用户决策;
- 不覆盖参考资料未涉及的主题(benchmarks.md 只收录 5 份源中提及的 benchmark)。

## 9. 验收标准

- skill 唤起后展示三选一菜单,并能据用户首句话推断受众(推断不出则询问)、调整语气;
- 三个模式各自能跑通对应工作流,产出对应方法论文档;
- 关键论断能标注来源(源 ID + 小节),追问"依据"能从 `sources/<id>.md` 引用原文;
- 5 份源都为可读 `.md` 且位于 `sources/`,PDF/JSON/嵌套产物不被读取;
- 话题超出资料覆盖时,明确告知而非编造;
- 用户要求写评估代码/跑评测时,skill 婉拒并改产出方法论或伪代码级设计;
- SKILL.md 聚焦路由,知识在 references/、流程在 playbooks/,按需加载。
