# 验证记录:benchmark-assistant skill 端到端溯源链

- 验证日期:2026-07-30
- 验证者:独立 verifier(fresh-eyes trace)
- 验证对象:`benchmark-assistant` skill(SKILL.md + playbooks/ + references/ + sources/)
- 验证方法:静态追溯 6 个场景的引用链(playbook 原则编号 -> design-principles.md -> knowledge-map.md -> sources/<id>.md 实际文本与行号)

---

## 场景 1 -- Mode 1(构建):PASS

**路由:**SKILL.md 第 29 行 -> `playbooks/build.md`,执行 10 步引导。

**10 步计数:**build.md 含 Step 1(line 11)/ Step 2(line 17)/ Step 3(line 23)/ Step 4(line 29)/ Step 5(line 35)/ Step 6(line 41)/ Step 7(line 47)/ Step 8(line 53)/ Step 9(line 59)/ Step 10(line 65)。共 10 步。✓

**Step 2(评估对象界定)引用链:**
- build.md line 20:依据「原则 1(chapter6 §引言;yehudai-survey §7 Discussion > Decoupling LLM & Harness Evaluation)」。
- 原则 1 -> `references/design-principles.md` line 7 `### 1. 评估对象解耦:测模型还是测 harness`。✓
- chapter6 §引言 -> knowledge-map §A 标注「chapter6 §引言(`# Agent 的评估` 章首,line 15)」;实读 `sources/chapter6.md` line 15 含「评估的对象不应只是模型,而应是模型与 Harness 的组合体」「模型替换实验(model swap)」。行号精确命中。✓
- yehudai-survey §7 Discussion > Decoupling -> `sources/yehudai-survey.md` line 749 `7 Discussion`、line 842 `Decoupling LLM & Harness Evaluation.`。✓

**额外抽检 2 步:**

*Step 6(指标体系):*
- build.md line 44:依据「原则 12(chapter6 §评估指标体系 ...;guidebook §SAMPLING ...)」。
- 原则 12 -> design-principles.md line 95 `### 12. Pass@k vs Pass^k vs Best@k 不可混用`。✓
- chapter6 §评估指标体系 -> `sources/chapter6.md` line 236 `## 评估指标体系`。✓
- guidebook §SAMPLING -> `sources/guidebook.md` line 1087 `## SAMPLING`。✓

*Step 8(统计与成本):*
- build.md line 56:依据「原则 13(chapter6 §评估结果的统计显著性;guidebook §Statistical validity ...);原则 15(chapter6 §Agent 系统的成本分析 ...)」。
- 原则 13 -> design-principles.md line 104 `### 13. 统计显著性`。✓
- chapter6 §评估结果的统计显著性 -> `sources/chapter6.md` line 522 `## 评估结果的统计显著性`。✓
- guidebook §Statistical validity -> `sources/guidebook.md` line 1510 `## Statistical validity`。✓
- 原则 15 -> design-principles.md line 120 `### 15. 成本非线性增长与优化`。✓
- chapter6 §Agent 系统的成本分析 -> `sources/chapter6.md` line 444 `### Agent 系统的成本分析`。✓

---

## 场景 2 -- Mode 2(复盘):PASS

**路由:**SKILL.md 第 30 行 -> `playbooks/review.md`,9 维检查清单(R1-R9)。

**9 维计数:**review.md 含 R1(line 12)/ R2(line 18)/ R3(line 24)/ R4(line 30)/ R5(line 36)/ R6(line 42)/ R7(line 48)/ R8(line 54)/ R9(line 60)。共 9 维。✓

**R4(指标误用)引用链:**
- review.md line 34:依据「原则 12(chapter6 §评估指标体系 ...;guidebook §SAMPLING ...)」。
- 原则 12 -> design-principles.md line 95。✓
- chapter6 §评估指标体系 -> `sources/chapter6.md` line 236。✓
- guidebook §SAMPLING -> `sources/guidebook.md` line 1087。✓

**额外抽检 1 维 -- R7(可复现性):**
- review.md line 52:依据「原则 14(guidebook §So, you can't reproduce reported model scores?,含 Different code base / Subtle implementation or loading difference / Different prompt / Different normalization)」。
- 原则 14 -> design-principles.md line 111 `### 14. 可复现性`。✓
- guidebook §So, you can't reproduce reported model scores? -> `sources/guidebook.md` line 485 `## So, you can't reproduce reported model scores?`(源文用弯引号 ’,与 knowledge-map 标注一致)。✓

---

## 场景 3 -- Mode 3(梳理):PASS

**路由:**SKILL.md 第 31 行 -> `playbooks/analyze.md`,5 部分框架(F1-F5)。

**5 部分计数:**analyze.md 含 F1(line 12)/ F2(line 19)/ F3(line 27)/ F4(line 33)/ F5(line 39)。共 5 部分。✓

**F1(测什么)-> references/benchmarks.md:**
- analyze.md line 15:已知 benchmark 先查 `references/benchmarks.md`(GAIA / τ-bench / BFCL / OSWorld / SWE-bench Verified / AndroidWorld 等)。
- `references/benchmarks.md` 文件存在。✓
- GAIA 条目 -> `references/benchmarks.md` line 23 `| GAIA / GAIA2 | 通用助手(推理+工具+检索) | 三级难度(L1 已饱和、L3 仍难)... | chapter6 §评估任务数据集的设计;yehudai-survey §4 Generalist Agent Evaluation;guidebook §ASSISTANT TASKS |`。✓

**F4(局限与陷阱)引用链:**
- analyze.md line 34:依据「原则 14 可复现性(guidebook §So, you can't reproduce reported model scores? ...);饱和与污染概念见 guidebook §Important concepts ...+ §MANAGING CONTAMINATION ...」。
- 原则 14 -> design-principles.md line 111。✓
- guidebook §So, you can't reproduce -> `sources/guidebook.md` line 485。✓
- guidebook §Important concepts -> `sources/guidebook.md` line 241 `## Important concepts`。✓
- guidebook §MANAGING CONTAMINATION -> `sources/guidebook.md` line 853 `## MANAGING CONTAMINATION`。✓

---

## 场景 4 -- 产出边界(婉拒写代码):PASS

**检查项:**SKILL.md「产出边界与异常」须明示不写评估代码 / 不执行评测 / 不调模型 API,并改产出方法论。

**证据:**`SKILL.md` line 50-51:
> - 产出方法论文档(评估方案、数据集规范、Rubric 模板、复盘清单、梳理笔记等),用 Write 落地。
> - **不写评估代码、不执行评测、不调模型 API**。用户要写代码/跑评测时婉拒,说明边界,改产出方法论或伪代码级设计。

文字明确无歧义:三条禁止项(写代码 / 跑评测 / 调 API)+ 婉拒 + 替代产出(方法论或伪代码级设计)。✓

---

## 场景 5 -- 溯源(引用原文):PASS

**检查项:**用户追问「依据」时,skill Read `sources/<id>.md` 引用原文;引用须干净(无 U+FFFD);knowledge-map 行号须命中。

**抽检引用:chapter6 §Rubric 四准则。**
- knowledge-map §F 标注:「chapter6 §LLM-as-a-Judge:自动化评估的核心(line 281)> Rubric 四准则(加粗小标题 line 289)」。
- 实读 `sources/chapter6.md` line 281 `### LLM-as-a-Judge:自动化评估的核心`;line 289 `**Rubric 四准则**(Scale AI,"Rubrics as Rewards"):`;lines 291-297 四条准则全文(基于专家指导 / 全面覆盖 / 标准重要性权重 / 自包含评估)。
- 文本干净,无乱码、无 U+FFFD。✓

**U+FFFD 全文扫描:**`sources/chapter6.md` 中 `\xef\xbf\xbd`(U+FFFD)匹配数 = 0。✓

**行号 spot-check(2 处):**
1. knowledge-map 标 chapter6 §评估指标体系 line 236 -> `sources/chapter6.md` line 236 = `## 评估指标体系`。精确命中。✓
2. knowledge-map 标 guidebook §SAMPLING line 1087 -> `sources/guidebook.md` line 1087 = `## SAMPLING`。精确命中。✓

(另复核多条均精确:chapter6 §引言 line 15、§评估结果的统计显著性 line 522、§Agent 系统的成本分析 line 444、guidebook §So, you can't reproduce line 485、§Statistical validity line 1510、§Important concepts line 241、§MANAGING CONTAMINATION line 853、§FUNCTIONAL SCORERS line 1117、§With judge models line 1165、yehudai-survey §7 Discussion line 749 / Decoupling line 842、chang-survey §7 GRAND CHALLENGES line 1525、§3 WHAT TO EVALUATE line 228(标题被拆字 `3W H A T T O E V A L U A T E`,knowledge-map 已注明 garbled)、chapter12 §12.2.6 line 898 / §12.4 line 1832。)

---

## 场景 6 -- 知识边界(只读 sources/):PASS

**检查项:**sources/ 仅含 5 份 .md,无 PDF/JSON/嵌套产物;SKILL.md 明示不读 sources/ 之外。

**sources/ 目录清单(`find -type f`):**
- `sources/chang-survey.md`
- `sources/chapter12.md`
- `sources/chapter6.md`
- `sources/guidebook.md`
- `sources/yehudai-survey.md`
- `sources/.gitkeep`(占位,非知识文件)

共 5 份 .md;无 .pdf / .json / images / 嵌套子目录(`find -type d` 仅 sources/ 自身)。✓

**SKILL.md 明示:**line 43-44:
> - 知识只来自 `sources/*.md`(chapter6 / chapter12 / guidebook / chang-survey / yehudai-survey)。
> - 不读 `sources/` 之外的文件(原始 PDF、JSON、images、auto/ 中间产物)。

显式禁止读 sources/ 之外。✓

---

## 总体结论

**6/6 场景全部 PASS。**

| 场景 | 结果 |
|------|------|
| 1 -- Mode 1 构建(10 步 + 原则/源链) | PASS |
| 2 -- Mode 2 复盘(R4 + R7 原则/源链) | PASS |
| 3 -- Mode 3 梳理(F1 benchmarks.md GAIA + F4 原则 14) | PASS |
| 4 -- 产出边界(婉拒写代码) | PASS |
| 5 -- 溯源(原文干净 + 行号命中) | PASS |
| 6 -- 知识边界(只读 sources/ 5 份 .md) | PASS |

引用链全程可解析:playbook 原则编号 -> design-principles.md(1-16 编号稳定)-> knowledge-map.md(源 ID + 小节 + 行号)-> sources/<id>.md 实际文本。所有 spot-check 行号精确命中,chapter6.md 无 U+FFFD,sources/ 无越界文件。

**遗留说明:**本次为静态溯源验证(读文件 + grep),确认引用结构端到端可解析。完整的动态行为测试(通过 Skill tool 实际唤起 skill、观察其是否真的 Read sources/、是否真的婉拒写代码)建议在 Claude Code 重启后进行,因为本 skill 是会话中途安装的,当前会话内 Skill tool 未必能正确加载其菜单与路由。
