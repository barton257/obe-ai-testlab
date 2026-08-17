# [S1] 订阅接口 userId 与 JWT 载荷不匹配未被拦截（潜在越权）

- 环境：Testnet / API `bullapitest.1bullex.com`
- 复现率：1/1
- 提交人：Barton（AI 辅助）
- 日期：2026-08-17
- 影响接口：`POST /botapi/v1/invest/purchase`（`invest/redeem` 待验证同类）

## 复现步骤

用 User1（`api=10732164`）的 JWT，故意把 body 里 `userId` 填成一个不存在或他人 ID：

```bash
curl -X POST 'https://bullapitest.1bullex.com/botapi/v1/invest/purchase' \
  -H 'authorization: Bearer <user1_token>' \
  -H 'content-type: application/json' \
  --data '{"userId":"99999999","botId":1342,"amount":1}'
```

## 预期

- 服务端应用 JWT `api` 字段（真实用户 ID）覆盖或校验 body 中的 `userId`
- 不一致时应返回 `403 forbidden` 或 `identity_mismatch`
- 至少不能让攻击者传入他人 ID 做操作

## 实际

- 返回 `{"code":0,"msg":"success","data":null,"timestamp":0}`
- 需追加验证：这条记录最终落到 JWT 的用户还是 body 传入的 userId 下
  - 如果落到 body 的 userId，属于**高危越权**
  - 如果落到 JWT 用户，属于接口设计冗余但不越权

## 建议核查

1. 用 User1 token + userId=User2 UID (`10732177`) 调 purchase，等批次完成后：
   - 查 User1 的 invest/history 是否新增此条
   - 查 User2 的 invest/history 是否被"代下"
2. 类似 redeem 场景重跑一遍
3. 若接口设计允许平台管理员代操作，需说明并加权限判定

## 严重级别 S1 依据

- 存在越权可能且能通过公开接口触发
- 涉及资金流向，一旦真越权可造成用户资金错动
