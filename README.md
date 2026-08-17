# obe-ai-testlab

OneBullEx QA 侧的 **AI 测试实验室** 仓库。集中沉淀业务走查资产、AI 测试能力和跨业务自动化框架。

- 与产品侧的 [`obe-ai-product-workflow`](https://github.com/HenrlyLin16/obe-ai-product-workflow) 分工：本仓库聚焦 **QA + 自动化 + AI 辅助测试**。
- 首个业务模块：**斯巴达机器人（300 SPARTANS）**，见 `projects/spartans/`。

## 目录结构

```
obe-ai-testlab/
├── AGENTS.md                  # AI 协作规范（Claude / Codex / 其他模型必读）
├── projects/                  # 按业务模块组织
│   └── spartans/
│       ├── docs/              # 需求解读、功能审计
│       ├── maps/              # 思维导图（.xmind / .mm）
│       ├── testcases/         # 结构化用例（YAML/MD）
│       ├── bugs/              # 缺陷记录
│       ├── roadmap/           # 版本/迭代计划
│       ├── bots/              # 测试人格 prompt
│       └── tests/             # 可执行测试
│           ├── api/           # 接口用例
│           ├── e2e/           # UI 端到端
│           ├── perf/          # 压测脚本
│           └── fixtures/      # 测试数据
├── automation/                # 跨业务共享的测试框架
│   ├── clients/               # OBE 通用 API 客户端
│   ├── page-objects/          # 通用 UI 页面对象
│   ├── perf/                  # 压测通用配置
│   ├── contracts/             # 契约测试
│   ├── ci/                    # 流水线定义
│   └── reporters/             # 报告聚合
├── ai-testlab/                # QA 侧 AI 能力沉淀
│   ├── skills/                # 可复用 AI 测试技能
│   ├── prompts/               # 通用 prompt 片段
│   ├── templates/             # 用例/缺陷/审计模板
│   └── workflows/             # 组合式流程
├── shared/                    # 跨项目共享
│   ├── glossary.md            # 术语表
│   ├── env/                   # 环境定义
│   ├── secrets/               # 只放 .example，真值走 .env.local
│   └── conventions/           # 命名/优先级/缺陷分级
└── scripts/                   # 本地小工具
```

每个一级目录下有独立 `README.md` 说明用途和示例，进入子目录前请先读。

## AI 技能清单

已装备的 skill 见 [`ai-testlab/skills/README.md`](ai-testlab/skills/README.md) — 含用途、输入输出、落点、当前案例数、触发场景速查。

## 分层原则

| 判断 | 放哪 |
|---|---|
| 只服务某个业务、含业务字眼 | `projects/<业务>/` |
| 抽象后可复用于多业务 | `automation/` 或 `shared/` |
| AI 生成能力本身 | `ai-testlab/` |
| 一次性小工具 | `scripts/` |

## 测试完整性

新功能落地遵循 **策略 → 用例 → 代码 → 验收** 四阶段：

1. **策略**：用 [`ai-testlab/skills/test-strategy-generator/`](ai-testlab/skills/test-strategy-generator/) 生成 `<功能>_TEST_STRATEGY.md`（六问 + 场景矩阵 + 六层测试 + 非功能维度）
2. **用例**：用 [`testcase-generator`](ai-testlab/skills/testcase-generator/) 展开 YAML 用例
3. **代码**：用 [`api-test-generator`](ai-testlab/skills/api-test-generator/) 生成 pytest；UI E2E 手写 Playwright；压测手写 k6
4. **验收**：对照 [`shared/conventions/dod.md`](shared/conventions/dod.md) 打勾

首个完整示例：[`projects/spartans/docs/SPARTANS_SUBSCRIBE_TEST_STRATEGY.md`](projects/spartans/docs/SPARTANS_SUBSCRIBE_TEST_STRATEGY.md)。

## 快速上手

```bash
git clone git@github-barton257:barton257/obe-ai-testlab.git
cd obe-ai-testlab
# 阅读顺序
cat AGENTS.md                         # 协作规范
cat shared/conventions/dod.md         # 上线闸
cat projects/spartans/README.md       # 业务入口
cat ai-testlab/README.md              # AI 能力入口

# 运行 spartans API smoke
uv venv --python 3.13 .venv && source .venv/bin/activate
uv pip install -r requirements-dev.txt
cp shared/secrets/spartans.example.env .env.local  # 填真值
pytest projects/spartans/tests/api/ -v -m "not e2e"
```

## 相关

- 产品侧工作流：[HenrlyLin16/obe-ai-product-workflow](https://github.com/HenrlyLin16/obe-ai-product-workflow)（同目录下 `obe-ai-product-workflow/` 被 `.gitignore` 排除）
