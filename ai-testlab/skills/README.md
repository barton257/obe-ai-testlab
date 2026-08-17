# skills/

可复用的 AI 测试技能。一个目录一个技能。所有 skill 遵循同一结构：`prompt.md`（生成规则）+ `cases/`（历史修正案例）+ `examples/`（示例输入输出）。

## 技能总览

| Skill | 用途 | 输入 | 输出 | 落点目录 |
|---|---|---|---|---|
| [test-strategy-generator](test-strategy-generator/) | 需求 → 完整测试策略（六问 + 矩阵 + 六层 + 非功能 + DoD 映射） | PRD、走查、变更点、审计报告 | `_TEST_STRATEGY.md` | `projects/<x>/docs/` |
| [testcase-generator](testcase-generator/) | 从走查/需求生成结构化 YAML 用例 | 走查产出、审计报告、需求 | `.yaml` 用例文件 | `projects/<x>/testcases/` |
| [bug-writer](bug-writer/) | 现场描述转标准化缺陷报告 | 口述、截图、日志 | `.md` 缺陷文件 | `projects/<x>/bugs/` |
| [walkthrough-recorder](walkthrough-recorder/) | 走查过程整理为审计报告 | 流水、笔记、录音字幕 | `_WALKTHROUGH.md` | `projects/<x>/docs/` |
| [regression-planner](regression-planner/) | 变更点推导回归清单 | PR/commit/需求变更 | `regression-*.md` | `projects/<x>/docs/` |
| [api-test-generator](api-test-generator/) | OpenAPI 生成 pytest 接口用例 | OpenAPI/Swagger | `test_*.py` | `projects/<x>/tests/api/` |

## 各 Skill 状态

| Skill | prompt.md | cases 案例数 | examples | 首个案例时机 |
|---|---|---|---|---|
| test-strategy-generator | ✅ 完整 | 0 | ✅（spartans-subscribe 首个） | 下次 QA 修正生成的策略文档 |
| testcase-generator | ✅ 完整 | **1**（V5 并发订阅双扣） | ✅ | 已有 |
| bug-writer | ✅ 完整 | 0 | ⏳ 待补 | 下次修正 AI bug 报告 |
| walkthrough-recorder | ✅ 完整 | 0 | ⏳ 待补 | 下次整理走查笔记 |
| regression-planner | ✅ 完整 | 0 | ⏳ 待补 | 2026-08-27 上线后复盘 |
| api-test-generator | ✅ 完整 | 0 | ⏳ 待补 | 下次生成新接口测试或对 `test_spartans_api.py` 做回归实验 |

## 触发场景速查

**日常 QA 动作 → 用哪个 skill**：

| 你在做什么 | 用哪个 |
|---|---|
| 收到 PRD、开始新功能测试 | `test-strategy-generator`（先出策略） → `testcase-generator`（展开用例）|
| 拿到走查/审计报告 | `walkthrough-recorder`（整理） → `test-strategy-generator` → `testcase-generator` |
| 走查发现了问题 | `bug-writer`（写缺陷）|
| 收到 PR 通知 | `regression-planner`（列回归清单）|
| 后端给了新接口 | `api-test-generator`（生接口用例）|

**多人格 × 同 skill 组合**：

```
projects/spartans/bots/ 三个人格
        ↓
Kakarotto 走查 ─┐
Vegeta 走查    ─┼─→ walkthrough-recorder → 三份走查报告
Frieza 走查    ─┘                         ↓
                                    testcase-generator
                                          ↓
                                 一批覆盖三视角的 YAML 用例
```

## 结构要求

每个 skill 目录：

```
<skill-name>/
├── README.md        # 用途、输入、输出、限制
├── prompt.md        # 主 prompt（含"扫 cases/"钩子）
├── cases/           # 历史修正案例（AI 学习用）
│   ├── README.md    # 什么时候写案例、特有关注
│   └── YYYY-MM-DD-*.md
└── examples/        # 示例输入输出（可选）
    ├── README.md
    └── ...
```

## 案例归档机制

每个 skill 的 `cases/` 目录记录"AI 首版 → 人工终版 → 修改原因"，让 AI 从修正中学习。

- 触发条件：AI 生成的产物你做了**结构性修改**
- 不触发：措辞润色、单个字段修改
- 详情：见各 skill 的 `cases/README.md`

## 新增 Skill

参考 `testcase-generator/` 结构复制，替换：

- 名称与用途
- 输入类型
- 输出规范（含文件命名规则）
- 生成规则（含专属自检清单）
- `cases/README.md`（写清楚这个 skill 特有的触发条件和关注点）

新增后**必须**在本文件的"技能总览"和"各 Skill 状态"两个表格里同步更新一行。
