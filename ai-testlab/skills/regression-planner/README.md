# regression-planner

根据变更点生成回归测试清单。

## 输入

- 变更描述：PR 摘要 / 提交记录 / 需求变更文档
- 相关业务的 `docs/` 和 `testcases/`

## 输出

- Markdown 清单：需要回归的用例 ID + 优先级 + 理由
- 输出到会话或 `projects/<x>/docs/regression-{YYYY-MM-DD}.md`

## 使用

```
输入变更：斯巴达订阅窗口从每小时改为每 30 分钟
调用 regression-planner
输出：受影响用例清单
```

## 待补充

- `prompt.md`
- `examples/`
