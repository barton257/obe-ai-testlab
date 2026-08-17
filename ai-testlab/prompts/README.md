# prompts/

通用 prompt 片段。不是完整技能，是可以被 skill 或临时会话组合使用的原料。

## 分类建议

- `roles/` — 角色定义（资深 QA、合约交易员、风控专家...）
- `styles/` — 风格约束（简洁中文、Markdown 输出、YAML 结构...）
- `guardrails/` — 通用护栏（脱敏、不臆造参数、必须给出出处...）

## 使用

在 skill 的 `prompt.md` 里通过引用组合：

```
参考: ai-testlab/prompts/guardrails/no-fabricated-params.md
```
