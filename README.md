# benchmark-assistant

> A Claude Code skill that guides building, reviewing, and analyzing LLM/agent benchmarks — grounded in 5 reference docs with traceable citations.

一个 Claude Code skill:大模型/智能体 benchmark(评估)方法论助手。所有引导基于 `sources/` 下 5 份参考资料,关键论断标注「源 ID + 小节」,可按需引用原文。不写评估代码、不跑评测,只给可溯源的方法论引导与文档产出。

## 三种模式

唤起后显式选模式,内置受众推断(按用户熟练度调术语深度)。

| 模式 | 做什么 | 产出 |
|---|---|---|
| **构建 benchmark** | 10 步引导(评估对象解耦 → 能力维度 → 数据集设计 → 环境 → 指标 → 评分 → 统计/成本 → 质量控制) | 《评估方案文档》(含数据集规范、Rubric 模板) |
| **复盘自己的项目** | 9 维检查清单逐维度诊断 | 按严重度(🔴🟠🟡)排序的问题清单 |
| **梳理他人的 benchmark** | 5 部分框架拆解 | 结构化梳理笔记 |

## 安装

### 作为 Claude Code 插件(推荐)

```bash
/plugin marketplace add henrydhruba11-rgb/benchmark-assistant
/plugin install benchmark-assistant@benchmark-assistant-marketplace
```

### 手动拷贝(不走插件机制)

```bash
git clone https://github.com/henrydhruba11-rgb/benchmark-assistant
# 用户级(全局可用)
cp -r benchmark-assistant/skills/benchmark-assistant ~/.claude/skills/
# 或项目级
cp -r benchmark-assistant/skills/benchmark-assistant <project>/.claude/skills/
```

重启 Claude Code,说"帮我构建/复盘/梳理一个 benchmark"即自动触发,或直接 `/benchmark-assistant`。

## 结构

```
benchmark-assistant/              # 仓库根 = 插件
  .claude-plugin/
    plugin.json                   # 插件清单
    marketplace.json              # 插件市场清单
  skills/
    benchmark-assistant/          # skill 本体
      SKILL.md                    # 入口:启动菜单、受众推断、模式路由、溯源规则、边界
      references/
        knowledge-map.md          # 主题 -> 源 ID + 小节 索引(溯源骨架)
        design-principles.md      # 跨源提炼的 16 条设计原则
        benchmarks.md             # 常见 benchmark 速查(LLM + agent)
      playbooks/
        build.md                  # 构建模式:10 步引导
        review.md                 # 复盘模式:9 维检查清单
        analyze.md                # 梳理模式:5 部分框架
      sources/                    # 5 份归一化参考资料(只读 .md)
  docs/                           # 设计 spec、实现 plan、验证记录
```

## 知识来源

skill 的知识全部来自 `sources/` 下 5 份资料(归一化为 .md):

| 源 ID | 内容 |
|---|---|
| `chapter6` | Agent 评估(中文教材章) |
| `chapter12` | Agent 评估(中文教材章) |
| `guidebook` | The LLM Evaluation Guidebook(HuggingFace) |
| `chang-survey` | A Survey on Evaluation of Large Language Models(Chang 等, 2024) |
| `yehudai-survey` | A Survey on Evaluation of LLM-based Agents(Yehudai 等, 2026) |

引用一律用源 ID + 小节,不用文件名或作者名。

## 不做哪些(边界)

- 不写评估代码、不执行评测、不调模型 API;
- 用户要写代码/跑评测时婉拒,改产出方法论或伪代码级设计;
- 话题超出 `sources/` 覆盖时明说"参考资料未覆盖",不编造。

## 已知限制

两份 survey(`chang-survey`、`yehudai-survey`)由 PDF 用 pypdf 保底转换,正文有空格粘连(如 `a n dhow`),但小节标题完整可定位。skill 按小节级溯源不受影响,按需引用时会作最小清理。如需更高保真,可用 [MinerU](https://github.com/opendatalab/MinerU) 重新转换后替换 `sources/` 对应文件。

## 许可证

[MIT](LICENSE)
