# tests/fixtures/

静态测试数据（脱敏后）。

## 什么放这里

- 稳定不变的**基线数据**（Tier 阈值表、错误码对照）
- 用于对比的**期望输出快照**（JSON snapshot）
- Mock 服务的响应样本

## 什么**不放**这里

- 动态生成的用户 / 订单（在测试代码里 factory 构造，运行后清理）
- 真实用户数据（即使已脱敏，也优先用 fake 数据）
- 大文件 / 二进制（超过 1MB 走 LFS 或外部存储）

## 命名

`{接口|模块}.{success|error}.{json|yaml}`

例：`subscribe.success.json`、`tier-thresholds.yaml`
