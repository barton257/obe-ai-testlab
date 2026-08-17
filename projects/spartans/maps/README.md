# maps/

斯巴达业务的思维导图。

## 命名规则

`{序号}-{业务}-{维度}.{xmind|mm}`

- `01-*-business-landscape` — 业务全景
- `02-*-end-to-end-flow` — 端到端流程
- `03-*-test-cases` — 测试用例演绎

## 双格式

每张图同时保留 `.xmind`（编辑）和 `.mm`（FreeMind，文本可 diff）两份，方便：

- `.xmind` 用于日常编辑（XMind 客户端）
- `.mm` 可 grep、可让 AI 读、可在 PR 上看差异

## 与 testcases/ 的关系

`maps/` 用于 **演绎和探索**，`testcases/` 用于 **结构化落地**。思维导图里定稿的用例分支要同步到 `testcases/` 下的 YAML。
