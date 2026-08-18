# 环境定义

各环境的入口、用途、可做与不可做。**不含任何凭证** —— 真值走 `.env.local`，
模板见 [`../secrets/spartans.example.env`](../secrets/spartans.example.env)。

---

## 环境列表

| 环境 | API Base | 前端 | 当前状态 |
|---|---|---|---|
| **Testnet** | `https://bullapitest.1bullex.com` | `https://testnet.1bullex.com` | ✅ 唯一在用 |
| Staging | 未确认 | 未确认 | ❓ 是否存在待确认 |
| Prod | 不写 | 不写 | 🚫 禁止自动化接入 |

环境变量键名：`SPARTANS_API_BASE` / `SPARTANS_FRONTEND_BASE`。
所有测试代码通过这两个变量读取，**不要在代码里硬编码域名**
（`playwright.config.ts` 和 `spartans_login.py` 有 fallback 默认值，仅为本地便利，
CI 必须显式注入）。

---

## Testnet

当前所有自动化的唯一目标环境。

### 特性

| 项 | 值 | 影响 |
|---|---|---|
| 邮箱 OTP | **固定 `123456`** | 登录可自动化，无需抓邮箱 |
| 订阅/赎回批次窗口 | **10 分钟** | E2E 等待用 `SPARTANS_BATCH_WINDOW_SECS`（默认 660s = 11min，留 1min 余量） |
| 结算时区 | UTC+0 | 跨日断言注意时差 |
| 简中路径 | `/zh-cn/*` | E2E `locale: 'zh-CN'` |
| 资金 | 真实扣款（测试币） | 见下方红线 |

### 已知不稳定

- **TLS 握手偶发断连** — `SSLEOFError` / `ERR_CONNECTION_CLOSED`。
  已在两处处理：`automation/clients/obe_http.py` 只重试 connect 阶段，
  `tests/e2e/fixtures/nav.ts` 的 `gotoWithRetry` 重试导航。
  实测同批用例连续三轮，命中的用例每次不同 ⇒ 连接层抖动，非用例缺陷。
- **bot 状态在结算窗口内变 `Settling`** — 断言 bot 状态时不要写死 `Running`。

### 红线

- Testnet 的钱**是真的会扣的**（测试币，但余额有限）。
  动账用例统一走专用资金账户，见 [`test-accounts.md`](test-accounts.md)。
- 压测只能打 Testnet / Staging，**禁止对生产施压**。

---

## Staging

是否存在、入口地址、与 Testnet 的数据隔离关系 —— **均未确认**。

待确认项（需问后端 / SRE）：

1. 有没有 Staging？入口是什么？
2. 批次窗口是否也是 10 分钟？
3. 账号体系与 Testnet 是否共通？
4. 能否用于压测？

确认后回填本节。在此之前所有文档不要假设 Staging 存在。

---

## Prod

**不接入自动化。** 本文件刻意不记录生产地址，避免误配 `SPARTANS_API_BASE` 打到生产。

生产相关口径（仅作对照，不用于测试）：

- 批次窗口：**1 小时**（Testnet 是 10 分钟，写用例时注意这个差异不要写死）

---

## 多地域

当前无地域差异需求。若未来出现（不同 region 的合约参数、限额不同），
新建 `regions.md` 记录，本节留指针。

---

## 相关

- 账号角色约定：[`test-accounts.md`](test-accounts.md)
- 凭证模板：[`../secrets/spartans.example.env`](../secrets/spartans.example.env)
- 术语：[`../glossary.md`](../glossary.md)
