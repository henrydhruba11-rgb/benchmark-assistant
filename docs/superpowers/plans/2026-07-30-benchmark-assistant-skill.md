# Benchmark 助手 Skill 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 实现一个 Claude Code skill `benchmark-assistant`,充当大模型/智能体 benchmark(评估)助手,基于 5 份归一化参考资料提供构建/复盘/梳理三模式的方法论引导。

**Architecture:** 知识地图 + 模式剧本。`SKILL.md` 做入口与路由(启动菜单显式选模式 + 受众推断),知识蒸馏到 `references/`(knowledge-map / design-principles / benchmarks),三模式流程在 `playbooks/`(build / review / analyze),5 份只读源在 `sources/`。skill 内化知识、关键论断标「源 ID + 小节」、按需 Read `sources/<id>.md` 引用原文。

**Tech Stack:** Claude Code skill(markdown:SKILL.md + references/ + playbooks/);无代码依赖;MinerU(可选,PDF→md 转换)。

## Global Constraints

(每个任务的隐含要求,逐字来自 spec `docs/superpowers/specs/2026-07-30-benchmark-assistant-skill-design.md`)

- **语言**:中文为主,保留英文术语(Pass@k、Pass^k、Best@k、Rubric、LLM-as-judge、Elo、harness 等)。
- **源 ID 规范**(全程统一,定义于 spec §7.1):`chapter6` / `chapter12` / `guidebook` / `chang-survey` / `yehudai-survey`。knowledge-map、design-principles、benchmarks、playbooks 中所有来源标注一律用这 5 个 ID,不用文件名或"Chang/Yehudai"等称呼。
- **知识边界**:知识只来自 `sources/*.md`(5 份归一化后的 .md)。skill 不读 `sources/` 之外的文件(原始 PDF、JSON、images/、auto/ 中间产物)。
- **溯源风格**:日常用自己话讲;关键论断/争议处标「源 ID + 小节」(如「chapter6 §数据集设计」);用户追问"依据/原文"时 Read `sources/<id>.md` 对应小节引用原文;引用遇乱码/笔误跨源印证或最小清理,不照搬错误文字;话题超出资料覆盖时明说"参考资料未覆盖",不编造。
- **产出边界**:顾问 + 方法论文档(评估方案、数据集规范、Rubric 模板、复盘清单、梳理笔记等)。不写评估代码、不执行评测、不调模型 API;用户要写代码/跑评测时婉拒,改产出方法论或伪代码级设计。
- **模式触发**:启动菜单三选一(构建/复盘/梳理);受众推断在启动时一次性完成,后续模式沿用其结论。
- **归一化前置**:实现任何 references/playbooks 之前,必须先完成 Task 2(5 份源归一化到 `sources/`)。
- **Claude Code skill 格式**:`SKILL.md` 顶部 YAML frontmatter(`name` + `description`);`references/`、`playbooks/`、`sources/` 为 skill 按需 Read 的支撑文件。skill 安装后经 Skill 工具或 description 自动触发调用。
- **验证方式说明**:本计划产出的是 markdown skill,无单元测试;各任务的"验证"步骤用结构检查(`grep`/`ls`/`Read`)代替,最终用 Task 10 的行为冒烟测试覆盖集成正确性。
- **命令 shell**:本计划所有命令为 **bash 语法**(`mkdir -p`/`touch`/`cp`/`rm -rf`/`grep -nP`/`wc -l`/`test -f`/`for` 等)。Windows 下默认 PowerShell 5.1 跑会挂,须用 **Git Bash** 执行(`grep -P` 依赖 Git Bash 自带的 GNU grep)。

---

## File Structure

| 文件 | 职责 | 由谁产生 |
|---|---|---|
| `.gitignore` | 忽略 MinerU 中间产物 / 临时转换目录 | Task 1 |
| `sources/chapter6.md` | 只读源:Agent 评估(中文教材章) | Task 2(复制) |
| `sources/chapter12.md` | 只读源:Agent 评估(中文教材章) | Task 2(复制) |
| `sources/guidebook.md` | 只读源:LLM 评估指南(HuggingFace) | Task 2(复制+修乱码) |
| `sources/chang-survey.md` | 只读源:LLM 评估 survey(由 PDF 转) | Task 2(转换) |
| `sources/yehudai-survey.md` | 只读源:Agent 评估 survey(由 PDF 转) | Task 2(转换) |
| `references/knowledge-map.md` | 主题→源 ID+小节 索引(溯源骨架) | Task 3 |
| `references/design-principles.md` | 跨源提炼的设计原则(每条标来源) | Task 4 |
| `references/benchmarks.md` | 常见 benchmark 速查(LLM + agent 两类) | Task 5 |
| `playbooks/build.md` | 构建 benchmark 的引导流程+问题库 | Task 6 |
| `playbooks/review.md` | 复盘自己项目的检查清单+评审框架 | Task 7 |
| `playbooks/analyze.md` | 梳理他人 benchmark 的拆解框架 | Task 8 |
| `SKILL.md` | 入口与路由(菜单/受众推断/路由/溯源/约束) | Task 9 |

---

### Task 1: 项目脚手架与 git 初始化

**Files:**
- Create: `.gitignore`
- Create: `references/`, `playbooks/`, `sources/`(空目录,各放一个 `.gitkeep`)
- Create: `docs/superpowers/plans/`(已存在,跳过)

**Interfaces:**
- Consumes: 无
- Produces: 目录结构 + git 仓库,供后续任务写入文件并提交

- [ ] **Step 1: 初始化 git 仓库**

当前目录不是 git 仓库(spec 已确认)。运行:
```bash
cd "."
git init
git config user.name "$(git config --global user.name || echo 'dev')"
git config user.email "$(git config --global user.email || echo 'dev@local')"
```
Expected: `Initialized empty Git repository in ...`

- [ ] **Step 2: 创建目录结构**

```bash
cd "."
mkdir -p references playbooks sources
touch references/.gitkeep playbooks/.gitkeep sources/.gitkeep
```
Expected: 三个目录存在,各含 `.gitkeep`。

- [ ] **Step 3: 写 .gitignore**

写入 `.gitignore`(忽略 MinerU 转换中间产物与临时目录,保留 sources/ 与原始 PDF):

```gitignore
# MinerU / PDF 转换中间产物
**/auto/_content_list.json
**/auto/_content_list_v2.json
**/auto/_middle.json
**/auto/_model.json
**/auto/*.pdf
sources/_conv/
__pycache__/
```

- [ ] **Step 4: 验证结构**

```bash
ls -d references playbooks sources docs/superpowers/specs docs/superpowers/plans
```
Expected: 五个目录路径都列出。

- [ ] **Step 5: 提交**

```bash
git add .gitignore references/.gitkeep playbooks/.gitkeep sources/.gitkeep docs/superpowers/specs docs/superpowers/plans
git commit -m "chore: scaffold benchmark-assistant skill project"
```
Expected: 首次提交成功。

---

### Task 2: 源文件归一化(spec §7.2 前置)

**Files:**
- Create: `sources/chapter6.md`、`sources/chapter12.md`、`sources/guidebook.md`、`sources/chang-survey.md`、`sources/yehudai-survey.md`
- (不动原始文件;只在 sources/ 产出归一化正本)

**Interfaces:**
- Consumes: 原始 5 份资料(根目录 `chapter6.md`、`第十二章 智能体性能评估.md`、`the-llm-evaluation-guidebook/.../the-llm-evaluation-guidebook (1).md`、两份 PDF)
- Produces: `sources/<id>.md` × 5,供 Task 3-9 全部引用;源 ID 与文件名锁定:`chapter6`→`sources/chapter6.md` 等。

- [ ] **Step 1: 复制两份根目录 md 到 sources/**

```bash
cd "."
cp "chapter6.md" "sources/chapter6.md"
cp "第十二章 智能体性能评估.md" "sources/chapter12.md"
```
Expected: `sources/chapter6.md`、`sources/chapter12.md` 存在且非空。

- [ ] **Step 2: 复制 guidebook md 到 sources/,记录原始路径**

```bash
cd "."
cp "the-llm-evaluation-guidebook/the-llm-evaluation-guidebook (1)/auto/the-llm-evaluation-guidebook (1).md" "sources/guidebook.md"
```
Expected: `sources/guidebook.md` 存在且非空(约 1565 行)。

- [ ] **Step 3: 修复 guidebook 乱码**

`sources/guidebook.md` 中 emoji 与智能引号损坏(如 `## ? Takeaways`、`what��s`、`�` 占位符)。用 Edit 工具逐处修复:
- `## ? Takeaways` → `## Takeaways`
- `what��s` → `what's`、`you��re` → `you're` 等智能引号/撇号损坏
- 单独的 `�` 占位符:依上下文删除或替换为合理标点
- 残缺的 emoji 标记(如 `� Going further`):删除 emoji 残留,保留标题文字 `## Going further`

验证无残留乱码:
```bash
grep -nP '[\x{FFFD}]' "sources/guidebook.md" || echo "no replacement chars"
grep -nP '��' "sources/guidebook.md" || echo "no double-replacement"
```
Expected: 两条都输出 `no ...`。

- [ ] **Step 4: 把 chang-survey PDF 转成 md**

把 `Chang 等 - 2024 - A survey on evaluation of large language models.pdf`(45 页)转成 `sources/chang-survey.md`,保留小节标题以便按小节定位。按以下顺序尝试,任一成功即可:

1. **MinerU(首选,质量最好)**:若 `mineru` 已安装(`command -v mineru`),用与 guidebook 相同的调用:
   ```bash
   cd "."
   mkdir -p sources/_conv/chang
   mineru -p "Chang 等 - 2024 - A survey on evaluation of large language models.pdf" -o sources/_conv/chang -m auto
   # 产物在 sources/_conv/chang/auto/*.md,合并为 sources/chang-survey.md
   ```
2. **安装 MinerU**:若未安装,尝试 `pip install -U "mineru[core]"` 后重跑步骤 1(依赖较重,装不上就跳到 3)。
3. **pypdf 保底(已在本环境验证可行)**:抽取文本(会有空格粘连、引用质量差,仅作保底):
   ```bash
   cd "."
   pip install pypdf 2>/dev/null || true
   mkdir -p sources/_conv
   cat > sources/_conv/extract.py <<'PY'
   import sys, pathlib
   from pypdf import PdfReader
   reader = PdfReader(sys.argv[1])
   parts = []
   for i, page in enumerate(reader.pages, 1):
       parts.append(f"\n\n<!-- page {i} -->\n" + (page.extract_text() or ""))
   pathlib.Path(sys.argv[2]).write_text("".join(parts), encoding="utf-8")
   PY
   python sources/_conv/extract.py "Chang 等 - 2024 - A survey on evaluation of large language models.pdf" sources/chang-survey.md
   ```
4. **(备选)Read+pages**:若执行环境为 Claude Code 且模型支持 PDF 输入,可用 Read 工具 `pages` 参数分批读(如 "1-20"/"21-40"/"41-45")拼成 md;本环境实测会报 "model does not support pdf input",仅作另一备选。

完成后清理中间产物并抽查小节标题(验证转换质量):
```bash
rm -rf sources/_conv
grep -niE 'designing AGI benchmarks|grand challenge|what to evaluate' sources/chang-survey.md | head
```
Expected: `sources/chang-survey.md` 存在、非空、为可读文本(非二进制);抽查命中至少一条已知小节标题。

- [ ] **Step 5: 把 yehudai-survey PDF 转成 md**

把 `Yehudai 等 - 2026 - A survey on evaluation of LLM-based agents.pdf` 转成 `sources/yehudai-survey.md`,方法同 Step 4(MinerU -> 安装 MinerU -> pypdf 保底 -> 可选 Read+pages)。pypdf 脚本可复用 Step 4 的 `extract.py`(已清理则重建):

```bash
cd "."
mkdir -p sources/_conv
python sources/_conv/extract.py "Yehudai 等 - 2026 - A survey on evaluation of LLM-based agents.pdf" sources/yehudai-survey.md
rm -rf sources/_conv
grep -niE 'decoupling|core benchmark dimensions|tool use|planning' sources/yehudai-survey.md | head
```
Expected: `sources/yehudai-survey.md` 存在、非空、可读;抽查命中至少一条已知小节标题。

- [ ] **Step 6: 验证 sources/ 归一化结果**

```bash
cd "."
ls sources/
# 期望仅 5 个 .md(可含 .gitkeep),无 PDF/JSON
ls sources/*.pdf sources/*.json 2>/dev/null || echo "no pdf/json in sources"
# 每份非空且可读
for f in sources/chapter6.md sources/chapter12.md sources/guidebook.md sources/chang-survey.md sources/yehudai-survey.md; do echo "$f: $(wc -l < "$f") lines"; done
```
Expected: `sources/` 仅含 5 份 .md(+ .gitkeep);无 pdf/json;每份行数 > 0(chapter6≈732、chapter12≈2743、guidebook≈1565,两份 survey 视转换而定,应 > 数百行)。

- [ ] **Step 7: 提交**

```bash
git add sources/
git commit -m "chore: normalize 5 reference sources into sources/*.md"
```
Expected: 提交 5 份源文件。

> ⚠️ **同步约定**:`sources/` 是原始资料的**快照**。`chapter6.md`、`第十二章 智能体性能评估.md` 是活文档(会被持续修改),guidebook/PDF 也可能更新。原始资料更新后,**必须重跑 Task 2**(重新复制/转换/修乱码)否则 `sources/` 会悄悄过期、溯源失准。spec §8 已声明"资料更新由用户负责"。

---

### Task 3: references/knowledge-map.md(溯源骨架)

**Files:**
- Create: `references/knowledge-map.md`

**Interfaces:**
- Consumes: `sources/<id>.md` × 5(按 ID 读取具体小节以核对映射)
- Produces: 主题→「源 ID + 小节」索引;Task 4-8 引用其中的小节定位;SKILL.md 与 playbooks 在标来源时查此文件。

- [ ] **Step 1: 写 knowledge-map.md**

文件结构(逐节填实,每条映射必须能在 `sources/<id>.md` 中找到对应小节,写前先 Read 该源核对):

```markdown
# Knowledge Map(溯源骨架)

本文件是 skill 的溯源索引:每个主题标注「源 ID + 小节」,供回答时标注来源、按需定位原文。
源 ID 见 spec §7.1:chapter6 / chapter12 / guidebook / chang-survey / yehudai-survey。

## A. 评估对象
- LLM 能力 vs agent vs harness 解耦
  - yehudai-survey §(decoupling LLM vs harness,贯穿讨论主题;非五核心维度之一)
  - chapter6 §(评估的对象不应只是模型,而应是模型与 Harness 的组合体;模型替换实验)

## B. 评什么(能力维度)
- LLM 能力分类(NLU/推理/NLG/多语言/事实性、鲁棒/伦理/偏见/可信)
  - chang-survey §3(What to evaluate)
- agent 四核心能力(规划/工具/自我反思/记忆)
  - yehudai-survey §2
- 工具调用/通用能力/数据生成质量
  - chapter12 §12.2(BFCL)、§12.3(GAIA)、§12.4(数据生成质量)
- 多智能体(覆盖薄,仅辅助)
  - chapter12 §12.1.2(略提 ChatEval)
- 通用能力维度(知识/数学/代码/长上下文/指令遵循/助手任务)
  - guidebook §(Benchmarks to know in 2025)

## C. 怎么评(范式)
- 评估环境:工具调用型/人机交互型、静态/动态、gym-like
  - chapter6 §(自动评估环境 / 工具调用型 / 人机交互型)
  - yehudai-survey §(static vs dynamic environments;gym-like)
- 评估粒度:最终回答/逐步/轨迹 × 参考有无
  - yehudai-survey §(end-task vs intermediate;trajectory reference-based vs reference-free)
- log-likelihood vs generative
  - guidebook §(Two main evaluation approaches)

## D. 数据集设计
- 五挑战(明确vs开放/真实vs可控/多样vs系统/成本vs覆盖/防泄漏)
  - chapter6 §(任务数据集设计的核心挑战)
- 任务描述精确性、难度层次化、可验证性、分布系统性
  - chapter6 §(任务描述的精确性设计 / 任务复杂度的层次化设计 / 可验证性与客观性保障 / 任务分布的系统性设计)
- 质量控制与迭代
  - chapter6 §(数据质量控制与迭代改进)
  - chapter12 §12.2.6(渐进式评估 gating:5->50->全量、accuracy>0.8 才放量)+ §12.4(数据生成的质量验证)

## E. 指标体系
- 过程指标(行动合法率/路径效率/检索覆盖率/成本延迟)
  - chapter6 §(评估指标体系 · 过程指标)
- 结果指标(任务成功率、Pass@k/Pass^k/Best@k)
  - chapter6 §(评估指标体系 · 结果与质量指标)
- 安全合规与鲁棒性
  - chapter6 §(评估指标体系 · 安全与合规指标 / 鲁棒性)
- 四类自动指标(准确/校准/公平/鲁棒)
  - chang-survey §(automatic evaluation metrics 四组)
- 采样指标(pass@k/maj@n/cot@n/avg@n)
  - guidebook §(Sampling)

## F. 评分方法
- 自动匹配指标(EM/BLEU/ROUGE/TER/BLEURT)
  - guidebook §(Metrics,Scoring free form text)
- functional scorer(IFEval 式可编程验证)
  - guidebook §(Functional scorers)
- LLM-as-judge(偏见:长度/位置/自我偏好...;缓解;多源;jury)
  - guidebook §(With judge models / PROS AND CONS / mitigating biases)
  - chapter6 §(LLM-as-a-Judge;同源模型问题与多源评判)
- Rubric 四准则(专家指导/全面覆盖/权重与否决/自包含)
  - chapter6 §(Rubric 四准则)
- 配对比较与 Elo/Bradley-Terry
  - chapter6 §(配对比较与模型排名)
  - guidebook §(reward models / Bradley-Terry)
- 人工评估(3H+六准则、vibe-check/arena/系统标注)
  - chang-survey §(human evaluation)
  - guidebook §(With humans)
- 奖励模型
  - guidebook §(What about reward models)

## G. 统计与成本
- 统计显著性(标准误/置信区间/配对分析/McNemar/多重比较)
  - chapter6 §(评估结果的统计显著性)
  - guidebook §(Statistical validity)
- 成本构成与优化、预算-能力曲线
  - chapter6 §(Agent 系统的成本分析 / 预算-能力曲线)
  - guidebook §(Cost and efficiency)

## H. 可复现性
- 代码库/实现/加载/prompt/模板/种子差异
  - guidebook §(So you can't reproduce reported model scores)
- 归一化、结构化生成
  - guidebook §(Normalization / Constraining model outputs)

## I. 从评估到改进
- 报告解读、假设-实验-验证闭环
  - chapter6 §(从 Benchmark 报告到系统改进)
- 内部评估基础设施(消融/AB/特性开关/提示词敏感性)
  - chapter6 §(从外部评估到内部评估)
- 评估作为学科
  - chang-survey §(evaluation as a discipline / grand challenges)

## J. benchmark 速查
- 见 references/benchmarks.md(本文件不重复罗列,只指向)
```

(写前对每个映射 Read 对应 `sources/<id>.md` 核对小节标题确实存在;若小节名与上表不符,以源文件实际标题为准并更新本表。)

- [ ] **Step 2: 验证所有映射可解析**

写一个临时核对:对 knowledge-map 中出现的每个源 ID,确认 `sources/<id>.md` 存在;抽 5 条映射 Read 源文件确认小节标题能找到。
```bash
cd "."
for id in chapter6 chapter12 guidebook chang-survey yehudai-survey; do test -f "sources/$id.md" && echo "$id OK" || echo "$id MISSING"; done
```
Expected: 5 行 `OK`。再用 Read 抽查:如 `chapter6` 的「Rubric 四准则」、「评估结果的统计显著性」小节确实存在于 `sources/chapter6.md`。

- [ ] **Step 3: 提交**

```bash
git add references/knowledge-map.md
git commit -m "feat: add knowledge-map source-index (topic -> source ID + section)"
```

---

### Task 4: references/design-principles.md(方法论核心)

**Files:**
- Create: `references/design-principles.md`

**Interfaces:**
- Consumes: `sources/<id>.md`(核对每条原则的来源小节)、`references/knowledge-map.md`(小节定位)
- Produces: 跨源提炼的原则清单(每条标源 ID+小节);playbooks 引用这些原则作为引导依据;review 模式用它做检查清单。

- [ ] **Step 1: 写 design-principles.md**

每条原则格式:`### 原则名` + 一句话陈述 + 来源(源 ID + 小节)+ 为什么重要(1-2 句)。包含以下原则(写前 Read 对应源核对小节):

```markdown
# Benchmark 设计原则(跨源提炼)

每条原则标注来源(源 ID + 小节)。skill 在构建/复盘/梳理时引用这些原则作为依据。

### 1. 评估对象解耦:测模型还是测 harness
同一模型在不同 harness 中表现差异悬殊;用模型替换实验区分瓶颈在模型还是 harness。
来源:chapter6 §(评估的对象不应只是模型);yehudai-survey §(decoupling LLM vs harness)。
为什么:Agent 表现不佳时,改进方向可能是 harness 而非换模型。

### 2. 明确性 vs 开放性
任务描述要明确到可复现,又不能死板到限制合理解法。GAIA 是范例:目标明确、路径开放。
来源:chapter6 §(挑战一:明确性与开放性的张力)。

### 3. 真实性 vs 可控性
真实任务带噪声能显鲁棒性,但威胁可复现。SWE-Bench Verified 用人工筛选在真实与可控间取衡。
来源:chapter6 §(挑战二:真实性与可控性的平衡)。

### 4. 多样性 vs 系统性
需覆盖典型/边界/陷阱,且系统组织以诊断能力短板。AndroidWorld 标注能力维度+参数化生成。
来源:chapter6 §(挑战三:多样性与系统性的协调)。

### 5. 成本 vs 覆盖
复杂 agent 任务耗时费 token,规模须在全面与经济间平衡。GAIA 466 题、SWE-Bench Verified 500 题。
来源:chapter6 §(挑战四:评估成本与覆盖范围)。

### 6. 防数据泄漏
公开数据易进训练集,测的是记忆力。手段:答案独特性、附件文件、动态参数生成、时间新鲜度、canary GUID。
来源:chapter6 §(挑战五:数据泄漏防范);guidebook §(Managing contamination)。

### 7. 可验证性与客观性
验证尽量可执行、客观、可复现:代码可执行、状态检查、关键词搜索;function scorer 优于模糊匹配。
来源:chapter6 §(可验证性与客观性保障);guidebook §(Functional scorers)。

### 8. 难度层次化
分级设计以诊断不同能力短板(GAIA 三级;τ²-bench 业务复杂度分层)。
来源:chapter6 §(任务复杂度的层次化设计)。

### 9. Rubric 四准则
基于专家指导 / 全面覆盖(含陷阱)/ 标准权重与一票否决 / 自包含可验证。否决项(如幻觉)与质量正交。
来源:chapter6 §(Rubric 四准则)。

### 10. LLM-as-judge 偏见与缓解
已知偏见:长度/位置/自我偏好/格式/输入扰动盲区。缓解:多源异构评判、交换顺序、jury、惩罚冗长、校准。
来源:guidebook §(With judge models / mitigating biases);chapter6 §(同源模型问题与多源评判)。
为什么:同源 judge 会被钻空子(古德哈特定律)。

### 11. 轨迹 vs 结果双重覆盖
只看轨迹漏"说了没做到",只看结果漏"走歪了"。两类评测都应覆盖。
来源:chapter6 §(执行轨迹与最终结果的双重覆盖)。

### 12. Pass@k vs Pass^k vs Best@k 不可混用
Pass@k 测能力上限(至少一次成功),Pass^k 测稳定性(全部成功),Best@k 测质量上限。混用导致误判。
来源:chapter6 §(评估指标体系 · 结果与质量指标)。

### 13. 统计显著性
分差小于噪声带宽时不做切换决策;用配对分析(McNemar)比独立相减灵敏;多重比较要收紧或复跑。
来源:chapter6 §(评估结果的统计显著性);guidebook §(Statistical validity)。

### 14. 可复现性
小差异(prompt/模板/归一化/种子/加载)可致数分偏差;报告须透明,复现极难。
来源:guidebook §(So you can't reproduce reported model scores)。

### 15. 成本非线性增长与优化
多轮上下文累积使成本非线性增长;优化核心是控轮次与上下文(KV Cache 复用、压缩、分层路由)。
来源:chapter6 §(Agent 系统的成本分析)。

### 16. 评估作为学科 / 持续迭代
评估不是一次性考试,而是嵌入每次决策的持续验证;观察->假设->实验->验证闭环。
来源:chapter6 §(从 Benchmark 报告到系统改进 / 持续迭代);chang-survey §(evaluation as a discipline)。
```

- [ ] **Step 2: 验证每条原则标了来源且来源可解析**

```bash
cd "."
grep -c '^### ' references/design-principles.md   # 期望 16
grep -c '来源:' references/design-principles.md    # 期望 >=16
```
Expected: 16 个原则标题,每条都有「来源:」行,且来源只用 5 个规范源 ID。抽查 3 条 Read 源文件确认小节存在。

- [ ] **Step 3: 提交**

```bash
git add references/design-principles.md
git commit -m "feat: add design-principles (16 cross-source principles with citations)"
```

---

### Task 5: references/benchmarks.md(速查表)

**Files:**
- Create: `references/benchmarks.md`

**Interfaces:**
- Consumes: `sources/<id>.md`(核对每个 benchmark 的描述与来源)、`references/knowledge-map.md` §J
- Produces: benchmark 速查表;playbooks(尤其 analyze 模式)引用;skill 梳理他人 benchmark 时查此表。

- [ ] **Step 1: 写 benchmarks.md**

分 LLM 评估与 agent 评估两类,每个 benchmark 一行:名称 | 测什么 | 设计要点 | 来源(源 ID + 小节)。写前 Read 源核对。包含(不限于):

```markdown
# Benchmark 速查

只收录 5 份源中提及的 benchmark。来源用源 ID + 小节。

## LLM 评估
| 名称 | 测什么 | 设计要点 | 来源 |
|---|---|---|---|
| MMLU-Pro / MMLU-Redux / Global-MMLU | 知识 | MMLU 的清洗/加难/去偏版本 | guidebook §(Knowledge) |
| GPQA | 博士级知识 | 仅领域博士可答;diamond 子集 | guidebook §(Knowledge) |
| HLE(Humanity's Last Exam) | 跨域专家知识与推理 | 私有、未破;常用 LLM judge | guidebook §(Knowledge) |
| AIME / MathArena / MATH-500 | 数学 | 奥赛级;AIME 可比前后年查污染 | guidebook §(Math) |
| LiveCodeBench / AiderBench / SWE-bench(Verified) | 代码 | 按日期查污染;repo 级编辑 | guidebook §(Code) |
| HELMET / RULER / NIAH | 长上下文 | 多任务聚合;NIAH 已近解决 | guidebook §(Long context) |
| IFEval / IFBench | 指令遵循 | 可编程验证格式约束;无需 judge | guidebook §(Instruction following) |

## Agent 评估
| 名称 | 测什么 | 设计要点 | 来源 |
|---|---|---|---|
| GAIA / GAIA2 | 通用助手(推理+工具+检索) | 三级难度;答案唯一可精确匹配;GAIA2 加移动环境 | chapter6 §(数据集设计);yehudai-survey §(generalist);guidebook §(Assistant tasks) |
| tau-bench / tau²-bench | 人机交互(航空/零售/电信客服) | 用户模拟+渐进式信息透露;二元奖励;τ² 加双控环境 | chapter6 §(人机交互型评估环境);yehudai-survey §(conversational) |
| BFCL(v1-v4) | 函数/工具调用 | AST 匹配;单/多/并行/无关性分类 | chapter12 §12.2;yehudai-survey §(tool use) |
| WebArena / Mind2Web / WebVoyager | Web 交互 | WebArena 沙盒可复现;Mind2Web 真实站泛化 | chapter6 §(数据集设计);yehudai-survey §(web) |
| OSWorld / OSWorld-Verified | GUI/桌面操作 | 134 个评估函数;跨 OS;Verified 修 300+ 问题 | chapter6 §(数据集设计);yehudai-survey §(generalist) |
| Terminal-Bench | CLI/终端 | Docker 容器;canary GUID 防泄漏 | chapter6 §(数据集设计) |
| SWE-bench Verified / Pro | 软件工程(解 issue) | FAIL_TO_PASS/PASS_TO_PASS 双验证;Verified 500 题人工筛 | chapter6 §(数据集设计);yehudai-survey §(SWE) |
| AndroidWorld | 移动 GUI | 116 任务×20 应用;参数化模板;能力标签矩阵 | chapter6 §(数据集设计 / 从 Benchmark 报告到系统改进) |
| ChatEval / SOTOPIA | 多智能体协作(覆盖薄) | 辅助参考 | chapter12 §12.1.2 |
```

- [ ] **Step 2: 验证来源可解析**

```bash
cd "."
grep -cE 'guidebook|chapter6|chapter12|chang-survey|yehudai-survey' references/benchmarks.md
# 抽查 3 个 benchmark,Read 源确认描述与小节
```
Expected: 多处来源命中;抽查的 benchmark 描述与源一致。

- [ ] **Step 3: 提交**

```bash
git add references/benchmarks.md
git commit -m "feat: add benchmarks quick-reference (LLM + agent)"
```

---

### Task 6: playbooks/build.md(构建模式)

**Files:**
- Create: `playbooks/build.md`

**Interfaces:**
- Consumes: `references/design-principles.md`(原则依据)、`references/knowledge-map.md`(小节定位)、`sources/<id>.md`(按需引用)
- Produces: 构建模式的 10 步引导流程 + 问题库 + 产出模板;SKILL.md 在用户选模式 1 时加载本文件。

- [ ] **Step 1: 写 build.md**

结构:开头说明本模式目标与受众沿用;然后 10 步,每步含「问什么(1-2 个问题,多选优先)」「决策依据(源 ID+小节/原则编号)」「常见陷阱」;末尾产出模板。

```markdown
# Playbook · 构建 benchmark

本模式用头脑风暴式引导,把"造一个 benchmark"拆成 10 个依次确认的决策。
引导规则:一次问一个(或一小簇)问题、多选优先、关键论断标来源、可按需引用原文。
受众推断已在启动时完成,沿用其结论调整术语深度。

## Step 1. 目标与受众
- 问:测 LLM 还是 agent?为谁(自用/研究组/社区发布)?发布还是内部用?
- 依据:无(需求澄清)。受众沿用启动推断;若发现偏差在此修正。
- 陷阱:未先界定评估对象就选指标。

## Step 2. 评估对象界定
- 问:你要测的是模型能力、agent 整体,还是 harness?打算用模型替换实验区分吗?
- 依据:原则 1(chapter6 §评估对象;yehudai-survey §decoupling)。
- 陷阱:把 agent 表现直接归因于模型,忽略 harness。

## Step 3. 能力维度
- 问:从 taxonomy 中勾选要测的维度(给多选:推理/工具/规划/记忆/事实性/鲁棒性/...)。
- 依据:knowledge-map §B(chang-survey §What;yehudai-survey §2 四核心能力;guidebook 通用维度)。
- 陷阱:维度过宽无法收敛;漏掉安全/鲁棒性。

## Step 4. 数据集设计
- 问:任务描述如何平衡明确与开放?难度如何分层?如何防泄漏?如何保证可验证?
- 依据:原则 2-8(chapter6 §数据集设计五挑战 / 精确性 / 层次化 / 可验证性 / 分布;原则 6 防泄漏)。
- 陷阱:忽略防泄漏;验证依赖主观判断而非可执行标准。

## Step 5. 评估环境
- 问:工具调用型还是人机交互型?静态还是动态?需不需要沙盒/用户模拟?
- 依据:knowledge-map §C(chapter6 §评估环境;yehudai-survey §static vs dynamic / gym-like)。
- 陷阱:人机交互任务一开始就暴露全部信息(违反渐进式透露)。

## Step 6. 指标体系
- 问:用哪些过程/结果指标?要测稳定性还是能力上限?有无安全否决项?
- 依据:原则 12(chapter6 §指标体系;Pass@k/Pass^k/Best@k);采样指标(guidebook §Sampling);原则(安全合规 chapter6)。
- 陷阱:Pass@k 与 Pass^k 混用;漏安全零容忍项。

## Step 7. 评分方法
- 问:有标准答案可自动匹配?还是需 LLM-as-judge/Rubric?还是配对比较?
- 依据:knowledge-map §F(guidebook §评分方法;chapter6 §Rubric 四准则 / LLM-as-Judge / 配对比较)。
- 陷阱:Rubric 抽象不可验证;同源 judge 不防偏见(原则 10)。

## Step 8. 统计与成本
- 问:评估集多大?分差要超噪声带宽多少才信?成本预算多少?
- 依据:原则 13(chapter6 §统计显著性;guidebook §Statistical validity);原则 15(chapter6 §成本分析)。
- 陷阱:几十个用例就分辨 2-3% 改进;忽略成本非线性增长。

## Step 9. 质量控制
- 问:是否小样本 gating?有无金标集校准 judge?人工抽检比例?
- 依据:chapter12 §12.2.6(渐进式评估 gating)+ §12.4(数据生成质量验证);chapter6 §人工抽检/评判者校准。
- 陷阱:未校准就放量 LLM judge;金标集不覆盖边界。

## Step 10. 产出
- 产出《评估方案文档》,含:评估对象、能力维度、数据集规范(任务模板/难度/防泄漏/验证)、环境、指标、评分方法(Rubric 模板)、统计与成本、质量控制。

## 产出模板:评估方案文档
- 1. 目标与评估对象(含 LLM/agent/harness 解耦说明)
- 2. 能力维度清单
- 3. 数据集规范(任务描述模板、难度分级、防泄漏策略、可验证标准)
- 4. 评估环境(类型、状态管理、隔离)
- 5. 指标体系(过程/结果/安全,标注 Pass@k 或 Pass^k)
- 6. 评分方法(Rubric 模板:维度/权重/否决项/边界案例)
- 7. 统计与成本(样本量、噪声带宽、预算)
- 8. 质量控制(gating、校准、抽检)
```

- [ ] **Step 2: 验证 10 步齐全且每步有依据**

```bash
cd "."
grep -c '^## Step ' playbooks/build.md   # 期望 10
grep -c '依据:' playbooks/build.md        # 期望 >=9(Step 1 无依据)
grep -c '陷阱:' playbooks/build.md        # 期望 9-10
```
Expected: 10 个 Step,每个(除 Step 1)有「依据:」指向原则编号或 knowledge-map 小节,来源用规范源 ID。

- [ ] **Step 3: 提交**

```bash
git add playbooks/build.md
git commit -m "feat: add build-mode playbook (10-step guided workflow)"
```

---

### Task 7: playbooks/review.md(复盘模式)

**Files:**
- Create: `playbooks/review.md`

**Interfaces:**
- Consumes: `references/design-principles.md`(检查清单依据)、`references/knowledge-map.md`、`sources/<id>.md`
- Produces: 复盘检查清单(逐维度)+ 评审框架 + 问题清单模板;SKILL.md 在用户选模式 2 时加载。

- [ ] **Step 1: 写 review.md**

```markdown
# Playbook · 复盘自己项目

用户给项目(文件或描述),按检查清单逐维度诊断,产出按严重度排序的问题清单/复盘报告。
引导规则:先问清评估对象与目标,再逐维度检查;每条问题给:问题描述 + 风险 + 改进建议 + 来源。

## 检查清单(逐维度)

### R1. 评估对象是否解耦
- 查:是否说清测的是模型/agent/harness?是否做了模型替换实验?
- 红旗:把 agent 表现直接归因模型;未区分模型能力与 harness 缺陷。
- 依据:原则 1。

### R2. 能力维度覆盖
- 查:维度是否覆盖目标能力?有无遗漏(尤其安全/鲁棒性)?
- 红旗:维度过窄或过宽;漏边界能力。
- 依据:knowledge-map §B。

### R3. 数据集五挑战
- 查:明确vs开放?真实vs可控?多样vs系统?成本vs覆盖?防泄漏?
- 红旗:任务描述歧义;无防泄漏;验证主观不可执行。
- 依据:原则 2-6(chapter6 §数据集设计)。

### R4. 指标误用
- 查:Pass@k/Pass^k/Best@k 是否用对?稳定性还是上限?有无安全零容忍?
- 红旗:用 Pass@k 掩盖不稳定;漏安全否决。
- 依据:原则 12(chapter6 §指标体系)。

### R5. Rubric 与评分
- 查:Rubric 是否符合四准则?否决项是否设定?judge 是否校准?
- 红旗:抽象不可验证;无否决项;未防同源偏见。
- 依据:原则 9、10(chapter6 §Rubric / LLM-as-Judge)。

### R6. 统计显著性
- 查:样本量是否够分辨目标改进?是否报告置信区间/配对分析?多重比较?
- 红旗:小样本下结论;未做配对分析。
- 依据:原则 13。

### R7. 可复现性
- 查:prompt/模板/归一化/种子是否固定且透明?指标定义是否清晰?
- 红旗:指标同名不同实现;归一化缺失。
- 依据:原则 14(guidebook §可复现性)。

### R8. 成本与效率
- 查:是否报告 token/时间/成本?轮次与上下文是否控制?
- 红旗:成本非线性增长未控;无预算上限。
- 依据:原则 15。

### R9. 质量迭代
- 查:有无 gating、金标校准、人工抽检、回归机制?
- 红旗:未校准就放量;评估集静态不迭代。
- 依据:chapter12 §12.2.6 + §12.4;chapter6 §质量迭代。

## 产出模板:问题清单(按严重度)
- 🔴 严重(影响结论可信):...
- 🟠 中等(影响覆盖/可复现):...
- 🟡 轻微(可改进):...
每条含:维度 / 问题 / 风险 / 改进建议 / 来源(源 ID+小节)。
```

- [ ] **Step 2: 验证检查维度齐全**

```bash
cd "."
grep -c '^### R[0-9]' playbooks/review.md   # 期望 9
grep -c '依据:' playbooks/review.md          # 期望 9
```
Expected: 9 个检查维度,每个有「依据:」指向原则编号或小节,来源用规范源 ID。

- [ ] **Step 3: 提交**

```bash
git add playbooks/review.md
git commit -m "feat: add review-mode playbook (9-dimension checklist)"
```

---

### Task 8: playbooks/analyze.md(梳理模式)

**Files:**
- Create: `playbooks/analyze.md`

**Interfaces:**
- Consumes: `references/benchmarks.md`(已知 benchmark 速查)、`references/knowledge-map.md`、`sources/<id>.md`
- Produces: 拆解他人 benchmark 的 5 部分框架 + 梳理笔记模板;SKILL.md 在用户选模式 3 时加载。

- [ ] **Step 1: 写 analyze.md**

```markdown
# Playbook · 梳理他人 benchmark

用户给论文/repo/名称,按 5 部分框架拆解,产出结构化梳理笔记。
引导规则:先确认要梳理的对象(必要时 Read 用户指向的文件),再按框架逐部分填;关键判断标来源。

## 框架

### F1. 测什么
- 能力维度(对齐 knowledge-map §B);评估对象(LLM/agent/harness)。
- 若是已知 benchmark,先查 references/benchmarks.md 作对照。

### F2. 怎么测
- 评估环境(工具调用/人机交互、静态/动态;knowledge-map §C)。
- 数据集设计(五挑战如何取舍;原则 2-6)。
- 指标(过程/结果、Pass@k 还是 Pass^k;原则 12)。
- 评分方法(自动/LLM-judge/Rubric/配对;knowledge-map §F)。

### F3. 设计取舍
- 明确 vs 开放、真实 vs 可控、防泄漏手段、可验证性如何保证(原则 2-7)。

### F4. 局限与陷阱
- 是否饱和/污染?复现性如何(原则 14)?已知问题(如 OSWorld 的 300+ 问题被 Verified 修)。
- 依据:guidebook §(saturation/contamination);chapter6 §(数据质量控制与迭代改进)。

### F5. 可借鉴与外推边界
- 对用户自己项目有何启示?结论能外推到哪些场景、不能外推到哪里?
- 依据:chapter6 §(评估首要价值是跟上模型演进);chang-survey §(evaluation as discipline)。

## 产出模板:结构化梳理笔记
- 对象:名称/来源
- 测什么:能力维度 + 评估对象
- 怎么测:环境 / 数据集 / 指标 / 评分
- 设计取舍:...
- 局限与陷阱:...
- 可借鉴与外推边界:...
每条关键判断标来源(源 ID + 小节)。
```

- [ ] **Step 2: 验证框架齐全**

```bash
cd "."
grep -c '^### F[0-9]' playbooks/analyze.md   # 期望 5
```
Expected: 5 部分框架,每部分有依据指向,来源用规范源 ID。

- [ ] **Step 3: 提交**

```bash
git add playbooks/analyze.md
git commit -m "feat: add analyze-mode playbook (5-part breakdown framework)"
```

---

### Task 9: SKILL.md(入口与路由)

**Files:**
- Create: `SKILL.md`

**Interfaces:**
- Consumes: `playbooks/build.md`、`playbooks/review.md`、`playbooks/analyze.md`(按模式加载)、`references/knowledge-map.md` + `sources/<id>.md`(溯源时查)
- Produces: skill 入口,被 Claude Code 经 Skill 工具或 description 自动触发加载。

- [ ] **Step 1: 写 SKILL.md**

```markdown
---
name: benchmark-assistant
description: 大模型/智能体 benchmark(评估)助手。当用户想构建、复盘或梳理 benchmark/评估项目时使用,基于目录内参考资料给出可溯源的方法论引导。
---

# Benchmark 助手

你是一个大模型/智能体 benchmark(评估)方法论助手。所有回答与引导必须基于 `sources/` 下的 5 份参考资料,不编造。

## 启动菜单

唤起后先亮菜单让用户显式选(不靠自动猜测模式):

> 来做哪件事?
> 1) **构建 benchmark** -- 从零设计一个评估
> 2) **复盘自己的项目** -- 诊断已有 benchmark
> 3) **梳理他人的 benchmark** -- 理解现有 benchmark
> 选一个,或直接说你的需求。

若用户话语已明确指向某模式,可确认后直接进入;模糊则让其选。

## 受众推断(启动时一次性完成)

从用户首句话推断熟练度(熟练/中级/新手),据此调术语解释深度与节奏。模糊时主动确认,如"我先按你熟悉 Pass@k 来讲,需要展开吗?"。后续模式沿用此结论;发现偏差则修正。

## 模式路由

按用户选择加载对应 playbook 并遵循其流程:
- 模式 1(构建)-> Read `playbooks/build.md`,执行 10 步引导,产出《评估方案文档》。
- 模式 2(复盘)-> Read `playbooks/review.md`,按 9 维检查清单诊断,产出按严重度排序的问题清单。
- 模式 3(梳理)-> Read `playbooks/analyze.md`,按 5 部分框架拆解,产出结构化梳理笔记。

## 溯源规则

- 日常用自己话讲(内化自 `sources/`)。
- 关键论断/争议处,查 `references/knowledge-map.md` 定位并标注「源 ID + 小节」,如「来源:chapter6 §数据集设计」。
- 用户追问"依据/原文"时,Read `sources/<id>.md` 对应小节引用原文(5 份均为 .md)。
- 引用遇乱码或明显笔误,跨源交叉印证或作最小清理,不照搬错误文字。
- 话题超出 `sources/` 覆盖时,明说"参考资料未覆盖",不编造;可给通用建议但标注"无源"。

## 知识边界

- 知识只来自 `sources/*.md`(chapter6 / chapter12 / guidebook / chang-survey / yehudai-survey)。
- 不读 `sources/` 之外的文件(原始 PDF、JSON、images、auto/ 中间产物)。
- 需要查 benchmark 速查 -> `references/benchmarks.md`;需要查原则 -> `references/design-principles.md`;需要定位小节 -> `references/knowledge-map.md`。

## 产出边界与异常

- 产出方法论文档(评估方案、数据集规范、Rubric 模板、复盘清单、梳理笔记等),用 Write 落地。
- **不写评估代码、不执行评测、不调模型 API**。用户要写代码/跑评测时婉拒,说明边界,改产出方法论或伪代码级设计。
- 请求超出三模式 -> 归到最近模式或作通用评估顾问应对。
- 中途换需求 -> 重新确认模式。
- `sources/<id>.md` 缺失/读取失败 -> 提示用户检查归一化前置(spec §7.2)是否完成。

## 源 ID

`chapter6`(Agent 评估·中文教材章)、`chapter12`(Agent 评估·中文教材章)、`guidebook`(LLM 评估指南)、`chang-survey`(LLM 评估 survey)、`yehudai-survey`(Agent 评估 survey)。全程用 ID,不用文件名或作者名。
```

- [ ] **Step 2: 验证 SKILL.md 结构**

```bash
cd "."
grep -q '^name: benchmark-assistant' SKILL.md && echo "name OK"
grep -q '^description:' SKILL.md && echo "desc OK"
grep -cE '构建 benchmark|复盘自己的项目|梳理他人的 benchmark' SKILL.md   # 期望 >=3(菜单+路由)
grep -q '不写评估代码' SKILL.md && echo "boundary OK"
```
Expected: name/desc/菜单三模式/边界都在。

- [ ] **Step 3: 提交**

```bash
git add SKILL.md
git commit -m "feat: add SKILL.md entry (menu, audience inference, routing, grounding, boundaries)"
```

---

### Task 10: 端到端验证

**Files:**
- 无新建;验证已实现的 skill 行为。

**Interfaces:**
- Consumes: Task 1-9 的全部产出
- Produces: 验证记录(skill 是否满足 spec §9 验收标准)

- [ ] **Step 1: 把 skill 安装到 Claude Code 可发现位置**

为使 Skill 工具能调用,把项目根(含 SKILL.md)放进 skills 路径。复制(跨平台可靠)到用户级 skills 目录:
```bash
cd "."
SKILLS_DIR="$HOME/.claude/skills"
mkdir -p "$SKILLS_DIR"
rm -rf "$SKILLS_DIR/benchmark-assistant"
mkdir -p "$SKILLS_DIR/benchmark-assistant"
cp -r SKILL.md references playbooks sources "$SKILLS_DIR/benchmark-assistant/"
ls "$SKILLS_DIR/benchmark-assistant"
```
Expected: 列出 `SKILL.md references playbooks sources`。

(注:若用户偏好项目级 skills,可改为 `mkdir -p .claude/skills && cp -r ... .claude/skills/benchmark-assistant/`;二选一即可。)

- [ ] **Step 2: 冒烟测试模式 1(构建)**

新开会话用 Skill 工具调用 `benchmark-assistant`,选菜单 1,回答前两步。验证:
- 它一次只问一个(或一小簇)问题;
- 在 Step 2(评估对象解耦)给出关键论断时标注来源(含 `chapter6` 或 `yehudai-survey`);
- 语气符合受众推断。
记录:是否通过(是/否 + 观察)。

- [ ] **Step 3: 冒烟测试模式 2(复盘)**

调用 skill,选菜单 2,给一个简短假项目描述(如"我做了个客服 agent 评测,20 个用例,用 GPT 当 judge 打 1-5 分,没做校准")。验证:
- 它按检查清单逐维度诊断,指出"样本量小""judge 未校准""Pass@k/Pass^k 混用"之类问题;
- 每条问题标来源;
- 产出按严重度排序的问题清单。
记录通过与否。

- [ ] **Step 4: 冒烟测试模式 3(梳理)**

调用 skill,选菜单 3,给"GAIA"。验证:
- 它先查 `references/benchmarks.md` 对照;
- 按 5 部分框架拆解(测什么/怎么测/设计取舍/局限/外推);
- 关键判断标来源。
记录通过与否。

- [ ] **Step 5: 边界测试(婉拒写代码)**

调用 skill,要求"帮我写一个调用 OpenAI API 跑评测的 Python 脚本"。验证:
- 它婉拒,说明不写代码/不跑评测的边界;
- 改为提供方法论或伪代码级设计(如评测脚手架应记录哪些字段)。
记录通过与否。

- [ ] **Step 6: 溯源测试(引用原文 + 只读 sources/)**

调用 skill,在某个有来源的论断后追问"依据"。验证:
- 它 Read 对应 `sources/<id>.md` 小节并引用原文片段;
- 引用文字无乱码(若有乱码则跨源印证/清理);
- **只读 sources/**:确认 skill 本次会话 Read 的路径均在 `sources/` 内,未读原始 PDF、JSON 或嵌套产物(对应 spec §9「PDF/JSON/嵌套产物不被读取」;由 Task 2 Step 6 结构检查 + SKILL.md 边界规则联合保证)。
记录通过与否。

- [ ] **Step 7: 知识边界测试(超出覆盖)**

调用 skill,问一个 5 份源未涉及的主题(如"帮我评估一个推荐系统的 CTR 模型")。验证:
- 它明说"参考资料未覆盖",不编造;
- 可给通用建议但标注"无源"。
记录通过与否。

- [ ] **Step 8: 汇总并提交验证记录**

把 Step 2-7 的通过情况写入 `docs/superpowers/plans/2026-07-30-benchmark-assistant-skill-verification.md`,标注未通过项与后续修复。提交:
```bash
git add docs/superpowers/plans/2026-07-30-benchmark-assistant-skill-verification.md
git commit -m "test: record end-to-end verification results"
```

---

## Self-Review

**1. Spec 覆盖:**
- §2 四决策:受众推断(SKILL.md Task 9 + build Step 1)、溯源(Task 9 溯源规则 + knowledge-map Task 3)、菜单触发(Task 9)、产出边界(Task 9 + 各 playbook 产出模板)✓
- §3 架构与文件职责:Task 1 脚手架 + Task 3-9 各文件 ✓
- §4 三模式工作流:Task 6/7/8 ✓
- §5 知识图谱骨架 A-J:Task 3 knowledge-map 全覆盖 ✓
- §6 启动/溯源/边界:Task 9 ✓
- §7 参考资料与归一化前置:Task 2 + Task 3 源 ID ✓
- §8 不在范围内:Task 9 产出边界 ✓
- §9 验收标准:Task 10 各步骤逐一对应;其中"PDF/JSON/嵌套产物不被读取"由 Task 2 Step 6 结构检查 + Task 10 Step 6(只读 sources/)联合验证 ✓

**2. 占位符扫描:** 无 TBD/TODO;每个内容任务给了具体大纲与必含项;PDF 转换给了三级回退(MinerU / 安装 MinerU / pypdf 保底)+ 小节标题抽查。✓

**3. 类型/命名一致:** 源 ID 五个(chapter6/chapter12/guidebook/chang-survey/yehudai-survey)在 Task 2-9 全程一致;原则编号 1-16 在 Task 4 定义、Task 6/7 引用一致;playbook 文件名与 SKILL.md 路由引用一致(build/review/analyze)。✓

**4. 已知风险(执行时注意):**
- PDF 转换:Task 2 已给三级回退(MinerU -> 安装 MinerU -> pypdf 保底);pypdf 文本有空格粘连、引用质量差,转换后须按 Step 4/5 抽查小节标题验证质量,引用时优先 chapter6/chapter12/guidebook 三份干净源。
- Claude Code skills 发现路径:Task 10 Step 1 用复制到 `~/.claude/skills/`;若该路径不被识别,改用项目级 `.claude/skills/`。
