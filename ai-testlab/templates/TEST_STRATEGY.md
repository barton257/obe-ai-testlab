# {功能名称} 测试策略

- 业务：{业务名，例如 spartans}
- 模块：{模块 / 子域}
- 负责人：{QA 姓名}
- 日期：{YYYY-MM-DD}
- 关联需求：{PRD 链接 / 会议纪要路径}
- 状态：Draft / Reviewed / Locked

> 本文档由 `ai-testlab/skills/test-strategy-generator/` 生成后由 QA 评审。
> 上线前需匹配 [`shared/conventions/dod.md`](../../shared/conventions/dod.md) 所有条目。

---

## 一、需求六问（Why & What）

| # | 问题 | 答案 |
|---|---|---|
| 1 | 用户能做什么？（动作） | |
| 2 | 系统必须保证什么？（不变量） | |
| 3 | 出错会怎样？（失败模式） | |
| 4 | 数据流经哪些系统？（链路） | |
| 5 | 谁有权限做？（角色 & 边界） | |
| 6 | 有多少人同时做？（并发规模） | |

**关键运营参数**（不写死，用占位符 `<name_from_config>`）：

- {参数名}：{业务口径}

---

## 二、场景矩阵

维度 A × 维度 B 交叉展开，每格显式给结果。空格填 `-` 或 `N/A` 并说明。

### 主矩阵：{维度 A} × {维度 B}

|   | 值 A1 | 值 A2 | 值 A3 |
|---|---|---|---|
| **值 B1** | 预期结果 / 用例 ID | | |
| **值 B2** | | | |
| **值 B3** | | | |

### 补充维度（按需展开）

- **权限**：未登录 / 已登录未 KYC / 已登录已 KYC / 黑名单 / 管理员
- **网络**：正常 / 慢网 / 断线 / 超时
- **端**：Web / Mobile Web / Android / iOS
- **国际化**：zh-CN / zh-TW / en / ja
- **批次冲突**：单批次窗口内单用户单次 / 多次 / 多用户同批次

---

## 三、分层测试计划

### 3.1 单元测试

| 目标函数 | 覆盖点 | 位置 |
|---|---|---|
| {calc_share(amount, nav)} | 边界、精度、除零 | {源码 repo} |

### 3.2 API 接口测试

| 用例 ID | 类型 | 描述 | 预期 code | 预期 msg |
|---|---|---|---|---|
| {spartans-subscribe-P0-normal-min} | 正常 | 最小订阅金额 | 0 | success |
| ... | | | | |

落点：`projects/{业务}/tests/api/test_{功能}.py`

### 3.3 API 端到端

| 用例 ID | 场景 | 断言链 | 等待时间 |
|---|---|---|---|
| e2e-subscribe-then-redeem | 订阅→批次→查份额→赎回→批次→对账 | 5 步 | 22 min |

标记：`@pytest.mark.e2e`，落点同 API 目录。

### 3.4 UI E2E (Playwright)

| Spec 文件 | 场景 | 关键断言 |
|---|---|---|
| {subscribe.spec.ts} | 登录→选 bot→提交订阅 | 弹窗关闭 + 我的订阅出现记录 |

落点：`projects/{业务}/tests/e2e/`

### 3.5 契约测试

- OpenAPI schema：`automation/contracts/{业务}.yaml`
- 断言：请求/响应 schema 无 breaking change

### 3.6 压测

| 场景 | 工具 | 目标 QPS | SLO | 断言 |
|---|---|---|---|---|
| 单接口 subscribe | k6 | 100 | P99<500ms | 无 5xx |
| 批次窗口内并发 | k6 | 500 用户同时提交 | 批次成功率>99% | 无重复扣款 |

落点：`projects/{业务}/tests/perf/`

---

## 四、非功能维度

### 4.1 安全

- [ ] 越权：body/URL 参数篡改跨用户 → 拒绝
- [ ] 注入：SQL/XSS/命令 → 已扫描
- [ ] 限流：接口有 rate limit
- [ ] 日志脱敏：敏感字段脱敏（[AGENTS.md 第七节](../../AGENTS.md)）
- [ ] Token / Session：过期、伪造、并发多端登录

### 4.2 数据一致性

对账路径（订阅赎回类功能必查）：

```
用户操作 → 钱包变动 → 账户权益变动 → 份额变动 → 资金池变动
```

每一步的数值应满足：{业务不变量，例如 Σ 用户份额 × nav = 资金池总资产}

### 4.3 可观测性

- [ ] 关键动作 metric：{列表}
- [ ] 失败 error log 带 traceId
- [ ] Trace 覆盖：{链路}

### 4.4 回滚 / 降级

- [ ] 批次调度器挂掉：{预期表现}
- [ ] DB 主备切换：{预期表现}
- [ ] Feature flag / kill switch：{位置}

---

## 五、风险与假设

| 风险 | 影响 | 缓解 | 责任人 |
|---|---|---|---|
| | | | |

---

## 六、Definition of Done 映射

对应 [`shared/conventions/dod.md`](../../shared/conventions/dod.md) 的清单：

- A 前置产出：本文档 ✅
- B 测试代码：见 §3
- C 非功能：见 §4
- D 交付前：Runbook 路径 `______`，灰度策略 `______`

---

## 七、附录

- 相关缺陷：`projects/{业务}/bugs/`
- 走查报告：`projects/{业务}/docs/`
- Fixtures：`projects/{业务}/tests/fixtures/`
