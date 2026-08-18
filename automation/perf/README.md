# perf/

性能测试与压测脚本。当前采用 **k6**（Grafana Labs 开源工具）。

---

## 当前状态

**未编写任何压测脚本。** 本目录占位，所有内容待补充。

---

## 工具选型

已确定使用 **k6**（见 `automation/README.md`）。

**优势**：
- JavaScript / TypeScript 编写（与 E2E 技术栈一致）
- 支持协议级压测（HTTP/WebSocket/gRPC）
- 内置指标丰富（P95/P99、RPS、错误率）
- 可集成 Grafana 实时看板
- 开源且活跃维护

**不足**：
- 不支持真实浏览器渲染（纯协议层压测）
- 若需浏览器级压测（含 JS 执行、渲染耗时），需用 Playwright 或 Artillery

---

## 应包含什么

### 脚本结构

```
perf/
  spartans/
    smoke.js              # 轻量健康检查（100 VU，持续 30s）
    load.js               # 常规负载（500 VU，持续 5min）
    stress.js             # 压力测试（1000→5000 VU 阶梯）
    spike.js              # 尖峰测试（瞬间拉高到 2000 VU）
    endurance.js          # 稳定性测试（200 VU，持续 2h）
  k6-config.js            # 全局配置（API base、阈值）
  README.md               # 本文件
```

### 关注指标

| 指标 | k6 字段 | 建议阈值（参考） |
|---|---|---|
| **成功率** | `http_req_failed` | < 1% |
| **P95 响应时间** | `http_req_duration{percentile:95}` | < 500ms（读）/ < 2s（写） |
| **RPS** | `http_reqs` | > 100 req/s（单实例） |
| **错误率** | `http_req_failed` | < 0.1%（生产） / < 5%（压力测试） |

**业务指标**（需自定义 Counter）：
- 订阅成功率
- 赎回处理时间（含批次窗口等待）
- 分润计算延迟

---

## 场景设计

### 1. Smoke（快速验证）

**目的**：确认系统基本可用，不施加真实压力。

```javascript
export let options = {
  vus: 10,           // 10 个虚拟用户
  duration: '30s',   // 持续 30 秒
  thresholds: {
    http_req_failed: ['rate<0.01'],  // 失败率 < 1%
    http_req_duration: ['p(95)<500'], // P95 < 500ms
  },
};
```

**请求**：
- `GET /bots` — 机器人列表
- `GET /bots/{id}` — 随机机器人详情
- `GET /user/summary` — 用户资产（需认证）

### 2. Load（常规负载）

**目的**：模拟生产流量，验证系统在预期负载下稳定运行。

```javascript
export let options = {
  stages: [
    { duration: '2m', target: 100 },  // 缓慢爬升
    { duration: '5m', target: 500 },  // 稳定在 500 VU
    { duration: '2m', target: 0 },    // 缓慢降低
  ],
};
```

**场景**：
- 80% 浏览（bot 列表 + 详情）
- 15% 查询（用户资产、订单历史）
- 5% 写操作（订阅、赎回）— **需专用测试账户池，避免污染生产**

### 3. Stress（压力测试）

**目的**：找到系统崩溃点。

```javascript
export let options = {
  stages: [
    { duration: '5m', target: 1000 },
    { duration: '5m', target: 3000 },
    { duration: '5m', target: 5000 },  // 持续拉高直到失败
  ],
};
```

**观察**：
- 哪个 VU 数开始出现超时？
- 错误率何时突破 5%？
- 后端哪个服务先崩（DB / Redis / 应用层）？

### 4. Spike（尖峰测试）

**目的**：验证突发流量承受能力（如活动开抢）。

```javascript
export let options = {
  stages: [
    { duration: '10s', target: 2000 },  // 瞬间拉到 2000
    { duration: '1m', target: 2000 },   // 持续 1 分钟
    { duration: '10s', target: 0 },     // 瞬间降到 0
  ],
};
```

---

## 数据隔离

压测**必须使用专用测试账户**，不能打生产真实用户数据。

**建议策略**：
1. 在 Testnet / Staging 环境压测
2. 创建 100 个测试用户（UID 10000000–10000099）
3. 每个 VU 随机选一个用户，避免热点账户
4. 订阅/赎回操作打专用的"压测机器人"（bot ID 固定，不影响真实 bot）

**禁止对生产环境压测**（即使用测试账户）。

---

## 执行

### 本地跑

```bash
# 安装 k6（macOS）
brew install k6

# 运行 smoke
k6 run automation/perf/spartans/smoke.js

# 查看实时指标
k6 run --out influxdb=http://localhost:8086 smoke.js
```

### CI 集成

在 CD 流程的 **post-deploy** 阶段自动跑 smoke：

```yaml
# .github/workflows/deploy.yml
- name: Performance smoke test
  run: k6 run automation/perf/spartans/smoke.js --quiet
  continue-on-error: true  # 失败不阻塞发布，但会告警
```

---

## 相关

- 测试账号约定：[`../shared/env/test-accounts.md`](../shared/env/test-accounts.md)
- 环境定义：[`../shared/env/environments.md`](../shared/env/environments.md)
- k6 文档：[https://k6.io/docs/](https://k6.io/docs/)
