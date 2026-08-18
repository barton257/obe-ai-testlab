# [S3] 订阅接口 userId 与 JWT 载荷不匹配未拦截（降级：非越权，但接口设计不严谨）

- 环境：Testnet / API `bullapitest.1bullex.com`
- 复现率：1/1
- 提交人：Barton（AI 辅助）
- 日期：2026-08-17
- 影响接口：`POST /botapi/v1/invest/purchase`（`invest/redeem` 同类待验证）
- **严重级别调整**：初报 S1（潜在越权）→ 复现后确认 S3（接口设计缺陷）

## 复现步骤

用 User1 JWT（`api=10732164`），body.userId 填 User2 UID (`10732177`)：

```bash
curl -X POST 'https://bullapitest.1bullex.com/botapi/v1/invest/purchase' \
  -H 'authorization: Bearer <user1_token>' \
  -H 'content-type: application/json' \
  --data '{"userId":"10732177","botId":1342,"amount":1}'
```

## 实际

- 接口同步返回 `{"code":0,"msg":"success"}`
- 调用后立即查询：
  - **User1 history 新增一条 `id=1819, tradeAmount=1, status=Init`** ← 记录落在了 JWT 用户下
  - **User2 history 完全无变化，total 仍为 12**
- 结论：服务端拿 JWT 的 `api` 字段作为真实操作者，body 里的 `userId` 被静默忽略

## 期望

服务端应对 body.userId 与 JWT.api 不一致的请求主动拒绝并返回业务错误（如 `identity_mismatch`），原因：

1. **接口契约不清晰**：调用方以为 body.userId 有意义，实际它是装饰字段，误导集成方
2. **审计困难**：日志里可能同时出现 body.userId 和 JWT.api，事后追踪难
3. **潜在攻击面**：如果哪天服务端逻辑改成"优先信 body.userId"（例如错误的 refactor），立即变高危越权
4. **符合防御性设计原则**：显式拒绝比静默忽略更安全

## 已排除（含批次结果二次确认）

批次窗口 10 min 后（2026-08-17 T+11min）复查：

- **User1 id=1819**：`status=Finished, tradeAmount=1, tradeUnits=1.016023, updatedAt=1786959017106` — 落 User1 名下，铸造份额 1.016023
- **User2 history**：total 仍为 12，最新记录仍为原 id=1759，**批次后完全无变化**

**结论坐实**：服务端以 JWT.api 为唯一操作者，body.userId 被静默忽略，**不越权**。S3 接口设计缺陷不升级。

## 建议

- 后端在 controller 层加校验：`if body.userId != jwt.api: return code=1, msg="identity_mismatch"`
- 前端不应显式传 userId，让服务端从 token 推断（当前实现里前端确实传了，见 `invest/purchase.js`）

---

## 复验记录 2026-08-18（Barton，AI 辅助）

**状态：缺陷仍存在，未修复。级别维持 S3。** 后端仓库不在本机，用 Testnet 实调复验。

复验方式与昨天一致 —— 用 User1 token 提交 `body.userId=<User2 UID>`，
并**分别用两个账号自己的 token 查各自 history**，确认记录归属（这是 S3 与 S1 的分界，必须验证）：

```
BEFORE  User1 total=52 latest #1838   |  User2 total=12 latest #1759
提交    User1 token + body.userId=User2(10732177), amount=1
同步    code=0 msg=success
AFTER   User1 total=53 latest #1839 amt=1  |  User2 total=12 latest #1759
        User1 记录数 +1 ; User2 记录数 +0
```

**结论不变**：服务端以 JWT.api 为唯一操作者，body.userId 被静默忽略。
User2 侧零变化 —— **不越权，不升级为 S1，S3 维持**。

（User1 total 由 47 增至 52 是同期其他复验与 E2E 用例产生的，与本条无关。）

### 与另两条缺陷的共性

本条与 [S2 订阅金额穿透](2026-08-17-spartans-S2-订阅金额小于最小值未拦截.md)、
[S2 赎回超权益静默截断](2026-08-17-spartans-S2-赎回金额超权益静默截断.md) 同属
**"入参越界/非法后静默处理，而非显式拒绝"** 的同一类根因，三条建议一并修复。

差别在于本条**当前不造成用户可感知的错误结果**（记录落对了人），
所以是埋雷型缺陷：一旦后端某次 refactor 改成"优先信 body.userId"，立刻变高危越权。
这正是原报告第 3 条理由，复验后依然成立。

### 修复建议（较原建议补充实施路径）

分两步，避免 breaking change：

1. **本迭代**：controller 层加一致性校验，不一致直接拒绝

   ```
   if body.userId != jwt.api:
       return {"code": 1, "msg": "identity_mismatch"}
   ```

   这一步对现有前端**无影响**（前端传的就是自己的 UID，本来就一致）。

2. **下个大版本**：从接口契约里移除 `userId` 字段，服务端只信 token。
   需前端同步改造（当前 `invest/purchase.js` 确实在传），属 breaking change，
   不建议与第 1 步同期做。

### 回归用例

`tests/api/test_spartans_api.py::TestKnownDefectRegressions::test_purchase_wrong_user_id_rejected`
已用 `@pytest.mark.xfail(strict=True)` 标记，2026-08-18 实测为 `XFAIL`（缺陷复现）。
后端修复后该用例转 XPASS 失败，强制回来摘标记。
