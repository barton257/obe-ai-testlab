# workflows/

组合式流程：一个业务任务串接多个 skill。

## 示例（待实现）

- `new-feature-audit-to-tests` — 新需求 → 审计报告 → YAML 用例 → API 用例骨架
- `bug-triage` — 用户反馈 → 缺陷报告 → 回归清单 → 关联用例更新
- `weekly-regression` — 变更周报 → 回归清单 → 用例执行 → 报告聚合

## 结构

每个 workflow 一个 Markdown，说明：

1. 触发条件
2. 涉及的 skill 顺序
3. 中间产物落点
4. 人工卡点位置
