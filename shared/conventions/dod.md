# Definition of Done — 功能上线前必查清单

**用途**：功能开发到"可上线"之间的最后一道闸。任何一条未打勾都不能进生产。
**适用范围**：所有业务模块（当前主战场 `projects/spartans/`）。
**维护者**：QA 主导，工程 & 产品配合。修改本文件走 [AGENTS.md 第十节](../../AGENTS.md) 流程。

---

## 使用方式

1. 新功能进入测试阶段时，从下方模板复制一份到 `projects/<业务>/roadmap/<日期>-<功能>-dod.md`
2. 每一项由**负责人**打勾并写"证据"（PR 链接 / 报告路径 / 截图）
3. 未适用项显式写 `N/A` 并说明理由，不留空
4. QA 最后一遍核查后签字

---

## 完整性三维定义

进入清单前先确认覆盖三个正交维度，缺一不可：

- **深度**：单元 → 集成 → 端到端 → UI
- **广度**：正常 / 边界 / 异常 / 并发 / 权限 / 兼容 / 性能
- **质量属性**：功能 / 数据一致性 / 安全 / 可用性 / 性能 / 可观测 / 兼容 / 可回归

---

## Definition of Done 清单

### A. 前置产出

- [ ] **需求解读文档**：`projects/<业务>/docs/<功能>_REQ.md` 或链接到 PRD
- [ ] **测试策略文档**：`projects/<业务>/docs/<功能>_TEST_STRATEGY.md`（由 `ai-testlab/skills/test-strategy-generator/` 生成 + 人工评审）
- [ ] **场景矩阵**已展开：正常 / 边界 / 异常 / 权限 / 并发 每一格显式标注

### B. 测试代码（按测试金字塔）

| 层 | 目标 | 通过基线 |
|---|---|---|
| 单元 | 算法/工具函数覆盖 | 覆盖率 ≥ 80% 且 100% 通过 |
| API | 单接口正/边/异 | 全绿 |
| API E2E | 跨接口业务闭环 | 至少 1 条 happy path 通过 |
| UI E2E (Playwright) | 用户视角主路径 | 至少 happy path + 1 error path |
| 契约 | Schema 稳定 | 无 breaking change |
| 压测 | 单接口/关键流程 | P99 < SLO |

- [ ] 单元测试：路径 `______`，覆盖率 `___%`，通过 `___/___`
- [ ] API 测试：路径 `projects/<业务>/tests/api/`，通过 `___/___`
- [ ] API E2E：`pytest -m e2e` 通过 `___/___`
- [ ] UI E2E：`projects/<业务>/tests/e2e/*.spec.ts`，通过 `___/___`
- [ ] 契约测试：`automation/contracts/` 无 diff 报错
- [ ] 压测：报告路径 `______`，P99 `___ms` < SLO `___ms`

### C. 非功能维度（这四条最容易漏）

- [ ] **安全清单**
  - [ ] 越权：跨用户 ID 篡改 body / URL 参数
  - [ ] 注入：SQL / XSS / 命令注入 已扫描
  - [ ] 限流：核心接口有 rate limit
  - [ ] 日志脱敏：`shared/glossary.md` 敏感字段全部脱敏
  - [ ] CSRF / CORS 配置正确
- [ ] **数据一致性**
  - [ ] 跨接口对账：`用户操作 → 钱包 → 账户 → 份额 → 资金池` 五路一致
  - [ ] 边界场景：批次窗口内并发订阅 / 赎回 / 取消 交叉不冲突
- [ ] **可观测性**
  - [ ] 失败路径有 error log 且含 traceId
  - [ ] 关键动作有 metric 上报（Prometheus / Sensors）
  - [ ] Trace 能贯穿 API → DB → 批次调度
- [ ] **回滚 / 降级**
  - [ ] 批次调度器挂掉时接口表现符合预期（不吞钱、不丢单）
  - [ ] DB 主备切换 / 缓存失效场景已验证
  - [ ] 有 feature flag 或 kill switch 可快速关闭功能

### D. 交付前

- [ ] Runbook：出问题怎么回滚，写在 `projects/<业务>/docs/<功能>_RUNBOOK.md`
- [ ] 灰度 / 分批策略已定义（例：先 1% 用户，再 10%，再全量）
- [ ] 监控告警已配置且阈值经过 review
- [ ] 与产品 / 客服对齐上线时间和用户沟通话术
- [ ] AGENTS.md 第七节脱敏规则在 PR、bug 报告、测试数据中全部执行

---

## 风险加权原则

不是每条都花同样力气。按风险分级：

| 功能类型 | 必须严格执行的条目 | 可以放宽的条目 |
|---|---|---|
| 资金流转（订阅/赎回/分润/提现） | A / B / C 全部；D 分批必须 | — |
| 用户数据（KYC/资料） | A / B（除压测）/ C 安全+一致性 | 压测可后置 |
| 展示层 UI / 文案 | A / B（Playwright + API smoke） | C 除安全外可放宽 |
| 内部工具 / 运营后台 | A / B API 层 | Playwright 可省，安全仍需过 |

**斯巴达业务默认按"资金流转"档执行**。

---

## 常见反模式（会被 QA 打回）

- ❌ "手动过一遍没问题就上"，没有可执行测试代码沉淀
- ❌ Playwright 通过就当 E2E 完成，缺 API E2E 覆盖数据链
- ❌ 只写 happy path，边界/异常延后到"下个版本"
- ❌ 安全清单跳过，"这个功能改动小"
- ❌ 没有 Runbook 或 kill switch，出问题只能等修复
- ❌ 灰度策略没定就全量上

---

## 与其他文档的关系

- 总纲：[`AGENTS.md`](../../AGENTS.md)
- 用例命名 / 优先级判定：本目录其他 `.md`（待补）
- 测试策略生成：[`ai-testlab/skills/test-strategy-generator/`](../../ai-testlab/skills/test-strategy-generator/)
- 用例骨架：[`ai-testlab/templates/testcase.yaml`](../../ai-testlab/templates/)（待补）
