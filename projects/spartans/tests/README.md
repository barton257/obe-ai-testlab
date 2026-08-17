# tests/

斯巴达业务的**可执行测试代码**。区别于 `../testcases/`（YAML 描述），这里的文件是能跑起来的。

## 目录

| 目录 | 类型 | 工具 | 运行方式 |
|---|---|---|---|
| [`api/`](api/) | 接口测试 | pytest + httpx / `.http` | `pytest api/` |
| [`e2e/`](e2e/) | UI 端到端 | Playwright | `npx playwright test e2e/` |
| [`perf/`](perf/) | 压力/性能 | k6 | `k6 run perf/xxx.perf.js` |
| [`fixtures/`](fixtures/) | 静态数据 | — | 被上述测试引用 |

## 环境变量

统一从根 `.env.local` 读取，不硬编码。示例见 `../../../shared/secrets/*.example.env`。

## CI 门禁

- `api/` — 每次 PR 必跑（阻塞合并）
- `e2e/` — 夜间跑（不阻塞 PR）
- `perf/` — 手动触发（tag / manual dispatch）

CI 配置见 `../../../automation/ci/`。

## 与 testcases/ 的对应

一条 YAML 用例可以对应多个测试脚本（不同实现层）。在测试脚本头部注释里注明对应 YAML 文件路径：

```python
# testcase: spartans/testcases/spartans-subscribe-P0-正常-最小订阅金额.yaml
```
