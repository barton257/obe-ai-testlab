# tests/perf/

斯巴达压力/性能测试。

## 技术选型

- k6（脚本轻、云端友好、指标标准）
- 通用基线在 `../../../../automation/perf/`

## 运行

```bash
# 项目根目录
export OBE_TESTNET_BASE_URL=https://testnet.onebullex.com
export OBE_TOKEN=***                                     # 从 .env.local 加载
k6 run projects/spartans/tests/perf/subscribe.perf.js
```

## 命名

`{场景}.perf.js`

## 编写要求

- 场景与 SLO 分开：脚本描述 workload，SLO 由 CLI 参数或 `automation/perf/` 基线注入
- 压测目标环境必须是 **Testnet 或 Staging**，禁止对生产施压
- 每个脚本头部注释：目标接口、期望 QPS、期望 P95 延迟、是否影响资金

## 触发方式

不进入主 CI，通过 manual dispatch 或 tag 触发。见 `../../../../automation/ci/`。

## 占位样例

- [`subscribe.perf.js`](subscribe.perf.js)
