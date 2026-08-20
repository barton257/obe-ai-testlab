# 测试账号角色约定

各测试账号的**角色分工与使用纪律**。凭证一律不入库 —— 键名见
[`../secrets/spartans.example.env`](../secrets/spartans.example.env)，真值在本地 `.env.local`。

本文件是账号角色的**单一出处**。此前这些约定散落在 `funds/README.md`、
`tests/e2e/README.md`、`login.spec.ts` 注释、`test_spartans_api.py` 里，
互相不引用，容易改一处漏另一处。

---

## 角色总表

| 别名 | 角色 | 主要用途 | 会动账 | 关键纪律 |
|---|---|---|---|---|
| `USER1` | 主订阅者 | API 只读 smoke、E2E `storageState` 来源 | ⚠️ 部分 xfail 用例会 | 不要在其他 spec 里重新登录它 |
| `USER2` | 次订阅者 | `login.spec.ts` 登录流程、越权对照用户 | ❌ | **不要改回 USER1**，见下 |
| `USER3` | 备用订阅者 | 尚未接入任何用例 | ❌ | 有并发/多用户场景时启用 |
| `FUNDS` | 专用资金账户 | 所有 `writes_funds` 用例 | ✅ 设计如此 | 每次跑完必须 `sync` 台账 |
| `BOT1` | 机器人账号 | 提供 `BOT1_ID`（Kakarotto，默认 `1342`） | — | 当前只用 ID，未用其凭证登录 |
| `BOT2` | 机器人账号 | 备用 | — | 未接入 |

机器人账号邮箱格式：`aibot.{uid}.{botId}@onebullex.com`。

---

## USER1 — 主订阅者

**用途**：`ObeClient.from_env()` 的默认身份（`AUTH_TOKEN`），
以及 `auth.setup.ts` 抓 `storageState` 的账号。

**纪律：不要在任何 spec 里重新登录 USER1。**

服务端 session 单点 —— 二次登录会把 `auth.setup.ts` 抓的 session 顶掉，
后续所有 `chromium` project 用例弹 auth-modal 全红。
实测数据（2026-08-18）：`login.spec.ts` 用 USER1 → 9 failed；改用 USER2 → 15 passed。

登录**只允许发生在两个地方**：

1. `auth.setup.ts` —— USER1，抓 `storageState`
2. `login.spec.ts` —— USER2，覆盖登录流程本身

**注意它并非完全只读**：`TestKnownDefectRegressions` 的三条 xfail 用例走 USER1
且带 `writes_funds` 标记，缺陷穿透期间会真实下单（0.5 / 1 USDT）。
这些用例默认不跑，显式加 `-m writes_funds` 才触发。

---

## USER2 — 次订阅者 / 越权对照

两个用途：

1. **`login.spec.ts`** — 验证登录流程本身。用它而非 USER1 的原因见上。
2. **越权对照用户** — `test_purchase_wrong_user_id_rejected` 把 `USER2_UID` 填进
   请求体，验证服务端是否校验 `body.userId` 与 JWT 身份一致
   （对应 S3 缺陷，当前静默忽略）。

⚠️ 该越权用例带 `writes_funds`：缺陷未修复期间，请求会**以 USER1 身份**真实下单 1 USDT，
不是以 USER2。资金影响落在 USER1 头上。

---

## USER3 — 备用

已配置凭证与 token，**尚未被任何用例引用**。
留给后续多用户场景：并发订阅同一 bot、份额稀释对照、私域白名单准入对照。

---

## FUNDS — 专用资金账户

**唯一允许真实动账的账号。** 完整台账规范见
[`../../projects/spartans/funds/README.md`](../../projects/spartans/funds/README.md)。

| 项 | 值 |
|---|---|
| 用途 | 所有 `@pytest.mark.writes_funds` 用例 |
| 初始入金 | 1000 USDT（2026-08-18 开户基线） |
| 余额下限 | `FUNDS_MIN_BALANCE`（默认 50 USDT），低于则用例 **skip 而非 fail** |
| 接入方式 | `funds_client` / `funds_uid` fixture |

**纪律**：

1. 跑完动账用例**立刻** `python scripts/spartans_funds_ledger.py sync`，不要攒
2. 手工操作（划转、开平仓）当场 `add` 补录，事后回忆容易漏
3. 每天结束前 `verify` 一次对账
4. 不要把 FUNDS 与 USER1/2/3 混用 —— 混用会让台账对不上，且无法区分是哪条用例动的钱

**为什么余额不足是 skip 不是 fail**：fail 的报错会指向业务断言
（"订阅未成功"），掩盖"其实是没钱了"这个真实原因。

---

## Token 与刷新

| 键 | 属主 | 刷新命令 |
|---|---|---|
| `AUTH_TOKEN` | USER1 | `python scripts/spartans_login.py --user USER1` |
| `USER2_AUTH_TOKEN` | USER2 | `... --user USER2 --key USER2_AUTH_TOKEN` |
| `USER3_AUTH_TOKEN` | USER3 | `... --user USER3 --key USER3_AUTH_TOKEN` |
| `FUNDS_AUTH_TOKEN` | FUNDS | `... --user FUNDS --otp 123456 --key FUNDS_AUTH_TOKEN` |

Testnet 邮箱 OTP 固定 `123456`，所以刷新可以完全自动化
（`--otp 123456` 免交互）。生产环境需人肉抓邮箱，脚本无法绕过。

### ⚠️ CI 里的 token 是未解问题

Token 会过期。本地靠人跑 `spartans_login.py` 刷新，CI 里没有对应机制 ——
Secrets 里的 token 过期后流水线会全红且原因不直观（401 而非"token 过期"）。
可选方向：CI 步骤里先调登录接口换 token（Testnet OTP 固定，可行），
或让流水线在 401 时给出明确报错。**待与 SRE 确认后回填。**

---

## `AUTH_IDENTIFY`（设备指纹）

请求头 `identify`，所有账号共用一个值，从 `.env.local` 的 `AUTH_IDENTIFY` 读取。

⚠️ `scripts/spartans_login.py:41` 有一个硬编码 fallback 值。它是 2026-08-17
从前端抓的真实设备指纹，**属于应脱敏但当前未脱敏的项**
（`AGENTS.md` 第七节口径）。清理时注意：去掉 fallback 会让未配置该变量的
本地运行直接失败，需同步在 `spartans.example.env` 标为必填。列为待清理项。

---

## 新增账号时

1. 在 [`../secrets/spartans.example.env`](../secrets/spartans.example.env) 加键（`<email>` / `<password>` / `<uid>` 占位）
2. 在本文件角色总表加一行，写清**角色**与**会不会动账**
3. 若会动账 → 必须走 FUNDS 模式（专用账户 + 台账），不要新开一个裸账号
4. `scripts/spartans_login.py` 的 `--user` 别名列表同步更新

---

## 相关

- 环境定义：[`environments.md`](environments.md)
- 凭证模板：[`../secrets/spartans.example.env`](../secrets/spartans.example.env)
- 资金台账：[`../../projects/spartans/funds/README.md`](../../projects/spartans/funds/README.md)
- 脱敏规则：[`../../AGENTS.md`](../../AGENTS.md) 第七节
