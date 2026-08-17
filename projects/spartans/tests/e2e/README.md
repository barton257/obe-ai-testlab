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

```bash
# 跑 happy path
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
├── fixtures/
│   └── auth.ts                      注入 JWT cookie 跳过登录
├── subscribe-happy.spec.ts          ✅ 完整实现（P0）
├── subscribe-frontend-validation.spec.ts  ⏳ 占位（P1，4 条 skip）
├── subscribe-risk-disclosure.spec.ts      ⏳ 占位（P1，2 条 skip）
├── subscribe-i18n.spec.ts                 ⏳ 占位（P1，3 条 skip）
└── subscribe-logout.spec.ts               ⏳ 占位（P1，1 条 skip）
```

对应策略文档：[`SPARTANS_SUBSCRIBE_TEST_STRATEGY.md §3.4`](../../docs/SPARTANS_SUBSCRIBE_TEST_STRATEGY.md)。

## 认证策略

用 `fixtures/auth.ts` 注入 `.env.local` 中的 `AUTH_TOKEN` 到 cookie，跳过邮箱密码登录流程。

优点：
- 快，无需每条 spec 都跑一次真实登录
- 稳定，不受登录页 DOM 变化影响
- 与 API 测试共享同一 token

限制：
- 无法覆盖登录流程本身（登录测试需另建 `login.spec.ts`）
- Token 过期后所有 e2e 失败 —— 见 [roadmap P2-20](../../../roadmap/2026-08-17-p0-p2.md)

## 编写要求

- 每个 spec 头部注释对应策略章节和优先级
- 优先用语义定位（`getByRole` / `getByText`），避免 CSS 深度选择器
- 测试之间独立：不依赖上一个 spec 的状态
- 敏感数据从 `.env.local` 读取，不硬编码
- 选择器不确定时先跑 `npm run codegen` 校准
