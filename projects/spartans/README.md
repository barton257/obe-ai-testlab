# spartans — 300 SPARTANS 策略机器人平台

OneBullEx 的自动化策略机器人平台。用户订阅机器人后，系统按策略在统一资金池内执行合约交易，用户按份额分享收益/风险。

## 走查环境

- URL：OneBullEx Testnet（简体中文）
- 首页：`/zh-cn/spartans`
- 开放平台：`/zh-cn/spartan-openplatform`
- 教程：https://support.onebullex.com/hc/zh-tw/articles/5376208077342

## 目录说明

| 目录 | 内容 | 当前文件 |
|---|---|---|
| [`docs/`](docs/) | 功能审计、需求解读、走查报告 | `SPARTANS_FEATURE_AUDIT.md`（全景梳理） |
| [`maps/`](maps/) | 业务全景 / 端到端流程 / 用例思维导图 | 三张 `.xmind` + `.mm` |
| [`testcases/`](testcases/) | 结构化用例（YAML） | 待补充 |
| [`bugs/`](bugs/) | 缺陷记录 | 待补充 |
| [`roadmap/`](roadmap/) | 迭代计划 | `2026-08-14-p0-p1.md` |
| [`bots/`](bots/) | 测试人格 | `Kakarotto.txt`、`Vegeta.txt` |
| [`tests/`](tests/) | 可执行测试 | 骨架样例见各子目录 |

## 核心业务模型

- **统一资金池**：所有订阅资金进入机器人合约账户统一执行；用户按份额分权益。
- **份额计算**：每股净值 = 账户总资产 ÷ 总份额；订阅/赎回按处理时净值计算份额/权益。
- **HWM 分润**：只有净值创新高且有已实现盈利时才触发分润。
- **Tier 机制**：Tier 1–5 决定 AUM 上限、Bot Limit、分润比例（运营参数，不写死）。

术语与详细口径见 [`docs/SPARTANS_FEATURE_AUDIT.md`](docs/SPARTANS_FEATURE_AUDIT.md) 及 `../../shared/glossary.md`。

## 测试重点

1. 订阅/赎回闭环（异步窗口、批次处理、失败回滚）
2. 聚合资金对账（订阅总额 / 钱包余额 / 账户权益 / 用户份额）
3. Tier 升降级边界
4. HWM 分润计算准确性
5. 权限隔离（机器人虚拟账户只开合约、私域白名单）

## 补测清单

见 [`docs/SPARTANS_FEATURE_AUDIT.md`](docs/SPARTANS_FEATURE_AUDIT.md) 第 7 节。
