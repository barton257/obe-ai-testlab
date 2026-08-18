# Handoff 交接文档

**最后更新**：2026-08-18  
**项目**：obe-ai-testlab / Spartans QA 自动化  
**分支**：`feature/spartand-20260817`（已推送）

---

## 遗留问题与任务

### 🔴 P0（已完成，已合入当前分支）

| # | 问题 | 描述 | 状态 | 提交 |
|---|---|---|---|---|
| 1 | **登录态失效导致断言结论反转** | 全量跑 E2E 时 storageState 过期，未登录态的 disabled 按钮被误判为"前端校验生效"，掩盖了真实缺陷 | ✅ 已修复 | `5f04959` |
| | | 改用每个 spec 的 `beforeEach` 独立重登，牺牲 6s×N 换稳定性 | | |
| 2 | **Happy Path 断言不足** | `subscribe-happy.spec.ts` 只验证 Kakarotto 标题出现，不能证明本次订阅成功（历史记录里本来就有） | ✅ 已补强 | `5f04959` |
| | | 新增：查找最新订阅记录，验证金额=1 且创建时间在 1 分钟内 | | |
| 3 | **反向断言错误** | 三个 UX 缺陷用例用 `not.toBeDisabled()` 记录错误行为，缺陷修复后测试会误报失败 | ✅ 已改正 | `ff9c3e0` |
| | | 改为正向断言 `toBeDisabled()` + `test.fail()` 标记，符合 Playwright 规范 | | |
| 4 | **文档与代码不一致** | `README.md` 描述已废弃的 JWT fixture，实际代码用 `auth.setup.ts` + storageState | ✅ 已同步 | `ff9c3e0` |

### 🟡 P1（已完成，后续需维护）

| # | 问题 | 描述 | 状态 | 后续方案 |
|---|---|---|---|---|
| 5 | **资金类测试无幂等性** | 每次真实扣款，无数据隔离，1000 次订阅就耗尽 User1 | ✅ 已隔离 | **维护要求**：每次跑动账用例后必须 `python scripts/spartans_funds_ledger.py sync` |
| | | 已接入专用账户（UID 10732178，初始 1000 USDT），建立资金变动台账（`projects/spartans/funds/`） | | **缺口**：订阅、赎回可自动采集，其余（划转/分润/各类费用）只能手工 `add` |
| | | 动账用例带 `writes_funds` 标记，日常回归不触发；余额低于 50 USDT 自动 skip | | **待确认**：是否设自动清理脚本定期赎回？`subscribe-happy` 每跑一次沉淀 1 USDT 不回流 |
| 6 | **API 缺陷回归用例缺失** | S2 两条（订阅低于 min / 赎回超权益）、S3 一条（userId 与 JWT 不匹配）无自动化覆盖 | ✅ 已补齐 | 用 `@pytest.mark.xfail` 标记，缺陷修复后改为正向用例 |
| | | 3 条 xfail 用例已验证：Testnet 后端仍未修复，预期失败全部命中 | | 修复后运行 `pytest -m xfail` 确认变绿，再移除标记 |
| 7 | **缺陷复验** | 需定期确认已归档 bug 是否修复 | ✅ 2026-08-18 已验证 | 每周或每个 Testnet 部署后跑一次复验 |
| | | 三条缺陷（S2×2 + S3×1）全部仍存在，无一修复 | | 文档：`projects/spartans/bugs/*.md` 末尾的「复验记录」章节 |
| 8 | **优先级规范缺失** | bug/用例无统一 P0/P1/P2 定义 | ✅ 已建立 | 文档：`shared/conventions/priority.md` |

### 🟠 P1（待确认 / 待外部输入）

| # | 问题 | 描述 | 阻塞原因 | 后续方案 |
|---|---|---|---|---|
| 9 | **TEST_STRATEGY 5 条待确认项** | 涉及产品决策、后端实现、SRE 监控的测试边界 | 需约产品/后端/SRE 评审 | 会议纪要回填到 `SPARTANS_SUBSCRIBE_TEST_STRATEGY.md` §待确认项 |
| | | 1. 批次窗口内能否取消订阅？（产品） | | 确认后补对应用例或标注「产品不支持」 |
| | | 2. 机器人暂停时前端按钮是否禁用？（前端 UX） | | 已有 `test_purchase_bot_paused` 框架，需实测路径 |
| | | 3. share 铸造失败/延迟的降级策略？（后端） | | 若有监控告警，E2E 只验 happy path；若无，需补异常路径 |
| | | 4. Testnet 批次窗口是否稳定 10min？（SRE） | | 若不稳定，`BATCH_WINDOW` 改为配置或轮询状态 |
| | | 5. 并发订阅同一 bot 的幂等性？（后端） | | 若后端保证幂等，补并发用例；若不保证，标注已知限制 |
| 10 | **钱包流水接口缺失** | 资金台账只能自动采集订阅/赎回，无法覆盖划转、分润、各类费用、资金费率 | 后端未暴露账单明细接口 | **方案 A**：若有接口，补进 `spartans_funds_ledger.py` 采集器 |
| | | 已探测 8 个候选路径全部 404：`invest/profit/history`、`api/asset/bill` 等 | | **方案 B**：若无接口，维持手工 `add`，在 README 明确标注限制 |
| | | `user_board` 只有 `rpnl`/`upnl` 总量快照，无逐笔明细 | | **方案 C**：前端能看到的流水页面，抓包找接口 |
| 11 | **订阅权益清理策略** | `subscribe-happy` 每跑一次沉淀 1 USDT 在 bot 里不回流，1000 次后耗尽可用余额 | 要自动归还就得等 11min 批次窗口，拖慢回归 | **待拍板**：是否设独立清理脚本定期批量赎回？还是手工清理？ |
| | | API E2E 订阅→赎回闭环净额为 0，但期间锁 1 USDT 约 11 分钟 | | 当前 1000 USDT 够跑很多轮，非紧急 |

### 🟢 P2（增强类，不阻塞）

| # | 问题 | 描述 | 后续方案 |
|---|---|---|---|
| 12 | **E2E 定位器脆弱** | `subscribe-i18n` 用 `.nth(1)` 找按钮，多语言环境下可能定位错 | 改用唯一语义（`role + name` 或 `data-testid`） |
| | | 风险 checkbox 用 `input[type="checkbox"]` 可能点击失败 | 改用 `label` 点击或 `locator.check()` |
| 13 | **缺 bot 状态机覆盖** | 只验证 Running/Settling，Paused/Stopped/Error 无用例 | 已有 `test_purchase_bot_paused` 框架，需确认触发路径（见 #9.2） |
| 14 | **批次窗口硬编码** | `BATCH_WINDOW` 写死 11min，Testnet 实际 10min，生产 1h | 改为环境变量或从配置文件读取 |
| 15 | **API 连接重试无退避** | `requests.adapters.Retry` 用固定间隔，高频失败时浪费配额 | 改为指数退避 `backoff_factor=0.5` |

---

## 当前测试覆盖现状

### E2E（Playwright）

- **18 条用例**，7 个 spec 文件
- 覆盖：订阅 happy path、前端金额校验（含 3 条 UX 缺陷记录）、风险披露、i18n、未登录跳转
- 稳定性：登录态问题已修复，本地单跑全绿
- **未覆盖**：赎回流程（需等批次窗口）、bot 状态机、并发、跨浏览器

### API（pytest）

- **10 条只读用例** + **4 条动账用例**（默认不跑）+ **3 条 xfail 缺陷回归**
- 覆盖：机器人列表/详情、用户看板、订阅→赎回完整链路、异常分支（无认证/负金额）
- 动账用例：订阅最小金额、赎回最小金额、历史记录验证
- **未覆盖**：批量订阅、部分赎回、订阅后立即取消（若产品支持）

### Bug 归档

- **3 条缺陷**（S2×2 + S3×1），全部有复现步骤 + 预期/实际对比 + 影响评估
- 模板：`projects/spartans/bugs/YYYY-MM-DD-spartans-Sx-模板.md`

---

## 资金账户台账使用指南

**账户信息**：UID `10732178`，初始 1000 USDT，凭证在 `.env.local`（gitignore）

**台账位置**：`projects/spartans/funds/LEDGER.md`（人读）+ `ledger.csv`（机读）

**工具**：`scripts/spartans_funds_ledger.py`

```bash
# 跑完动账用例后同步（幂等，重跑不重复）
python scripts/spartans_funds_ledger.py sync

# 手工补录（划转/分润/费用等无法自动采集的类型）
python scripts/spartans_funds_ledger.py add

# 对账（台账累计 vs 接口余额）
python scripts/spartans_funds_ledger.py verify
```

**纪律**：
1. 每次用这个账户跑动账用例，**跑完就 sync**，不要攒着
2. 手工操作（划转、开仓等）后立即 `add` 补录
3. 每天结束前 `verify` 一次，不平立即排查
4. 台账 commit message 必须包含单号/机器人/金额，便于追溯

**当前状态**（2026-08-18）：
- 1 笔记录（#1841 subscribe -1 USDT，权限验证产生）
- 可用余额 999 USDT，**对平** ✓

---

## 下次接手清单

1. **立即检查**：`python scripts/spartans_funds_ledger.py verify` 确认台账对平
2. **约会议**：与产品/后端/SRE 评审 TEST_STRATEGY 5 条待确认项（#9）
3. **后端确认**：
   - S2/S3 缺陷修复排期？修复后移除 xfail
   - 是否有钱包流水接口？有则补采集器（#10）
4. **决策**：订阅权益清理策略 —— 自动脚本 or 手工？（#11）
5. **可选增强**：P2 列表中的定位器优化、状态机覆盖

---

## 相关文档

| 文档 | 路径 |
|---|---|
| 测试策略 | `projects/spartans/docs/SPARTANS_SUBSCRIBE_TEST_STRATEGY.md` |
| E2E README | `projects/spartans/tests/e2e/README.md` |
| API README | `projects/spartans/tests/api/README.md` |
| Bug 归档 | `projects/spartans/bugs/` |
| 资金台账 | `projects/spartans/funds/` |
| 优先级规范 | `shared/conventions/priority.md` |
| 今日计划 | `projects/spartans/docs/2026-08-18-今日计划.md` |
| GPT 审查报告 | `projects/spartans/docs/SPARTANS_E2E_TEST_CASE_REVIEW_20260818.md` |

---

**联系人**：barton.c@office.onebullex.com  
**分支状态**：可合入 main（全部 P0 已修复，CI 应全绿）
