# ai-testlab/

QA 侧 AI 能力沉淀。让"AI 帮忙测试"的过程本身变成可版本化、可复用、可评估的资产。

## 与其他目录的关系

```
输入          ai-testlab/skills/        输出
─────────  ─────────────────────  ─────────
docs/*.md   testcase-generator/    projects/<x>/testcases/*.yaml
maps/*.mm   walkthrough-recorder/  projects/<x>/docs/*_WALKTHROUGH.md
现象描述     bug-writer/            projects/<x>/bugs/*.md
变更点       regression-planner/    回归清单
OpenAPI     api-test-generator/    projects/<x>/tests/api/*.py
```

## 目录

| 目录 | 内容 |
|---|---|
| [`skills/`](skills/) | 可复用 AI 测试技能（一目录一技能） |
| [`prompts/`](prompts/) | 通用 prompt 片段（角色/风格/约束） |
| [`templates/`](templates/) | 用例/缺陷/审计的空白模板 |
| [`workflows/`](workflows/) | 多 skill 组合的复合流程 |

## Skill 结构

每个 `skills/<name>/` 必须包含：

```
<name>/
├── README.md          # 输入、输出、使用方式、限制
├── prompt.md          # 主 prompt
└── examples/
    ├── input-01.md    # 示例输入
    └── output-01.yaml # 示例输出
```

## 使用原则

1. **可评估**：每个 skill 至少 3 组示例（正/异/边界），用于快速回归 prompt 变更
2. **可复用**：skill 输出必须能直接落到 `projects/<业务>/` 对应目录，不做二次加工
3. **可审计**：调用 skill 生成的产物在 commit message 加 `[AI-assisted via <skill-name>]`
4. **人工兜底**：所有 AI 产物必须由 QA 人工审核后 commit
