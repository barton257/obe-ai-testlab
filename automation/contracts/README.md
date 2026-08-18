# contracts/

测试契约定义。包括 **schema 验证**（响应字段类型与必填性）与 **contract testing**
（消费者驱动契约，若前后端采用 Pact 等工具）。

---

## 当前状态

**未建立契约测试。** 本目录占位。

---

## 应包含什么

### 1. Schema 验证

API 响应的字段契约。当前在 `test_spartans_api.py` 里混写了部分断言
（如 `test_bot_summary` 检查 `totalBots` 字段），但不成体系。

**建议做法**：

- 定义 Pydantic / JSON Schema 模型（一个文件一个端点）
- 在 smoke 用例里自动校验响应是否符合 schema
- **不检查业务值正确性**（那是业务断言的活），只检查"该字段存在且类型对"

示例结构：
```
contracts/
  api/
    bot_summary_response.json      # JSON Schema
    bot_detail_response.json
    user_summary_response.json
    purchase_response.json
    ...
  validate.py                      # 加载 schema 并校验的工具函数
```

### 2. 消费者驱动契约（可选）

若前后端用 Pact / Spring Cloud Contract 协作：

- `consumer/` — 前端期望的契约（mock 数据）
- `provider/` — 后端验证自己是否满足前端期望

**当前无此需求，暂不接入。**

---

## 与 API 测试的分工

| 关注点 | 位置 | 例子 |
|---|---|---|
| **字段存在、类型、必填性** | `contracts/` | `totalBots` 是 `int` 且必填 |
| **业务值正确性** | `projects/spartans/tests/api/` | `totalBots` 的值是否符合当前机器人数 |
| **边界与异常** | `projects/spartans/tests/api/` | amount=0 / 负数 / 超余额 被拒 |

契约测试**不关心具体业务值**，只确保"接口没改坏结构"。

---

## 何时写契约

适合在以下情况引入：

1. 前后端并行开发，后端接口未稳定时前端需 mock
2. 微服务架构，服务间接口频繁变更需自动化保护
3. 回归发现过"字段改名/删除导致前端崩溃"的线上事故

当前 Spartans 项目前后端在同一团队且迭代节奏较慢，暂无紧迫性。
**若未来前端报"接口字段缺失"相关 bug 超过 3 次，立即建立此机制。**

---

## 相关

- API 测试：[`../projects/spartans/tests/api/`](../projects/spartans/tests/api/)
- Schema 示例参考：[Pact documentation](https://docs.pact.io/)
