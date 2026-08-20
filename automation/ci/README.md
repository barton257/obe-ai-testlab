# ci/

CI 配置与流水线脚本。**只存 CI 逻辑**（跑什么、什么时机触发、输出报告格式），
不存业务用例。

---

## 当前状态

**未接入 CI。** 本目录占位，所有内容待补充。

---

## 待确认

需与 SRE / DevOps 确认：

1. **CI 平台** — GitHub Actions / GitLab CI / Jenkins / 其他？
2. **触发时机** — PR / merge to main / 定时（如每日 smoke）？
3. **环境隔离** — Testnet 用哪个 runner？是否有专用 IP 段？
4. **凭证注入** — Token 如何刷新？
   - Testnet OTP 固定 `123456`，可在 CI 步骤调登录接口自动换 token
   - 或手工维护 Secrets 里的 token（会过期，需定期人肉刷新）
5. **报告上传** — Allure / HTML / 接入内部平台？
6. **通知** — 失败通知到哪里（Slack / 企微 / 邮件）？
7. **并发控制** — 动账用例是否需串行队列？

---

## 建议文件

待 CI 接入后补充：

- `github-actions.yml` 或 `.gitlab-ci.yml` — 流水线定义
- `smoke-daily.sh` — 每日 smoke 脚本（API 只读 + E2E happy path）
- `regression-full.sh` — 完整回归（含 `writes_funds`，需人工触发）
- `setup-env.sh` — CI 环境初始化（安装依赖、启动浏览器、健康检查）
- `allure-report.sh` — 报告生成与上传（若用 Allure）

---

## 本地验证命令

在接入 CI 之前，脚本应先在本地验证通过：

```bash
# API smoke（只读，可随时跑）
source .venv/bin/activate
pytest projects/spartans/tests/api/ -v

# E2E smoke（只读，需登录态）
npx playwright test --grep-invert '@writes_funds'

# 完整回归（含动账，需确认资金账户余额）
pytest projects/spartans/tests/api/ -v -m writes_funds
npx playwright test  # 全量
```

---

## 相关

- 测试账号约定：[`../shared/env/test-accounts.md`](../shared/env/test-accounts.md)
- 环境定义：[`../shared/env/environments.md`](../shared/env/environments.md)
- 登录脚本：[`../scripts/spartans_login.py`](../scripts/spartans_login.py)
