# 自评测:黄金场景套件

dogfooding——这个 skill 教别人"评估是持续学科"(原则 16、gating 5→50→全量),它自己也按这套来。`scenarios.json` 里的每个场景对应 skill 规范里的一条行为承诺(`spec` 字段指到 SKILL.md/playbooks 小节),可判定检查失败时直接定位到规范出处。

## 什么时候跑

| 时机 | 范围 |
|---|---|
| 改了 SKILL.md / playbooks / references 之后 | `--core` 冒烟 5 题(S01/S03/S05/S08/S09) |
| 发布新版本前 | 全量 12 题 + 逐条过 `manual` 项 |
| sources/ 更新后 | 全量(溯源类场景 S04/S05 最易受影响) |

```bash
python tools/run_evals.py --core            # 冒烟(约 5-10 分钟,耗模型调用)
python tools/run_evals.py                   # 全量 12 题
python tools/run_evals.py --only S03,S09    # 指定场景
python tools/run_evals.py --dry-run         # 只看组合的 prompt,不跑
python tools/run_evals.py --cmd "claude -p --dangerously-skip-permissions"  # 换 agent CLI
```

默认用 `kimi -p`(也可用 `--cmd` 换成 claude 等;prompt 追加在命令末尾,或用 `{prompt}` 占位符指定位置),在仓库根目录起全新会话,让 agent 自己 Read SKILL.md 并扮演 skill 回应场景输入——即真实使用路径的模拟。版本横幅/进度行等 CLI 噪音会在判定前剥掉。每题原始回应落盘 `evals/last-run/<id>.txt` 供人工复核。

## 怎么读结果

- 可判定检查(`must_contain_all` / `must_contain_any` / `must_not_contain`):**必要不充分**。过了不代表行为完美,挂了一定是回归。
- `manual` 项:发布前逐条对照 `evals/last-run/` 的原文人工判断(如"菜单没有自行猜模式""诊断按严重度排序")。这是刻意的——语义判断硬编码成字符串匹配会产出大量误报,这正是 skill 里讲的"judge 校准前不放量"(原则 10)。
- 失败定位:按场景的 `spec` 字段回到 SKILL.md/playbooks 对应小节,先确认是 skill 文本变了(改场景)还是行为退了(修 skill)。

## 加新场景

往 `scenarios.json` 加一条:

```json
{
  "id": "S13",
  "title": "一句话说明测什么行为",
  "spec": "SKILL.md §对应小节",
  "prompt": "模拟的用户输入",
  "expect": {
    "must_contain_all": ["必须都出现的字符串"],
    "must_contain_any": [["同组至少出现一个"], ["可多个组"]],
    "must_not_contain": ["出现即失败的字符串"],
    "manual": ["需要人工复核的语义判断"]
  }
}
```

场景编写纪律:一个场景只测一条行为承诺;可判定检查宁缺毋滥(误报多了套件就没人信了);`spec` 必填——没有规范出处的期望是空中楼阁。

## 已知边界

- 结果是单次采样:LLM 有波动,偶发 FAIL 先重跑该题(`--only`)再下结论。要做通过率统计就把同一题跑 N 次自己算 pass@1——目前套件按"单次不过即排查"的保守口径用。
- 不在 CI 里跑(需要 CLI + 模型额度);这是发布前的人工关卡,CI 管静态检查(引用/快照/版本)。
