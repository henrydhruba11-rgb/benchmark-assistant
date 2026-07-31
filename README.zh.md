# benchmark-assistant

[English](README.md) | **中文**

> 一个 Claude Code skill:引导构建、复盘、梳理大模型/智能体 benchmark,基于 5 份参考资料,关键论断可溯源。

`benchmark-assistant` 是大模型/智能体 benchmark(评估)的方法论助手。所有回答基于 `sources/` 下 5 份参考资料,关键论断标注「源 ID + 小节」,可按需引用原文。**不写评估代码、不跑评测、不调模型 API**,只给可溯源的方法论引导与文档产出。

## 三种模式

唤起后显示菜单;启动时一次性推断受众熟练度,据此调整术语深度。

| 模式 | 做什么 | 产出 |
|---|---|---|
| **构建 benchmark** | 10 步引导(评估对象解耦 -> 能力维度 -> 数据集设计 -> 环境 -> 指标 -> 评分 -> 统计/成本 -> 质量控制) | 《评估方案文档》(含数据集规范、Rubric 模板) |
| **复盘自己的项目** | 9 维检查清单逐维度诊断 | 按严重度(🔴🟠🟡)排序的问题清单 |
| **梳理他人的 benchmark** | 5 部分框架拆解 | 结构化梳理笔记 |

## 使用示例

**构建 benchmark**
```
你:我想为客服 agent 建一个 benchmark。
Skill:(模式 1)走 10 步决策——评估对象(LLM/agent/harness 解耦)、能力维度、
     数据集设计(明确vs开放、防泄漏、可验证性)、环境、指标(Pass@k vs Pass^k)、
     评分(Rubric)、统计与成本、质量控制,并产出《评估方案文档》(含数据集规范与 Rubric 模板)。
```

**复盘自己的项目**
```
你:复盘我的 agent 评测:20 个用例,GPT 当 judge 打 1-5 分,没做校准。
Skill:(模式 2)按 9 维诊断,指出"样本量小""judge 未校准""Pass@k/Pass^k 混用"等问题,
     标来源,产出按严重度排序的问题清单。
```

**梳理他人的 benchmark**
```
你:梳理一下 GAIA 这个 benchmark。
Skill:(模式 3)查 references/benchmarks.md 对照,按 5 部分拆解(测什么、怎么测、
     设计取舍、局限、可借鉴),关键判断标来源。
```

**追问依据**
```
你:这条的依据是什么?
Skill:Read sources/<id>.md 对应小节,引用原文片段,标注「源 ID + 小节」。
```

**超出边界**
```
你:帮我写个跑评测的 Python 脚本。
Skill:婉拒(不写代码/不跑评测/不调 API),改为提供方法论或伪代码级设计。
```

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

也兼容 **Codex**、**Gemini CLI** 等其他 agent--仓库已含适配文件(`.codex-plugin/`、`GEMINI.md`、`AGENTS.md`),详见 [AGENTS.md](AGENTS.md)。

## 结构

```
benchmark-assistant/              # 仓库根 = 插件
  .claude-plugin/
    plugin.json                   # 插件清单
    marketplace.json              # 市场清单
  skills/
    benchmark-assistant/          # skill 本体
      SKILL.md                    # 入口:菜单、受众推断、模式路由、溯源规则、边界
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

知识全部来自 `sources/` 下 5 份归一化为 .md 的资料:

| 源 ID | 内容 |
|---|---|
| `chapter6` | Agent 评估(中文教材章) |
| `chapter12` | Agent 评估(中文教材章) |
| `guidebook` | The LLM Evaluation Guidebook(HuggingFace) |
| `chang-survey` | A Survey on Evaluation of Large Language Models(Chang 等, 2024) |
| `yehudai-survey` | A Survey on Evaluation of LLM-based Agents(Yehudai 等, 2026) |

引用一律用源 ID + 小节,不用文件名或作者名。

## 边界

- 不写评估代码、不执行评测、不调模型 API;
- 用户要写代码/跑评测时婉拒,改产出方法论或伪代码级设计;
- 话题超出 `sources/` 覆盖时明说"参考资料未覆盖",不编造。

## 已知限制

两份 survey(`chang-survey`、`yehudai-survey`)由 PDF 用 pypdf 保底转换,正文有空格粘连(如 `a n dhow`),但小节标题完整可定位。按小节级溯源不受影响,按需引用时会作最小清理。

## 致谢与许可证

本 skill 的方法论提炼自以下参考资料。其中 4 份以**原许可证**内置(见 [NOTICE.md](NOTICE.md));仓库的 MIT 许可证仅覆盖 skill 的原创文件(`SKILL.md`、`references/`、`playbooks/`)。

| ID | 作品 | 许可证 | 是否内置 |
|---|---|---|---|
| `chapter6` | Agent 评估章([bojieli/ai-agent-book](https://github.com/bojieli/ai-agent-book)) | Apache-2.0 | ✅ |
| `chapter12` | 智能体性能评估,HelloAgents([datawhalechina/hello-agents](https://github.com/datawhalechina/hello-agents)) | CC BY-NC-SA 4.0 | ✅ |
| `guidebook` | The LLM Evaluation Guidebook,Fourrier 等(HuggingFace) | CC BY-NC-SA 4.0 | ✅ |
| `yehudai-survey` | A Survey on Evaluation of LLM-based Agents,Yehudai 等(ACL 2026) | CC-BY 4.0 | ✅ |
| `chang-survey` | A Survey on Evaluation of Large Language Models,Chang 等(2024) | CC-BY 4.0(arXiv 预印本) | ✅ |

方法论本身的版权归原作者所有。

## 许可证

[MIT](LICENSE)
