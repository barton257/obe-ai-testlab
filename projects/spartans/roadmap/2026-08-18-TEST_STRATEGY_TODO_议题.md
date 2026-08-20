# SPARTANS 测试策略待确认项 — 会议议题

**日期**：2026-08-18  
**发起人**：QA（Barton）  
**对接方**：产品 + 后端 + SRE  
**文档来源**：`SPARTANS_SUBSCRIBE_TEST_STRATEGY.md` §待确认项

---

## 背景

订阅测试策略文档已完成初稿，有 6 个技术细节需要外部方拍板才能完成对应的测试用例编写。
这些项**不阻塞当前已有用例**，但会影响下一阶段（P1 / P2）的测试覆盖完整性。

---

## 待确认项清单

### 1. 批次窗口内多次订阅的服务端行为

**问题**：同用户对同一 bot 在一个批次窗口内提交多次订阅，服务端是**合并成一条记录**还是**分多条记录**？

**当前观察**：
- UI 层面："我的订阅 → 进行中" tab 按 bot 聚合显示累计金额
- "操作记录" tab 显示单条记录
- 这是 **UI 呈现口径**，服务端 DB 存储和批次结算逻辑未确认

**影响范围**：
- API E2E 用例 `e2e-multi-purchase-same-batch` 的预期断言
- 资金台账对账规则（单条 vs 批次汇总）

**需要产品 / 后端明确**：
- [ ] 服务端 DB 存储：合并 or 分记录？
- [ ] 批次结算：按总金额一次性铸造份额 or 分批铸造？
- [ ] `invest/history` 返回几条记录？

---

### 2. Tier 参数变更通知机制

**问题**：`min_subscribe` / `max_subscribe` / `tier_aum_cap` 等参数由运营配置，**改动后能否触发通知 QA？**

**当前状况**：
- `tests/fixtures/tier_config.yaml` 是手工维护的基线（值来自 2026-08-17 Testnet 实测）
- 运营改动后会静默过期，导致测试用例边界值失效

**影响范围**：
- `TestPurchaseAmountBoundaries` 类的所有用例
- 压测用例的 AUM 上限断言

**需要后端 / 运营明确**：
- [ ] Tier 参数存在哪个配置系统？（DB / 配置中心 / 代码常量）
- [ ] 改动流程是什么？（工单 / 后台界面 / 代码发版）
- [ ] 能否在改动时 @ QA 或自动同步到测试 fixtures？

**临时方案**（若无自动通知）：
- QA 每周一手动抓取一次 Testnet tier 参数，diff 后更新 `tier_config.yaml`
- 在 CI 中加一条用例：实际值 vs fixtures 值不一致时报警而非失败

---

### 3. Metric / Trace 命名规范

**问题**：测试策略要求验证可观测性（§4.3），但 **metric / trace 的命名约定尚未与 SRE 对齐**。

**影响范围**：
- 压测用例的 SLO 断言（需要 metric 查询）
- 故障演练用例（需要 trace 查询验证链路完整性）

**需要 SRE / 后端明确**：
- [ ] Metric 命名规范：`spartans.purchase.requests` / `spartans.batch.duration` 是否对齐？
- [ ] Error log 的 traceId 格式是什么？能否在测试中关联请求和日志？
- [ ] Trace span 命名：网关 → controller → validate → DB → 批次调度器 的 span name 分别是什么？

**产出期望**：
- 一份 `SPARTANS_OBSERVABILITY.md` 文档，列出所有 metric / log / trace 的命名和查询方式
- 或至少给出一个实际的 traceId 样例供 QA 参考

---

### 4. Private bot 白名单管理入口

**问题**：测试策略覆盖了 Private bot 订阅权限（`private_bot_subscribe_denied`），但**白名单管理入口在哪里**？

**当前状况**：
- 已有用例 `test_purchase_private_bot_denied` 用一个不存在的 botId 触发拒绝
- 但无法测试"bot 存在 + 用户不在白名单"的真实场景

**影响范围**：
- Private bot 订阅权限测试覆盖不完整
- 无法验证白名单增删改的生效时间

**需要产品明确**：
- [ ] 白名单管理入口是什么？（后台界面 / API / 手工配置文件）
- [ ] QA 能否自助添加测试账户到某个 Private bot 的白名单？
- [ ] 白名单变更生效时间？（实时 / 需重启 / 有缓存延迟）

**临时方案**（若无管理入口）：
- 请后端在 Testnet 手工配置一个 Private bot + 两个测试账户（一个在白名单、一个不在）
- QA 用这两个账户覆盖白名单测试场景

---

### 5. 批次失败时的 Kafka topic / DB 状态

**问题**：测试策略要求覆盖批次回滚（roadmap P2-6），但**批次失败时的技术表征是什么**？

**影响范围**：
- `e2e-batch-rollback` 用例无法编写（不知道验证什么字段）
- 故障演练无法验证资金回退完整性

**需要后端明确**：
- [ ] 批次失败时 `invest/history` 的 status 会变成什么？（`Failed` / `Cancel` / 其他）
- [ ] 资金回退到钱包的时机？（实时 / 下一批次 / 人工介入）
- [ ] 是否有 Kafka 消息 topic 记录失败事件？Topic 名称是什么？
- [ ] 测试环境能否注入"故意让批次失败"的开关？

**产出期望**：
- 后端提供一个"批次失败注入"的 API 或配置开关
- 或至少提供一次手工触发的批次失败，QA 录制当时的 DB / history / Kafka 状态作为基线

---

### 6. 如何单独验证 `max_subscribe` 校验？（新增）

**问题**：当前测试账户余额（~9.5k USDT）远小于 Tier `max_subscribe`（100000000），任何超 max 的金额都会**先撞 `balance_not_enough`**，无法单独验证 max 校验逻辑。

**当前状况**：
- `test_purchase_above_max_rejected` 只能断言"被拒绝"，但不知道是因为 max 还是因为余额
- `test_purchase_equal_max_accepted` 理论上应该通过，但实际也会因余额不足被拒

**影响范围**：
- Tier 边界测试覆盖不完整，max 校验逻辑可能有 bug 但测不出来

**需要产品 / 后端选择一个方案**：
- [ ] **方案 A**：提供一个余额 > 100000000 的高余额测试账户
- [ ] **方案 B**：在 Testnet 新建一个 `max_subscribe=1000` 的低 max Tier，用现有账户测
- [ ] **方案 C**：暂时接受这个覆盖空缺，等生产出现高净值用户后补测

**临时处理**：
- 已在 `test_purchase_above_max_rejected` 注释中标注这个限制
- 不标记为 xfail，因为"被拒绝"本身是对的，只是无法区分拒绝原因

---

## 会议产出期望

对每个待确认项：
- [ ] 给出明确结论 or 临时方案
- [ ] 指定责任人和预计完成时间
- [ ] 结论回填到 `SPARTANS_SUBSCRIBE_TEST_STRATEGY.md` §待确认项

---

## 附录

- 测试策略原文：`projects/spartans/docs/SPARTANS_SUBSCRIBE_TEST_STRATEGY.md`
- 当前 API 测试代码：`projects/spartans/tests/api/test_spartans_api.py`
- Tier 配置基线：`projects/spartans/tests/fixtures/tier_config.yaml`（待建）
- 优先级约定：`shared/conventions/priority.md` §5-D（待确认项处理原则）
