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
