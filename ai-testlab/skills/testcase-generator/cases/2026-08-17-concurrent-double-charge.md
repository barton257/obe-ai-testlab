# 案例：并发订阅双扣（Vegeta V5）

- 日期：2026-08-17
- Skill: `testcase-generator`
- 输入源：`projects/spartans/bots/examples/Vegeta-subscribe-walkthrough.md#问题-V5`
- 终版落地：`projects/spartans/testcases/spartans-subscribe-P0-异常-并发订阅双扣.yaml`

## Input

走查发现（Vegeta 视角）：

> 在订阅弹窗打开期间，同一机器人在另一 Tab 再次打开订阅弹窗，同时提交两次。
> 并发提交未加幂等锁，两笔订阅均成功扣款（各 500 USDT），操作记录显示两条，但实际余额只扣一次——数据不一致。

要求：生成 P0 级并发/幂等验证用例。

## AI First Draft（问题版）

```yaml
id: spartans-subscribe-concurrent-double
title: 并发订阅测试
module: spartans
priority: P0
type: 异常
steps:
  - action: 打开两个订阅弹窗
  - action: 同时提交
expected:
  - 系统正确处理并发请求
  - 不出现数据不一致
```

**问题**：
1. `expected` 太抽象，"正确处理"没有明确的可断言项
2. 缺少 `cleanup`——涉及资金的用例必须清理，否则测试账号会污染
3. 没有具体金额和边界条件，操作者不知道用多少 USDT
4. 只描述"两个弹窗"，未覆盖不同浏览器/断网重发等真实并发场景
5. 未提及后端幂等键（Idempotency-Key）的实现要求，前端测试无法验证后端行为

## Final Version（关键片段）

```yaml
preconditions:
  - 可用 USDT 余额 = <2 * subscribe_amount>   # ← 显式给操作者说明
data:
  subscribe_amount: <min_subscribe_amount_from_config>
steps:
  - action: 使用脚本或手动在极短时间内（<200ms）同时点击 Tab1 和 Tab2 的"确认"  # ← 具体时间窗口
expected:
  - 至多一笔订阅成功，另一笔应返回明确错误（幂等冲突 / 状态锁）
  - 可用 USDT 余额只扣一份 <subscribe_amount>
  - 操作记录中最多出现一条对应订阅记录（或两条中一条状态为"失败"）
  - 后端接口对相同幂等键返回相同结果，不重复扣款   # ← 显式断言后端行为
cleanup:
  - 撤销成功的订阅（若允许）或等待赎回窗口清理     # ← 必须清理
edge_cases:
  - 不同浏览器（Chrome + Safari）并发
  - 前后端时钟不同步时的行为
  - 提交后立即断网，重发请求
notes:
  - 需前后端都实现幂等：请求头带 Idempotency-Key，服务端按 (user_id + bot_id + key) 加锁
```

## 学习点（后续同类用例请遵循）

1. **涉及资金的 P0 用例必须显式列 `cleanup`**——测试环境的账号状态污染会导致后续用例连锁失败
2. **并发场景要写清"时间窗口"**（例：<200ms）——不写 AI 会默认"约同时"，实际执行的人不知道多快算并发
3. **断言要覆盖后端行为，不只是前端可见结果**——幂等问题只看 UI 可能看不出
4. **`edge_cases` 至少含 3 个**——单一场景无法说明并发问题被真正解决
5. **`notes` 附实现约束**——测试暴露的问题往往需要架构级修复，写清楚有助于研发排查

## Diff 度量

| 指标 | 值 |
|---|---|
| First draft 行数 | 12 |
| Final 行数 | 28 |
| Human edit ratio | ~85% |
| 学到的模式数 | 5 |

## 回归清单

修改 `prompt.md` 后，用相同 Input 重新生成，检查：

- [ ] 输出中包含 `cleanup` 字段
- [ ] `steps` 描述含具体时间窗口
- [ ] `expected` 中至少一条断言后端幂等行为
- [ ] `edge_cases` >= 3 条
- [ ] `notes` 中提及幂等键实现方式
