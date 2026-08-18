# env/

环境定义。只写"哪些环境存在、约定的账号角色、可访问入口"，**不写真实凭证**。

## 文件

- [`environments.md`](environments.md) — 各环境入口、批次窗口、可做与不可做
- [`test-accounts.md`](test-accounts.md) — 账号角色约定（USER1/2/3/FUNDS/BOT1/2 分工与纪律）
- `regions.md` — 多地域差异（当前无需求，未来有差异时再建）

## 真实凭证

一律不入库。使用者在本地 `.env.local`（已 gitignore）配置，示例模板放 `../secrets/`。
