# Changelog

本项目遵循 [Semantic Versioning](https://semver.org/lang/zh-CN/)。语义化约定:知识库内容修正为 patch;skill 行为/结构变化为 minor;原则编号(1-16)等被引用锚点的破坏性变更为 major。

## [0.2.1] - 2026-08-10

对抗式审查(fresh-eyes 独立审查 v0.2.0 四个 commit)后的修复发布。

### Fixed

- **发布盲区**:`.codex-plugin/plugin.json` 与 `gemini-extension.json` 在 0.2.0 漏升版本;`check_versions.py` 从只查 2 个 manifest 扩为查全部 4 个(假绿比没检查更糟)。
- `fetch-sources.sh`:独立安装(`~/.claude/skills/`,无 tools/)下明确退出而非污染环境/假成功;加 `set -euo pipefail`;pypdf 分支改临时文件 + mv,不再往全局 Python 装包;重转限定 `--only chang-survey`(不再误重写 yehudai-survey)。
- `run_evals.py`:preamble 明示"不写任何文件"并给 skill 路径加引号;套件运行前后 diff `git status` 报警子 agent 落盘;`last-run/` 落盘改为**原始**回应(判定用清洁副本),文档不再撒谎;`clean_output` 的 `• ` 剥除限定 kimi 输出(不再误杀合法 bullet)。
- `check_citations.py`:内部标题正则兼容更多结尾;描述词剥除改为仅前缀/后缀(全局 replace 会把"内容"吃成"容");`INTERNAL_IDS` 死代码消除。
- 文档硬编码检查计数("383")改为"数百项",防漂移。

### Added

- NOTICE.md:yehudai-survey 补上 ACL Anthology 正式出处链接,并标注同文 arXiv 预印本是 CC BY-NC-SA(不可替代)。

## [0.2.0] - 2026-08-10

### Added

- 仓库质量关卡(CI):`tools/check_citations.py`(数百项引用图谱检查:源 ID+小节+行号解析、原则编号 1-16 守护、playbook 结构)、`tools/check_snapshot_sync.py`(快照 hash 完整性 + 原文漂移检测)、`tools/check_versions.py`(清单版本一致性),GitHub Actions 每次 push/PR 自动运行。
- `tools/sources-registry.json`:知识库的机器可读单一事实源(源 ID、快照 hash、原始文件、许可证、引用 alias)——新增参考资料 = 注册表条目 + 快照文件。
- `tools/reconvert_surveys.py`:survey 重转管线(pymupdf4llm)。
- 自评测黄金场景套件:`evals/scenarios.json` 12 个场景(每条对应 skill 规范的一处行为承诺)+ `tools/run_evals.py` 运行器(支持 claude/kimi 等 CLI)+ 运行协议(见 `evals/README.md`)。

### Changed

- `chang-survey` / `yehudai-survey` 从 pypdf 保底转换改为 pymupdf4llm:标题规范、无空格粘连乱码;knowledge-map 全部行号重新锚定。
- `chang-survey` 的来源钉死为 arXiv CC-BY 预印本(此前注册信息隐含指向仓库根目录的 Zotero PDF,实为 ACM 正式版,不可再分发)。

### Fixed

- 修复 lint 抓到的既有引用漂移:DIFFERENT PROMPT 533→529、chapter12 多智能体 78-79→74、同源模型评判 372→364、chang-survey「§1 引言」实为摘要、§METRICS 内 Normalization 归属、Bradley-Terry model 措辞。

## [0.1.0] - 2026-07-30

首个公开发布:三模式(构建 10 步引导 / 复盘 9 维清单 / 梳理 F1-F5 框架)、5 份内置参考资料(各保留原许可证)、16 条跨源设计原则、knowledge-map 溯源索引、benchmark 速查表、新手/中级/熟练三档教学协议(例子先行 / 术语防火墙 / 图优先 / teach-back / 理解自检)、Claude Code 插件 + Codex/Gemini 适配。
