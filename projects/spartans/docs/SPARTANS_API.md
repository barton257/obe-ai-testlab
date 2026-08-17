# SPARTANS 接口清单（Testnet）

> 来源：Testnet 前端 JS 反爬 + 实调（2026-08-17）
> Base URL: `https://bullapitest.1bullex.com`
> 认证：Bearer JWT（`authorization` 头），同时需 `identify`、`platform: WEB`、`x-client-version: 1.0.0`
> 响应结构：`{ code, msg, data, timestamp }`，`code == 0` 表示成功

## 通用响应错误码

| code | 场景 | 备注 |
|---|---|---|
| 0 | 成功 | `msg` 通常为 `null` 或 `"success"` |
| 1 | 业务错误 | 具体见 `msg` 字段（枚举字符串） |
| 401 | 未认证 | header 缺 token 或 token 无效 |

已见 `msg` 枚举：
- `amount_not_allowed` — 订阅金额不允许（0 会命中）
- `balance_not_enough` — 钱包 USDT 不足
- `private_bot_subscribe_denied` — botId 不存在或私域白名单
- `Missing Authorization header` — 401 层面

## 批次处理窗口

| 环境 | 订阅 | 赎回 |
|---|---|---|
| Testnet | 10 min | 10 min |
| 生产 | 1 hour | 1 hour |

订阅/赎回接口**同步返回 success**，但 `invest/history` 里的记录会先出现 `status=Init, tradeUnits=0`，等批次窗口过后变为 `Finished` 并铸造份额。

## 机器人相关

### POST `/botapi/v1/bot/list`
分页列出机器人。

请求体：
```json
{
  "asc": false,
  "orderBy": ["updated_at"],
  "page": 1,
  "limit": 10,
  "botAlias": "",
  "strategyType": "",
  "reserved": false,
  "days": 7,
  "tags": ""
}
```

⚠️ **坑**：
- `orderBy` 必须是数组，传字符串返回 `请求体格式错误`
- `tags` 必须是字符串（"" 或 "Private"），传数组返回 `请求体格式错误`

响应关键字段：`data.total`, `data.bots[].{id, nameAlias, strategyType, status, aum, nav, roi7d/30d/90d, totalPnl, profitShareRatio, axisLabel, axisValue}`

### POST `/botapi/v1/bot/detail`
```json
{"botAlias": "Kakarotto", "days": 30}
```
响应包含 `profitShareRatio`（分润比例，默认 10，每机器人可配）、`aum`、`nav`、`totalUser/curUser`、`description`（HTML）、7 日走势数组。

### POST `/botapi/v1/bot/all/concise`
`{}` — 返回全量机器人的极简列表：`name / roi7d / roi30d / roi90d / avatar`。

### GET `/botapi/v1/bot/summary`
无参 —— 整站聚合：`topRoi`, `totalNav`, `totalSubscribers`。

### POST `/botapi/v1/bot/recommend/top3`
`{}` — 首页推荐 3 个机器人。

### POST `/botapi/v1/bot/position/current`
```json
{"strategyId": <int>, "page": 1, "pageSize": 20}
```

### POST `/botapi/v1/bot/trade/histroy`（拼写错误，服务端原样）
同上入参，返回机器人的历史成交。

## 订阅/赎回

### POST `/botapi/v1/invest/purchase`
```json
{"userId": "10732164", "botId": 1342, "amount": 1}
```
- 同步返回 `{code:0, msg:"success"}`
- `invest/history` 里立即出现一条 `tradeType=Purchase, status=Init, tradeUnits=0`
- 等下一个批次窗口后 `status=Finished`，`tradeUnits` 为铸造份额

### POST `/botapi/v1/invest/redeem`
```json
{"userId": "10732164", "botId": 1342, "settleAmount": 1}
```
- `settleAmount` 是要赎回的**金额（USDT）**，不是份额
- 同步返回 success，实际结算等批次

### POST `/botapi//v1/invest/cancel`（前端路径带双斜杠）
```json
{"userId": "10732164", "botId": 1342}
```
取消尚未处理的订阅/赎回请求。

### POST `/botapi/v1/invest/history`
```json
{"page": 1, "limit": 10, "userId": "10732164"}
```
返回该用户所有订阅/赎回记录。字段：`tradeType (Purchase/Redeem)`, `status (Init/Finished)`, `tradeAmount`, `tradeUnits`, `createdAt`, `updatedAt`。

## 用户资产

### POST `/botapi/v1/invest/user/summary`
`{}` — 顶部资产卡：`total`、`availableBalance`、`estTotalValue`。

### GET `/botapi/v1/invest/user/board`
分布图：`distributions[]` 每个 bot 占比 + Available Balance；`subscription`、`roi`、7 日 axis。

### GET `/botapi/v1/invest/user/board/linechart?days=7`
折线图数据，`days` 可选 7/30/90。

## 疑似缺陷（详见 `projects/spartans/bugs/`）

| # | 现象 | 期望 |
|---|---|---|
| 1 | `purchase amount=0.5` 返回 success（Tier 最小值应为 1） | 应拒绝，`amount_below_min` |
| 2 | `redeem settleAmount=999999999` 返回 success，远超权益 | 应拒绝，`settle_amount_exceeds` |
| 3 | `purchase` 时 `userId` 与 JWT 不匹配返回 success | 应用 JWT 中 `api` 字段校验，拒绝跨用户操作 |
