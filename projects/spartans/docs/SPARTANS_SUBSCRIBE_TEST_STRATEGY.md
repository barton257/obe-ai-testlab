# SPARTANS 订阅（Subscribe）测试策略

- 业务：spartans
- 模块：invest / subscribe（含 `invest/purchase` 接口 + UI 提交表单 + 批次结算）
- 负责人：Barton（QA 主导）
- 日期：2026-08-17
- 关联需求：`projects/spartans/docs/SPARTANS_FEATURE_AUDIT.md` §3.3、§3.4
- 状态：Draft（等 QA 评审）

> 本文档由 `ai-testlab/skills/test-strategy-generator/` 首次生成，作为 skill 的落地示例。
> 上线前对照 [`shared/conventions/dod.md`](../../../shared/conventions/dod.md) 全部条目打勾。

---

## 一、需求六问

| # | 问题 | 答案 |
|---|---|---|
| 1 | 用户能做什么？ | 已登录用户在机器人详情页输入订阅金额，勾选风险披露，提交订阅；同步接口返回 success，等下一个批次窗口铸造份额 |
| 2 | 系统必须保证什么？ | (a) 金额 ∈ `[<tier_min>, <tier_max>]`；(b) 用户钱包 USDT 余额 ≥ 金额；(c) 机器人 `status=Running` 且用户在白名单（若私域）；(d) JWT 用户与 body.userId 匹配；(e) 铸造份额 = 金额 ÷ 批次结算时的 nav；(f) 五路对账一致（钱包-账户-份额-资金池-history） |
| 3 | 出错会怎样？ | 前置校验失败：同步返回业务错误码（`amount_not_allowed` / `balance_not_enough` / `private_bot_subscribe_denied` 等）；批次结算失败：`invest/history` 状态由 `Init` 变为 `Failed` 或 `Cancel`，资金应回退到钱包 |
| 4 | 数据流经哪些系统？ | Web UI → 网关 → `botapi/v1/invest/purchase` → 订阅表（Init）→ 每 `<batch_window>` 批次调度器 → 计算 nav 铸造份额 → 更新 user_summary / user_board / invest/history → 资金池账户 |
| 5 | 谁有权限做？ | 已登录 + KYC 通过的用户；机器人 visibility=Public 或用户在 Private 白名单中；服务端以 JWT `api` 为准（body.userId 会被覆盖，见 [S3 bug](../bugs/2026-08-17-spartans-S3-userId与JWT不匹配未拦截.md)） |
| 6 | 有多少人同时做？ | 单批次窗口（Testnet 10 min / 生产 1 h）内理论上无上限，实际按机器人 AUM 上限 `<tier_aum_cap>` 累计；同用户同 bot 单窗口可多次订阅，服务端会合并或分记录（待 §4.2 验证） |

**关键运营参数**（不写死，见 `projects/spartans/tests/fixtures/tier_config.yaml`）：

- `<tier_min>` — Tier 最小订阅金额（Testnet 当前 1）
- `<tier_max>` — Tier 最大订阅金额（Testnet 当前 1e8）
- `<tier_aum_cap>` — 机器人 AUM 上限（Testnet 当前 1e8）
- `<batch_window_secs>` — 批次窗口（Testnet 600 / 生产 3600）
- `<profit_share_ratio>` — 分润比例（默认 10%，每 bot 可配）

---

## 二、场景矩阵

### 主矩阵：金额 × 用户状态

|   | 金额=0 | 0 < 金额 < min | 金额 = min | min < 金额 < max | 金额 = max | 金额 > max | 金额 > 余额 |
|---|---|---|---|---|---|---|---|
| **未登录** | 401 | 401 | 401 | 401 | 401 | 401 | 401 |
| **登录未 KYC** | `amount_not_allowed` | 拒 (`kyc_required`) | 拒 (`kyc_required`) | 拒 (`kyc_required`) | 拒 (`kyc_required`) | 拒 | 拒 |
| **登录已 KYC** | `amount_not_allowed` ✅ | **应拒但穿透** ← [S2](../bugs/2026-08-17-spartans-S2-订阅金额小于最小值未拦截.md) | success ✅ | success ✅ | success（预期） | 拒 (`amount_exceeds_max`) | `balance_not_enough` ✅ |
| **黑名单用户** | 拒 | 拒 | 拒 | 拒 | 拒 | 拒 | 拒 |
| **管理员冒用他人 UID** | 落 admin 名下 ✅（S3 记录） | 同 S2 | 同 admin | 同 admin | 同 admin | 拒 | 落 admin 名下 |

✅ = 已在 `test_spartans_api.py` 覆盖并通过
✗ = 未覆盖或已知未拦截

### 副矩���：机器人可见性 × 批次冲突

|   | 首次订阅 | 同窗口第二次订阅 | 订阅未结算前赎回 |
|---|---|---|---|
| **Public bot** | 记录 Init → 批次 Finished | 待验证（合并 or 双记录？） | invest/cancel 撤销 pending |
| **Private + 白名单** | 同上 | 同上 | 同上 |
| **Private + 无白名单** | `private_bot_subscribe_denied` ✅ | 拒 | 拒 |
| **botId 不存在** | `private_bot_subscribe_denied` ✅ | 拒 | 拒 |
| **bot status ≠ Running** | 应拒（待验证） | 应拒 | 应可撤销 |

### 补充维度

- **网络**：正常 / 慢网 (5s) / 断线 / 超时 — UI 侧需要 loading 态、重复提交防抖
- **端**：Web 桌面 / Mobile Web（Playwright 双设备跑）
- **国际化**：zh-CN（默认）/ zh-TW / en — 金额单位、风险披露文案
- **精度**：小数位数（业务规定 6 位）、极大值精度损失

---

## 三、分层测试计划

### 3.1 单元测试

**位置**：斯巴达后端源码 repo（本仓库不含后端源码，此处仅列 QA 应索取的覆盖点）。

| 目标函数 | 覆盖点 |
|---|---|
| `calc_share(amount, nav)` | amount=0 / nav=0 / 精度、四舍五入到 6 位、极大值溢出 |
| `validate_purchase_amount(user, bot, amount)` | 金额边界、余额校验、KYC、白名单、bot status |
| `settle_batch(bot_id)` | 空批次、部分失败回滚、并发一致性 |

通过基线：覆盖率 ≥ 80%，100% 通过。

### 3.2 API 接口测试

**位置**：`projects/spartans/tests/api/test_spartans_api.py`（已建骨架）
**通过基线**：全绿。

| 用例 ID | 类型 | 描述 | 预期 | 状态 |
|---|---|---|---|---|
| test_purchase_amount_zero_rejected | 异常 | amount=0 | `amount_not_allowed` | ✅ 已过 |
| test_purchase_below_min | 边界 | amount=`<tier_min>`-0.5 | 应拒 | ✗ 已知穿透 S2 |
| test_purchase_equal_min | 边界 | amount=`<tier_min>` | success | 待补 |
| test_purchase_equal_max | 边界 | amount=`<tier_max>` | success | 待补 |
| test_purchase_above_max | 边界 | amount=`<tier_max>`+1 | `amount_exceeds_max` | 待补 |
| test_purchase_no_balance_rejected | 异常 | amount 远超余额 | `balance_not_enough` | ✅ 已过 |
| test_purchase_without_auth | 异常 | 无 token | 401 | ✅ 已过 |
| test_purchase_wrong_user_id | 异常 | body.userId 与 JWT 不符 | 应 `identity_mismatch` | ✗ 已知穿透 S3 |
| test_purchase_kyc_not_passed | 异常 | 未 KYC 用户 | 应拒 | 待补，需 User3 未 KYC 账号确认 |
| test_purchase_private_bot_denied | 权限 | botId=999999 | `private_bot_subscribe_denied` | ✅ 已过 |
| test_purchase_bot_paused | 异常 | bot status ≠ Running | 应拒 | 待补 |

### 3.3 API 端到端

**位置**：同上，标记 `@pytest.mark.e2e`
**通过基线**：至少一条 happy path 通过。

| 用例 ID | 场景 | 断言链 | 等待时间 |
|---|---|---|---|
| TestSubscribeRedeemE2E | 订阅 1U → 等 `<batch_window>` → history=Finished tradeUnits>0 → 赎回 1U → 等批次 → history=Finished | 5 步 | ~22 min（Testnet）/ ~2 h（生产） |
| e2e-batch-rollback | 故意让批次失败（需后端支持注入）→ 验资金回退钱包 | 3 步 | ~11 min |
| e2e-multi-purchase-same-batch | 同用户同 bot 单窗口内 2 次订阅 → 验 history 分记录 or 合并 | 3 步 | ~11 min |

### 3.4 UI E2E (Playwright)

**位置**：`projects/spartans/tests/e2e/`
**通过基线**：happy path + 1 error path。

| Spec 文件 | 场景 | 关键断言 |
|---|---|---|
| subscribe-happy.spec.ts | 登录 → 选 Kakarotto → 输金额=1 → 勾风险 → 提交 → 弹窗关闭 → 我的订阅出现记录 | UI 显式确认 |
| subscribe-frontend-validation.spec.ts | 输金额=0 / 0.5 / abc / 空 | 提交按钮灰 or 前端提示 |
| subscribe-risk-not-checked.spec.ts | 不勾风险披露 | 提交按钮灰 |
| subscribe-logout.spec.ts | 未登录点订阅 | 跳登录页 |
| subscribe-i18n.spec.ts | zh-CN / en 切换 | 文案对齐 |

### 3.5 契约测试

**位置**：`automation/contracts/spartans.yaml`（待建）
**通过基线**：schema 无 breaking change。

- 请求 schema：`{userId, botId, amount}` 三字段类型固定
- 响应 schema：`{code, msg, data, timestamp}`
- 已知 `msg` 枚举：`success` / `amount_not_allowed` / `balance_not_enough` / `private_bot_subscribe_denied` / `Missing Authorization header`
- Breaking change 检测：字段类型变更、必填字段增减、枚举值删除

### 3.6 压测

**位置**：`projects/spartans/tests/perf/`（已存 `subscribe.perf.js` 骨架）
**通过基线**：见下表。

| 场景 | 工具 | 目标 | SLO |
|---|---|---|---|
| 单接口 purchase 峰值 | k6 | 100 QPS 持续 5 min | P99 < 500ms，无 5xx |
| 批次窗口并发 | k6 | 500 用户同时提交 | 批次成功率 > 99%，无重复扣款 |
| AUM 逼近上限 | k6 | 累计逼近 `<tier_aum_cap>` | 超限精准拒绝，无部分成功 |

---

## 四、非功能维度

### 4.1 安全

- [ ] **越权**：body.userId 与 JWT 不匹配应拒（当前静默忽略，见 S3）→ 用例 `test_purchase_wrong_user_id`
- [ ] **注入**：botId 传 SQL 片段、amount 传字符串 → 期望 400 而非 500
- [ ] **限流**：单用户单 IP 每分钟 purchase 次数上限（`<rate_limit>`）
- [ ] **日志脱敏**：错误日志不能包含完整 JWT、真实邮箱；用户 UID 保留后 4 位
- [ ] **CSRF**：跨站请求应被 CORS/CSRF 中间件拒绝
- [ ] **Token 篡改**：改 exp、改 api 字段 → 应 401
- [ ] **重放**：同一 identify + 同 body 短时间重放 → 应幂等或拒重复

### 4.2 数据一致性

对账路径：

```
1. 用户操作：purchase(1 USDT)
   ↓
2. 钱包：USDT 余额 - 1
   ↓
3. 账户权益：subscription total + 1
   ↓
4. 份额：user_shares += 1 / nav_at_batch
   ↓
5. 资金池：bot_aum + 1
   ↓
6. history：新增记录 status=Finished, tradeAmount=1, tradeUnits=1/nav
```

**不变量**（每步都要断言）：

- Σ 所有用户对 bot X 的份额 × nav_X = bot_X.aum
- Σ 用户订阅金额 - Σ 用户赎回金额 = bot 净流入 = bot_aum 变化（扣除 PnL）
- user_summary.total = availableBalance + Σ bot_estValue
- user_board.distributions[].rate 相加 = 1.0（当前 smoke 已覆盖）

### 4.3 可观测性

- [ ] Metric：`spartans.purchase.requests`、`spartans.purchase.errors`（按 msg 分维度）、`spartans.batch.duration`
- [ ] Error log：失败路径写 error level，含 traceId、userId（脱敏）、botId、amount、msg
- [ ] Trace：网关 → controller → validate → DB → 批次调度器 全链路可 grep
- [ ] Sensor：前端点击"提交订阅"打点，含金额段位（不含真实金额）

### 4.4 回滚 / 降级

- [ ] **批次调度器挂**：新 purchase 应仍能创建 Init 记录；调度恢复后按创建顺序结算；用户看不到"卡在提交中"
- [ ] **DB 主备切换**：切换窗口内 purchase 应报"服务临时不可用"，不能吞 amount 不回执
- [ ] **Feature flag**：`spartans.subscribe.enabled=false` 时接口返回 `feature_disabled`，UI 提示维护
- [ ] **Kill switch**：紧急暂停单个 bot 的订阅，通过 bot status ≠ Running 实现

---

## 五、风险与假设

| 风险 | 影响 | 缓解 | 责任人 |
|---|---|---|---|
| 批次结算过程中 nav 剧烈波动 | 用户份额与预期偏差大 | UI 显示"结算时净值决定"，加提示；测试模拟 nav ± 5% 波动 | 产品 + 后端 |
| Tier 参数运营侧改动无通知 QA | 测试用例失效 | fixtures/tier_config.yaml 每周对齐；加告警 | QA + 运营 |
| S2 / S3 尚未修复 | 生产可能出现小额穿透和身份日志混乱 | 上线前必修 S1/S2；S3 可延后但 monitor | 后端 |
| 批次窗口生产 1h，问题反馈时间长 | 用户投诉滞后 | 加 batch health check + Slack 告警 | 后端 + SRE |
| 私域 bot 白名单机制未测 | 越权订阅 Private bot | 补 test_purchase_private_bot_denied 变体 | QA |

---

## 六、Definition of Done 映射

**风险档：资金流转 — 严格执行 DoD 全部条目**。参考 [`shared/conventions/dod.md`](../../../shared/conventions/dod.md)。

### A 前置产出

- [x] 需求解读：`docs/SPARTANS_FEATURE_AUDIT.md` §3.3 / §3.4
- [x] 测试策略：本文档
- [x] 场景矩阵：本文档 §2

### B 测试代码

- [ ] 单元测试：由后端团队补，QA 索取覆盖率报告
- [x] API 测试（部分）：`test_spartans_api.py` 9/14 通过，5 条待补
- [x] API E2E 骨架：`TestSubscribeRedeemE2E`
- [ ] UI E2E：`tests/e2e/subscribe-*.spec.ts` 待建
- [ ] 契约测试：`automation/contracts/spartans.yaml` 待建
- [ ] 压测：`tests/perf/subscribe.perf.js` 待完善

### C 非功能

- [ ] 安全清单：7 项，当前 3 项覆盖
- [ ] 数据一致性：4 条不变量，当前 1 条覆盖（board.rate 相加=1）
- [ ] 可观测性：待与后端对齐 metric / trace 命名
- [ ] 回滚降级：待后端提供注入接口

### D 交付前

- [ ] Runbook：`docs/SPARTANS_SUBSCRIBE_RUNBOOK.md` 待写
- [ ] 灰度：Testnet 已开放，生产分批策略待产品定
- [ ] 监控告警：待 SRE 配置
- [ ] 上线沟通：待产品 + 客服对齐

---

## 七、附录

- 需求 / 审计：`projects/spartans/docs/SPARTANS_FEATURE_AUDIT.md`
- API 文档：`projects/spartans/docs/SPARTANS_API.md`
- 已有用例：`projects/spartans/testcases/spartans-subscribe-P0-正常-最小订阅金额.yaml`
- 相关 bug：
  - `bugs/2026-08-17-spartans-S2-订阅金额小于最小值未拦截.md`
  - `bugs/2026-08-17-spartans-S1-赎回金额超权益未拦截.md`（联动）
  - `bugs/2026-08-17-spartans-S3-userId与JWT不匹配未拦截.md`
- Fixtures：`tests/fixtures/tier_config.yaml`
- 测试代码：`tests/api/test_spartans_api.py`、`tests/api/client.py`
- 通用底座：`automation/clients/obe_http.py`

## 待 QA 补充（TODO 项）

1. `TODO(产品)`：批次窗口内多次订阅是否合并 or 分记录？
2. `TODO(后端)`：Tier 参数在哪个配置项，运营改动能否触发 webhook 通知 QA？
3. `TODO(SRE)`：metric / trace 命名规范
4. `TODO(产品)`：Private bot 白名单管理入口
5. `TODO(后端)`：批次失败时的 kafka topic / db 状态
