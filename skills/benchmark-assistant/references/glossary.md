# 术语表(Glossary)

skill 在向新手/中级受众解释时,引用本表给出白话定义(熟练档可跳过)。每条标注来源(源 ID + 小节)。

## 评估对象

- **harness(脚手架)** - 包裹模型的外层工程:提示词、工具、记忆、反馈循环等。同一个模型换不同 harness,表现可能差很多。来源:chapter6 §引言。
- **model swap(模型替换实验)** - 固定 harness 只换模型,看分数变化。换强模型分数不涨=瓶颈在 harness;分数大跌=瓶颈在模型。来源:chapter6 §引言。
- **评估对象解耦** - 区分"测的是模型能力、agent 整体、还是 harness"。不区分会把 harness 缺陷误当模型不行。来源:chapter6 §引言;yehudai-survey §7 Decoupling。

## 指标

- **Pass@k** - 跑 k 次,**至少成功一次**的概率。回答"能不能做到"(测能力上限)。来源:chapter6 §评估指标体系。
- **Pass^k** - 跑 k 次**全部成功**的概率。回答"稳不稳定"(测可靠性,回归测试用)。来源:chapter6 §评估指标体系。
- **Best@k** - k 次里**最好一次**的得分(不是是否成功)。测"给足机会后的质量上限"。来源:chapter6 §评估指标体系。
- **二元奖励** - 全部检查通过才得 1 分,任何一项不过就是 0。便于统计 Pass^k,但"对 99% 但漏一字段"和"完全失败"同分。来源:chapter6 §人机交互型评估环境。
- **轨迹(trajectory)vs 结果(outcome)** - 轨迹=agent 过程中做了什么;结果=系统最终变成什么样。两者要都覆盖:只看轨迹漏"说了没做到",只看结果漏"走歪了"。来源:chapter6 §评估指标体系。

## 评分方法

- **精确字符串匹配(exact match)** - 模型最终答案与标准答案逐字符比对,完全一致才过。客观可复现,但格式略有出入就算错。来源:chapter6 §任务描述的精确性设计。
- **functional scorer(可编程验证)** - 不比对文本,而是检查输出是否满足可编程约束(如"恰好 3 个 bullet""JSON 结构合法")。比模糊匹配客观,无需 judge。来源:guidebook §FUNCTIONAL SCORERS。
- **LLM-as-judge** - 用一个 LLM 当评委给输出打分。能评开放式任务,但有偏见(偏长答案、偏位置、自我偏好等),需多源评判缓解。来源:guidebook §With judge models;chapter6 §LLM-as-a-Judge。
- **Rubric(评分准则)+ 四准则** - 结构化评分标准。四准则:基于专家指导、全面覆盖(含陷阱)、标准权重与一票否决、自包含可验证。来源:chapter6 §Rubric 四准则。
- **配对比较 / Elo / Bradley-Terry** - 两两对决挑更好者,不依赖绝对分数。Elo 用胜负给排名;Bradley-Terry 是其统计基础。位置偏差要交换顺序各评一次。来源:chapter6 §配对比较与模型排名。

## 数据集设计

- **饱和(saturation)** - 模型性能已过人类基线或都接近满分,benchmark 失去区分不同模型的能力。来源:guidebook §Important concepts。
- **污染(contamination)** - 评估数据进了模型训练集,分数虚高,测的是记忆力不是能力。来源:guidebook §Important concepts;chapter6 §挑战五。
- **防泄漏手段** - 答案独特性(多源组合才能答)、附件文件(网上不存在的 PDF/音频/图片)、动态参数生成(每次随机实例)、时间新鲜度(用训练截止后的新题)、canary GUID(嵌入唯一标记使泄漏可检测)。来源:chapter6 §挑战五;guidebook §MANAGING CONTAMINATION。
- **渐进式信息透露** - 人机交互评估里,模拟用户不一次性说全需求,按 agent 提问逐步透露。更真实,但需用户模拟器剧本保证可复现。来源:chapter6 §人机交互型评估环境。
- **静态 vs 动态环境** - 静态=离线轨迹/缓存页面;动态=agent 操作真的改变环境状态(沙盒/仿真)。动态能暴露长程任务的连锁错误。来源:chapter6 §自动评估环境;yehudai-survey §5 Environment。
- **gym-like 环境** - 仿 OpenAI Gym 的可控交互仿真(Docker、浏览器沙盒等),可重置、可重复、支持并行。来源:yehudai-survey §6 Gym-like Environments。
- **工具调用型 vs 人机交互型** - 前者 agent 调预定义工具完成任务(代码/数据);后者还需与人类用户对话(客服/咨询)。来源:chapter6 §自动评估环境。

## 统计与成本

- **统计显著性 / 标准误** - 成功率受抽样随机波动;标准误≈√(p(1-p)/n)。分差小于噪声带宽(约 2 倍标准误)时不能下"有改进"的结论。来源:chapter6 §评估结果的统计显著性;guidebook §Statistical validity。
- **配对分析(McNemar)** - 同一批任务上逐题比两个配置胜负,扣除了"题目难易"的共同噪声,比"两个独立成功率相减"灵敏。来源:chapter6 §评估结果的统计显著性。
- **成本非线性增长** - 多轮 agent 调用中上下文不断累积,每轮把历史全发一遍,成本随轮次非线性上升;优化靠 KV Cache 复用、上下文压缩、模型分层路由。来源:chapter6 §Agent 系统的成本分析。
- **消融(ablation)** - 逐一关闭某组件看整体性能掉多少,判断该组件的真实贡献。区别于 model swap(换模型)。来源:chapter6 §引言;chapter6 §从外部评估到内部评估 > §消融基础设施。
