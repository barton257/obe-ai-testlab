# funds/ — 专用资金账户台账

斯巴达测试专用资金账户的**全部资金变动记录**。任何涉及金额变化的操作都要落这里。

## 账户信息

| 项 | 值 |
|---|---|
| UID | `10732178` |
| 邮箱 | 见 `.env.local` 的 `FUNDS_EMAIL`（不入库） |
| 密码 | 见 `.env.local` 的 `FUNDS_PASSWORD`（不入库） |
| Token | 见 `.env.local` 的 `FUNDS_AUTH_TOKEN`（不入库，过期用下述命令刷新） |
| 初始入金 | **1000 USDT**（2026-08-18 开户基线，`availableBalance=1000`、历史记录 0 笔） |

Token 刷新：

```bash
source .venv/bin/activate
python scripts/spartans_login.py --user FUNDS --otp 123456 --key FUNDS_AUTH_TOKEN
```

## 文件

| 文件 | 内容 |
|---|---|
| [`LEDGER.md`](LEDGER.md) | 人读台账。按时间倒序，每笔一行，含类型/金额/流向/费用 |
| [`ledger.csv`](ledger.csv) | 同一份数据的机器可读版，便于 diff、统计、对账 |

两份必须保持一致。用 `scripts/spartans_funds_ledger.py` 同步可自动化的部分，
其余手工补录（见下）。

## 记录范围

按要求，**只要涉及资金变动就记**：

| 类型 | type 值 | 能否自动采集 |
|---|---|---|
| 订阅（下单买入机器人） | `subscribe` | ✅ `invest/history` |
| 赎回（卖出机器人份额） | `redeem` | ✅ `invest/history` |
| 账户间划转 | `transfer` | ❌ 手工 |
| 开仓 | `open_position` | ❌ 手工 |
| 平仓 | `close_position` | ❌ 手工 |
| 收益（已实现盈亏） | `pnl_realized` | ⚠️ 只能从 `user_board` 的 `rpnl` 推总量，无逐笔 |
| 分润（付给机器人主） | `profit_share` | ❌ 手工 |
| 手续费 | `fee_trading` | ❌ 手工 |
| 平台使用费 | `fee_platform` | ❌ 手工 |
| 资金费率 | `funding_rate` | ❌ 手工 |
| 其他资金变动 | `other` | ❌ 手工 |

### ⚠️ 自动化的边界（重要）

`invest/history` **只返回订阅与赎回**。截至 2026-08-18，已探测以下路径均 404
或不可达，未找到钱包流水/账单接口：

```
/botapi/v1/invest/profit/history    /botapi/v1/invest/settle/history
/botapi/v1/invest/profit/share      /api/asset/bill      /api/asset/history
/api/asset/overview                 /api/asset/list      /api/asset/spot/list
```

因此**划转、开平仓、分润、各类手续费、资金费率目前无法自动采集**，
只能手工补录。如果后端有对应接口（或前端某个页面能看到流水），
把路径告诉我，我把采集器补上 —— 这是当前台账最大的缺口。

`user_board` 能给出 `rpnl`（已实现盈亏）与 `upnl`（未实现盈亏）的**总量快照**，
可用于对账，但拿不到逐笔明细。

## 字段定义

`ledger.csv` 的列：

| 列 | 说明 |
|---|---|
| `time` | 资金变动时间，`YYYY-MM-DD HH:MM:SS`（本地时区）。自动采集用接口的 `createdAt` |
| `type` | 见上表的 type 值 |
| `amount` | 变动金额，**带符号**：账户资金减少为负、增加为正 |
| `currency` | 币种，当前均为 `USDT` |
| `from` | 资金来源。如 `available_balance`、`bot:Kakarotto`、`external` |
| `to` | 资金去向。同上取值 |
| `fee_type` | 若本笔是费用，写具体费种（`trading` / `platform` / `funding` / `profit_share`）；否则留空 |
| `ref_id` | 关联单号。订阅赎回用 `invest/history` 的 `id`；手工记录可留空 |
| `bot` | 相关机器人 alias，无则留空 |
| `balance_after` | 该笔之后的 `availableBalance`；不确定时留空 |
| `source` | `api`（自动采集）或 `manual`（手工补录） |
| `note` | 备注。测试用例产生的记录请写明用例名 |

符号约定：站在**这个账户的可用余额**视角。订阅是资金离开可用余额 → 负；
赎回回流 → 正；手续费 → 负；收到分润 → 正。

## 用法

同步订阅/赎回记录（幂等，按 `ref_id` 去重）：

```bash
source .venv/bin/activate
python scripts/spartans_funds_ledger.py sync
```

查看当前余额与台账是否对得上：

```bash
python scripts/spartans_funds_ledger.py verify
```

手工补录一笔：

```bash
python scripts/spartans_funds_ledger.py add \
  --type fee_platform --amount -0.5 --fee-type platform \
  --from available_balance --to platform \
  --note "订阅 Kakarotto 的平台使用费"
```

## 与测试用例的接线

动账用例通过 `funds_client` / `funds_uid` 两个 fixture 使用本账户
（见 `projects/spartans/tests/api/test_spartans_api.py`）。

- 余额低于 `FUNDS_MIN_BALANCE`（默认 50 USDT）时用例**直接 skip**，
  不会跑到一半才失败 —— 否则失败信息会指向业务断言，掩盖"其实没钱了"这个真实原因
- 所有动账用例带 `writes_funds` 标记，裸跑 `pytest` 不会触发

```bash
# 日常回归（不动账）
pytest projects/spartans/tests/api/test_spartans_api.py

# 动账用例（跑完记得 sync）
pytest projects/spartans/tests/api/test_spartans_api.py -m writes_funds -v
python scripts/spartans_funds_ledger.py sync
```

## 资金消耗参考

实测（2026-08-18）：

| 场景 | 单次消耗 |
|---|---|
| API E2E 主链路（订阅→等批次→赎回） | 约 0 净额（赎回回流），但期间锁 1 USDT 约 11 分钟 |
| e2e `subscribe-happy`（只订阅不赎回） | **-1 USDT，不回流** |
| xfail `below_min` | -0.5 USDT |
| xfail `wrong_user_id` | -1 USDT |
| xfail `redeem_exceeds_equity` | 清空该 bot 全部权益（回流为正） |

`subscribe-happy` 每跑一次就沉淀 1 USDT 在 bot 里不回来。1000 USDT 够跑很多轮，
但**需要定期把权益赎回**，否则可用余额会单向下降。目前没有自动清理 ——
一个完整闭环最少 11 分钟（批次窗口），做进用例会让回归变得很慢。
建议做法：订阅类用例只管下单，另设独立清理脚本定期赎回。此取舍待确认。

## 纪律

1. **每次用这个账户跑动账用例，跑完就 sync**，不要攒着
2. 手工类记录当场补，事后回忆容易漏
3. `verify` 报不平时先查是不是有未采集的费用类记录，不要直接改数字凑平
4. 台账只增不改；写错了追加一条冲正记录并在 `note` 说明，不要删行
