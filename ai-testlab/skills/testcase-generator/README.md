# testcase-generator

从需求/审计文档生成结构化测试用例（YAML）。

## 输入

- 功能审计报告：`projects/<x>/docs/*_FEATURE_AUDIT.md`
- 思维导图（可选）：`projects/<x>/maps/*.mm`
- 目标模块 / 优先级范围（用户提供）

## 输出

- YAML 文件，落到 `projects/<x>/testcases/`
- 命名遵循 `../../../AGENTS.md` 第三节

## 使用

```
读取 projects/spartans/docs/SPARTANS_FEATURE_AUDIT.md 第 3.4 节（订阅动作）
调用 ai-testlab/skills/testcase-generator/prompt.md
目标：生成 P0 正常/异常/边界 各 3 条 YAML 用例
输出目录：projects/spartans/testcases/
```

## 限制

- 不写死运营参数（金额、比例、Tier 门槛），一律用 `<placeholder_from_config>`
- 涉及资金操作的用例必须包含"失败回滚"验证步骤
- 每条用例必须能被人工独立执行

## 待补充

- `prompt.md`（主 prompt）
- `examples/`（≥3 组示例）
