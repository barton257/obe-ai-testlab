# test-strategy-generator

从需求 / 走查 / 变更点生成完整测试策略文档，覆盖分层、场景矩阵、非功能维度、DoD 映射。

## 用途

一份 PRD 或需求描述进来，AI 帮你把测试策略展开成结构化文档，QA 只做评审 + 补充业务知识，不用从零抬手。

## 输入

支持任一或组合：

1. **PRD / 需求文档**：Markdown / 会话内自然语言
2. **功能审计报告**：`projects/<业务>/docs/*_FEATURE_AUDIT.md`
3. **变更点 / PR diff**：新功能的代码变更清单
4. **走查发现**：`projects/<业务>/bots/examples/*-walkthrough.md`

## 输出

- 一份符合 `ai-testlab/templates/TEST_STRATEGY.md` 骨架的文档
- 落点：`projects/<业务>/docs/<功能>_TEST_STRATEGY.md`
- 文件名遵循 AGENTS.md 第三节走查/审计规范

## 使用

在会话中：

```
读取 projects/spartans/docs/SPARTANS_FEATURE_AUDIT.md 第 3.4 节（订阅动作）
调用 ai-testlab/skills/test-strategy-generator/prompt.md
业务：spartans
功能：subscribe（订阅）
风险档：资金流转（严格执行 DoD 全部条目）
```

## 限制

- 不写死运营参数（Tier 门槛、分润比例、批次窗口时长），一律 `<name_from_config>`
- **不能凭空捏造场景**：所有场景必须能追溯到需求文档、走查记录、已有 bug 或 API 契约中的某一句
- 输出必须显式列 A/B/C/D 四段 DoD 映射，方便 QA 打勾
- 场景矩阵必须**穷举**至少两个维度的交叉；空格用 `N/A` + 理由，不留空
- 涉及资金操作的策略必须包含"数据一致性对账"和"失败回滚"两小节

## 与其他 skill 的关系

```
需求文档 / PRD
    ↓
test-strategy-generator   → 生成 TEST_STRATEGY.md（策略）
    ↓
testcase-generator        → 展开成 YAML 用例（具体用例）
    ↓
api-test-generator        → 生成 pytest 代码（可执行）
    ↓
regression-planner        → PR 时用它列回归清单
```

顺序上：策略先行，用例次之，代码最后。

## 待补充

- [x] `prompt.md`
- [ ] `examples/spartans-subscribe/`（首个示例）
- [ ] `cases/` 案例（首次 QA 修正后写）

## 归档触发

以下修改触发 `cases/` 案例：

- 场景矩阵少了关键维度（例：忘了"并发"轴）
- DoD 映射漏项
- 非功能维度描述过泛（"要测安全"这种）→ 需具体化为可执行断言
- 把运营参数写死了
