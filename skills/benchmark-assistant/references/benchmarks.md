# Benchmark 速查

只收录 5 份源（chapter6 / chapter12 / guidebook / chang-survey / yehudai-survey）中提及的 benchmark。来源用「源 ID + 小节」标注，小节标题均已核对源文件实际文本。

> 说明：部分 benchmark 同时出现在 LLM 评估与 Agent 评估两表中（如 SWE-bench Verified），因各源切入角度不同——guidebook §CODE 把它当作代码基准，chapter6/yehudai-survey 则按 agent 任务来分析。两表各取其视角，不重复展开。

## LLM 评估

| 名称 | 测什么 | 设计要点 | 来源 |
|---|---|---|---|
| MMLU-Pro / MMLU-Redux / Global-MMLU | 知识 | MMLU 的清洗（Redux）/加难（Pro，社区主流替代）/去文化偏（Global）版本；多用于预训练评估与消融 | guidebook §KNOWLEDGE |
| GPQA | 博士级知识 | 生物/化学/物理 PhD 级题目，仅对应领域博士可答；diamond 子集最常用；2023 后开始被污染 | guidebook §KNOWLEDGE |
| HLE（Humanity's Last Exam） | 跨域专家知识与推理 | 2.5K 专家众包题目，跨领域；私有、未破；无快速评分通道，常用 LLM judge 评分，导致各家结果不可比 | guidebook §KNOWLEDGE |
| AIME / MathArena / MATH-500 | 数学 | 奥赛级；AIME 每年更新等难度题，可对比发布年与上一年结果查污染；MathArena 持续收录多场竞赛；MATH-500 为 MATH 的 500 题代表性子集 | guidebook §MATH |
| LiveCodeBench / AiderBench / SWE-bench（Verified） | 代码 | LiveCodeBench 按题目日期划分，可比训练截止前后查污染；AiderBench 取自 Exercism，专测代码编辑与重构；SWE-bench（Verified）测 repo 级 issue 解决（逻辑理解+跨文件编辑+长上下文） | guidebook §CODE |
| HELMET / RULER / NIAH | 长上下文 | NIAH（Needle in a Haystack）2025 已近解决；RULER 加多跳追踪/词频变化，亦近解决；HELMET 聚合 RAG/QA/召回/摘要等多任务为单一数据集，仍有区分力 | guidebook §LONG CONTEXT |
| IFEval / IFBench | 指令遵循 | 可编程验证格式约束（关键词/标点/字数/Markdown/HTML 等），每条约束用专门解析测试检验；罕见地无需 judge 即可得严格分数；IFBench 为 IFEval 的扩展 | guidebook §INSTRUCTION FOLLOWING |

## Agent 评估

| 名称 | 测什么 | 设计要点 | 来源 |
|---|---|---|---|
| GAIA / GAIA2 | 通用助手（推理+工具+检索） | 三级难度（L1 已饱和、L3 仍难）；答案唯一可精确字符串匹配；466 题；GAIA2 升级为移动环境（邮件/消息/日历等 app），并引入歧义/噪声/时序约束/多智能体协作 | chapter6 §评估任务数据集的设计；yehudai-survey §4 Generalist Agent Evaluation；guidebook §ASSISTANT TASKS |
| τ-bench / τ²-bench | 人机交互（航空/零售/电信客服） | 用户模拟器+渐进式信息透露；任务层汇总为二元奖励（便于 Pass^k）；τ²-bench 增量在双控环境（Dual-Control，用户模拟器也能改共享环境）与组合式任务生成 | chapter6 §人机交互型评估环境；yehudai-survey §3.4 Conversational Agents |
| BFCL（v1–v4） | 函数/工具调用 | AST 匹配+执行响应+状态匹配；v1 四类（simple/multiple/parallel/irrelevance）；v2/v3 加多轮、组织工具、多步逻辑（yehudai-survey）；v3 聚焦工具调用、v4 测 web/搜索（guidebook） | chapter12 §12.2；yehudai-survey §2.2 Function Calling & Tool Use；guidebook §TOOL-CALLING |
| WebArena / Mind2Web / WebVoyager | Web 交互 | WebArena 自建可完全复现的沙盒网站（电商/论坛/代码托管等）；Mind2Web 在上百个真实网站上测泛化（离线）；WebVoyager 多模态在线评估（被指性能估计偏乐观，Online-Mind2Web 为更严格的替代） | chapter6 §评估任务数据集的设计；yehudai-survey §3.1 Web Agents |
| OSWorld / OSWorld-Verified | GUI/桌面操作 | OSWorld 配 134 个独立评估函数，完整 OS 权限，跨三个操作系统（研究表明跨 OS 能力强相关）；OSWorld-Verified 修 15 个月使用中暴露的 300+ 问题（环境/任务描述/验证逻辑/初始状态四类），并迁移到 AWS 实现 50 倍并行加速 | chapter6 §评估任务数据集的设计；yehudai-survey §4 Generalist Agent Evaluation |
| Terminal-Bench | CLI/终端 | Docker 容器标准化环境；文件系统状态检查+程序执行功能验证；嵌入金丝雀标识符（canary GUID）使数据泄漏可检测；任务注册表 200+，按技术领域×操作复杂度双维度分层 | chapter6 §评估任务数据集的设计；yehudai-survey §3.2 Software Engineering Agents |
| SWE-bench Verified / Pro | 软件工程（解 GitHub issue） | FAIL_TO_PASS（修复前失败、修复后通过）+ PASS_TO_PASS（修复前后都通过，防引入新 bug）双验证；Verified 由 OpenAI 从 2294 题人工筛至 500 题（29% 通过率）；Pro 含 1865 题人工核验任务、跨 41 仓库，常需多文件编辑、Pass@1 仍低于 25% | chapter6 §评估任务数据集的设计；yehudai-survey §3.2 Software Engineering Agents |
| AndroidWorld | 移动 GUI | 116 个任务×20 个真实应用；参数化模板可批量生成任务变体（防记忆+支持对比实验）；验证基于最终 UI 状态而非操作序列；能力标签矩阵可诊断 transcription/math_counting/complex_ui_understanding 等维度短板 | chapter6 §评估任务数据集的设计 / §从 Benchmark 报告到系统改进 |
| ChatEval / SOTOPIA | 多智能体协作（覆盖薄，仅辅助参考） | ChatEval 评多智能体对话系统质量；SOTOPIA 评社交场景中的智能体互动能力 | chapter12 §12.1.2 主流评估基准概览 |
