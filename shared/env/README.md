# env/

环境定义。只写"哪些环境存在、约定的账号角色、可访问入口"，**不写真实凭证**。

## 建议文件

- `environments.md` — 环境列表（Testnet / Staging / Prod）
- `test-accounts.md` — 测试账号角色约定（订阅者 A/B、创建者 A/B、审核员）
- `regions.md` — 多地域差异（如涉及）

## 真实凭证

一律不入库。使用者在本地 `.env.local`（已 gitignore）配置，示例模板放 `../secrets/`。
