# AGENTS.md — AI 协作规范

本仓库由多个 AI 工具协作维护（Claude Code、Codex、Cursor 等）。**所有 AI 在写入或修改文件前必须先阅读本文件**。

## 〇、两轴关系图（最容易混的一处）

仓库沿**两条正交的轴**组织：**业务产物** vs **通用能力/工具**。搞清楚坐标再动手。

```
                    通用能力 / 工具（跨业务复用）
                    ▲
                    │
       automation/ ─┼─  ai-testlab/
       测试框架     │   AI 生产工具
       客户端/CI    │   skills/prompts/templates
                    │
   跨业务 ─────────┼──────────── 业务专属
                    │
       shared/     │    projects/<业务>/
       术语/规范    │    docs/maps/testcases/bugs/tests
                    │
                    ▼
                    业务产物（具体交付物）
```

### `projects/` 与 `ai-testlab/` 的生产关系

`ai-testlab/` 是**工厂**，`projects/` 是**仓库**。

```
输入                    ai-testlab/(工具)              projects/<业务>/(产物)
──────────────────    ──────────────────────────    ──────────────────────────
docs/*.md         →   skills/testcase-generator  →  testcases/*.yaml
现象/日志         →   skills/bug-writer          →  bugs/*.md
OpenAPI           →   skills/api-test-generator  →  tests/api/*.py
变更点            →   skills/regression-planner  →  docs/regression-*.md
走查录音/截图     →   skills/walkthrough-recorder →  docs/*_WALKTHROUGH.md
```

判断口诀：

- **一个 prompt / 模板 / 生成规则** ≥ 2 个业务能用 → `ai-testlab/skills/`
- **一份具体的用例 / bug / 报告** → `projects/<业务>/`
- **一个客户端 / 页面对象 / CI 定义** 多业务共用 → `automation/`
- **一个业务专属角色 prompt** → `projects/<业务>/bots/`

四个顶层目录再对照：

| 轴 | 目录 | 一句话定义 |
|---|---|---|
| 业务产物 | `projects/` | 各业务的走查、用例、缺陷、测试脚本 |
| 通用工具 | `ai-testlab/` | 生成产物的 AI 技能 / prompt / 模板 |
| 通用工具 | `automation/` | 测试运行时依赖的框架代码 |
| 跨业务规范 | `shared/` | 术语、环境、密钥示例、规则约定 |

## 一、写入前四问

1. **它属于哪个业务？** 有业务字眼 → `projects/<业务>/`；跨业务通用 → `automation/` 或 `shared/`；是 AI 能力本身 → `ai-testlab/`。
2. **它是哪一类产物？** docs / maps / testcases / bugs / roadmap / bots / tests(api|e2e|perf|fixtures) — 严格按分类落位。
3. **是否含敏感信息？** 真实 UID、API Key、Secret、订单号、真实邮箱、密码 → 一律脱敏（`<uid_placeholder>` / `***`）或改走 `.env.local`（已 gitignore）。
4. **是否需要人工审核？** 所有 AI 生成的用例、缺陷、审计报告必须由 QA 人工过一遍再 commit，commit message 注明"AI 生成 + 人工审核"。

## 二、目录用途一览

| 路径 | 放什么 | 不放什么 |
|---|---|---|
| `projects/<业务>/docs/` | 需求解读、功能审计、走查报告（.md） | 通用规范（→ `shared/conventions/`） |
| `projects/<业务>/maps/` | 思维导图 `.xmind` `.mm`（业务全景/流程/用例） | 结构化用例（→ `testcases/`） |
| `projects/<业务>/testcases/` | 结构化用例 `.yaml` `.md`（可 diff、可 grep、可喂 AI） | 可执行脚本（→ `tests/`） |
| `projects/<业务>/bugs/` | 缺陷记录 `.md`（一 bug 一文件） | 缺陷模板（→ `ai-testlab/templates/`） |
| `projects/<业务>/roadmap/` | 迭代计划 `YYYY-MM-DD-*.md` | 长期战略（→ `docs/`） |
| `projects/<业务>/bots/` | 测试人格/角色 prompt（`.txt` `.md`） | 通用 prompt（→ `ai-testlab/prompts/`） |
| `projects/<业务>/tests/api/` | 接口用例（pytest / `.http`） | 通用客户端（→ `automation/clients/`） |
| `projects/<业务>/tests/e2e/` | UI 端到端（Playwright） | 通用页面对象（→ `automation/page-objects/`） |
| `projects/<业务>/tests/perf/` | 压测脚本 `.js`（k6）`.py`（Locust） | 通用基线（→ `automation/perf/`） |
| `projects/<业务>/tests/fixtures/` | 静态基线数据（脱敏后） | 动态生成的临时数据（写在测试代码里） |
| `automation/clients/` | OBE 通用 API 客户端封装 | 业务专属逻辑 |
| `automation/page-objects/` | 跨业务通用 UI 组件 | 单业务页面 |
| `automation/perf/` | 压测通用配置、公共 SLO 定义 | 具体业务场景 |
| `automation/contracts/` | 契约测试（Pact / JSON Schema / OpenAPI diff） | 单向接口用例 |
| `automation/ci/` | CI 流水线定义、门禁规则 | 本地脚本（→ `scripts/`） |
| `automation/reporters/` | 报告模板、结果聚合 | 具体报告输出（→ 各 `tests/` 下） |
| `ai-testlab/skills/<name>/` | 可复用 AI 测试技能（含 README + prompt + 输入输出示例） | 一次性 prompt |
| `ai-testlab/prompts/` | 通用 prompt 片段（角色/风格/约束） | 完整技能（→ `skills/`） |
| `ai-testlab/templates/` | 用例/缺陷/审计模板（`.md` 骨架） | 已填写的实例（→ 对应业务） |
| `ai-testlab/workflows/` | 多 skill 组合式流程 | 单一 skill |
| `shared/glossary.md` | OBE / 合约 / 斯巴达等术语的统一定义 | — |
| `shared/env/` | 环境定义（testnet / staging URL、账号约定） | 真实凭证 |
| `shared/secrets/` | 只放 `*.example.env` | 真值（→ 本地 `.env.local`） |
| `shared/conventions/` | 用例命名、优先级、缺陷分级、commit message 规则 | — |
| `scripts/` | 本地小工具（导出、格式化、迁移一次性脚本） | 测试脚本（→ 对应 `tests/`） |

## 三、命名规则

- **测试用例文件**：`{业务}-{模块}-{P0|P1|P2|P3}-{正常|异常|边界}-{简述}.{yaml|md}`
  - 例：`spartans-subscribe-P0-正常-最小订阅金额.yaml`
- **缺陷文件**：`YYYY-MM-DD-{业务}-{严重级别 S1..S4}-{简述}.md`
  - 例：`2026-08-15-spartans-S2-赎回按钮点击无响应.md`
- **走查/审计报告**：`{业务}_{类型}_{YYYYMMDD}.md`（大写 SNAKE_CASE 兼容现有 `SPARTANS_FEATURE_AUDIT.md`）
- **Roadmap**：`YYYY-MM-DD-{主题}.md`
- **测试脚本**：pytest 使用 `test_*.py`，Playwright 使用 `*.spec.ts`，k6 使用 `*.perf.js`
- **AI skill 目录**：kebab-case，含 `README.md` + `prompt.md` + `examples/`

## 四、用例结构（YAML 骨架）

```yaml
id: spartans-subscribe-P0-normal-min-amount
title: 订阅最小金额校验
module: spartans / subscribe
priority: P0
type: 正常
preconditions:
  - 账号已登录
  - 可用 USDT 余额 >= 最小订阅金额
steps:
  - action: 打开机器人详情页
    data: bot_name=OBE-Jason
  - action: 点击订阅
  - action: 输入最小订阅金额
    data: amount=<min_from_config>
  - action: 勾选风险披露 → 提交
expected:
  - 提交成功，弹窗关闭
  - 我的订阅 → 操作记录出现"订阅 OBE-Jason"，金额为负
notes:
  - 最小金额受运营配置控制，用占位符不写死
generated_by: ai-testlab/skills/testcase-generator
reviewed_by: <QA 姓名>
```

## 五、缺陷结构（MD 骨架）

```markdown
# [S2] 赎回按钮点击无响应

- 环境：Testnet / Web / Chrome 128
- 复现率：3/3
- 提交人：<QA>
- 日期：2026-08-15

## 复现步骤
1. ...

## 预期
...

## 实际
...

## 附件
截图 / HAR / 日志（脱敏后）
```

## 六、AI 产物落地规则

- **可执行代码类**（api/e2e/perf/skill 代码）：提交前必须本地跑一次，日志贴 PR 描述。
- **文档类**（docs/testcases/bugs）：AI 生成 → 人工审核 → commit message 加 `[AI-assisted]` 前缀。
- **不允许**：AI 直接改 CI 配置、`AGENTS.md`、根 `README.md`、`shared/conventions/*`。这些改动必须由人主动发起。
- **AI 引用**：文件内引用 AI 产物时用相对路径，例如 `参见 ai-testlab/skills/testcase-generator/README.md`。

## 七、脱敏规则

| 字段 | 处理 |
|---|---|
| 用户 UID | `<uid>` 或 `uid_***1234`（保留后 4 位） |
| 邮箱 | `u***@example.com` |
| API Key / Secret | `<api_key>` |
| 订单号 / 交易哈希 | `<order_id>` |
| 真实金额（涉隐私时） | 保留量级 `~1000 USDT` |
| 内部 IP / 域名 | `<internal-host>` |

违反脱敏规则的 commit 会被 revert。

## 八、依赖与环境

- Python 3.11+（api / perf）
- Node 20+（e2e Playwright）
- k6 最新 stable
- 本地凭证仅存 `.env.local`，不入库

## 九、扩展新业务模块

复制 `projects/spartans/` 目录结构，替换业务名：

```
projects/<新业务>/
├── README.md            # 业务概述、入口路径
├── docs/
├── maps/
├── testcases/
├── bugs/
├── roadmap/
├── bots/
└── tests/{api,e2e,perf,fixtures}/
```

同时在根 `README.md` 的业务列表中加一行。

## 十、修改本规范

`AGENTS.md` 的变更需要：

1. 人工发起（不接受 AI 直接改）
2. commit message 前缀 `docs(agents):`
3. 变更后同步给团队并更新相关 skill 的输入输出说明
