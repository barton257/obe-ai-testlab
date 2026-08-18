# tests/e2e/

斯巴达 UI 端到端测试（Playwright + TypeScript）。

## 首次准备

```bash
cd projects/spartans/tests/e2e
npm install
npx playwright install chromium

# 确保根目录 .env.local 有 AUTH_TOKEN 和 SPARTANS_FRONTEND_BASE
```

## 常用命令

> ⚠️ `subscribe-happy` 会**真实下单扣款**（默认 1 USDT），目前没有专用资金账户，
> 日常回归请用下面的"排除 happy"命令。

```bash
# 全量回归（排除真实下单）—— 日常用这条
npx playwright test --grep-invert "happy path"

# 跑 happy path（会真实扣款）
npm run test:happy

# 有头模式（看浏览器操作）
npm run test:headed

# UI 交互调试模式
npm run test:ui

# 用 codegen 校准选择器（推荐首次跑 happy 前用）
npm run codegen

# 全部
npm test

# 看 HTML 报告
npm run report
```

## 目录结构

```
tests/e2e/
├── package.json                     依赖 + npm scripts
├── playwright.config.ts             全局配置（loads .env.local）
├── auth.setup.ts                    UI 登录并保存 storageState（User1）
├── .auth/
│   └── user1.json                   认证状态（gitignore）
├── fixtures/
│   ├── auth.ts                      [已废弃] JWT fixture 方案
│   ├── login.ts                     登录辅助函数
│   └── nav.ts                       gotoWithRetry：连接类错误重试
├── subscribe-happy.spec.ts          ✅ 订阅 happy path（P0）
├── subscribe-frontend-validation.spec.ts  ✅ 金额校验 5 条（P0）
├── subscribe-risk-disclosure.spec.ts      ✅ 风险披露 3 条（P0）
├── subscribe-i18n.spec.ts                 ✅ 国际化 6 条（P1）
├── subscribe-logout.spec.ts               ✅ 未登录限制（P1）
└── login.spec.ts                          ✅ 登录流程（P1，用 User2）
```

对应策略文档：[`SPARTANS_SUBSCRIBE_TEST_STRATEGY.md §3.4`](../../docs/SPARTANS_SUBSCRIBE_TEST_STRATEGY.md)。

## 认证策略

使用 `auth.setup.ts` 通过真实 UI 登录流程，将认证状态保存到 `.auth/user1.json`，后续测试复用此 storageState。

工作流程：
1. `auth.setup.ts` 运行一次，使用 `USER1_EMAIL` + `USER1_PASSWORD` + Testnet 固定 OTP `123456` 登录
2. 登录后访问 Kakarotto 详情页确保会话有效
3. 将 cookies 和 localStorage 保存到 `.auth/user1.json`
4. `chromium` project 的所有测试自动加载此认证状态

优点：
- 接近真实用户登录流程，覆盖登录服务可用性
- 每次测试运行重新生成认证状态，避免过期 token
- 与 API 测试共享凭证（都从 `.env.local` 读取）
- 避免每个测试重复登录，节省时间

限制：
- 所有认证测试依赖登录服务可用性
- 缺少 `.env.local` 配置时整个 chromium 测试集失败
- Token 过期后需重新运行 setup — 见 [roadmap P2-20](../../../roadmap/2026-08-17-p0-p2.md)
- 登录流程本身的测试需独立编写（见 `login.spec.ts`，使用 `anon` project）

storageState 文件位置：`.auth/user1.json`（gitignore）

### ⚠️ 登录只发生在两个地方

1. `auth.setup.ts` —— 抓 User1 的 storageState，供所有 chromium 用例复用
2. `login.spec.ts` —— 覆盖登录流程本身，**必须用 User2**

**不要给业务 spec 加登录逻辑。** 服务端 session 单点，任何额外的 User1 登录都会顶掉
setup 抓的 session，导致后续用例全部弹 auth-modal。

### 已解决：全量跑登录态失效（原 TODO P0-1）

2026-08-18 定因并修复。根因是 `login.spec.ts` 用 User1 真实登录，顶掉了 setup 的 session。

隔离实验（同一 commit）：

| 运行范围 | 含 login.spec.ts | 结果 |
|---|---|---|
| 仅 chromium | 否 | 15 passed |
| 全量 | **是（User1）** | **9 failed** |
| 全量去掉 login.spec | 否 | 仅 1 failed（网络抖动） |

修复：`login.spec.ts` 改用 User2。连续三轮全量跑 17/17 通过。

判据留档：金额校验用例失败时先看按钮状态 —— `enabled` 是真缺陷复现，
`disabled` 则大概率是登录态丢了（未登录时按钮本来就禁用），别误判成前端已修复。

### 网络抖动重试

Testnet 偶发 `ERR_CONNECTION_CLOSED`。所有 `page.goto` 走 `fixtures/nav.ts` 的
`gotoWithRetry`（3 次，退避 1s/2s，仅对连接类错误重试）。

没有开 `playwright.config.ts` 的全局 `retries` —— 整条用例重试会掩盖真实的断言不稳定，
上面的 P0-1 正是靠"稳定复现的失败"才定位到的。

## 编写要求

- 每个 spec 头部注释对应策略章节和优先级
- 优先用语义定位（`getByRole` / `getByText`），避免 CSS 深度选择器
- 测试之间独立：不依赖上一个 spec 的状态
- 敏感数据从 `.env.local` 读取，不硬编码
- 选择器不确定时先跑 `npm run codegen` 校准
