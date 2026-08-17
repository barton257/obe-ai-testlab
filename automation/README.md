# automation/

跨业务共享的**测试框架层**。业务无关的封装、工具、CI 配置都放这里，避免每个业务重复实现。

## 判断是否属于 automation/

- 抽象出的**类/函数**，不含业务字眼 ✅
- 多业务复用的**基础设施**（客户端、页面对象基类、CI 模板）✅
- 只服务一个业务，含 `spartans` / `合约账户` 等字眼 ❌ → 放 `projects/<业务>/`

## 目录

| 目录 | 用途 | 典型内容 |
|---|---|---|
| [`clients/`](clients/) | OBE 通用 API 客户端 | 认证、请求签名、通用错误处理 |
| [`page-objects/`](page-objects/) | Playwright 通用页面对象 | 登录页、导航栏、通用弹窗 |
| [`perf/`](perf/) | 压测通用配置 | k6 base config、SLO 定义 |
| [`contracts/`](contracts/) | 契约测试 | Pact、OpenAPI diff |
| [`ci/`](ci/) | 流水线定义 | GitHub Actions、门禁规则 |
| [`reporters/`](reporters/) | 报告聚合 | Allure/JUnit 模板、飞书通知 |

## 依赖注入原则

业务测试代码通过 import 使用 `automation/`，不允许反向依赖：

```python
# projects/spartans/tests/api/test_subscribe.py
from automation.clients.obe_http import ObeClient

def test_subscribe():
    client = ObeClient(env="testnet")
    ...
```

## 版本策略

`automation/` 里的接口保持向后兼容；破坏性变更需要在 PR 里列出所有引用点并一起改。
