# tests/e2e/

斯巴达 UI 端到端测试。

## 技术选型

- Playwright（TypeScript）
- 使用 `automation/page-objects/` 里的通用组件

## 运行

```bash
# 项目根目录
npm install                                         # 首次
npx playwright install                              # 首次
npx playwright test projects/spartans/tests/e2e/
```

## 编写要求

- 每个 `*.spec.ts` 头部注释对应 YAML 用例路径
- 优先用语义定位（`getByRole` / `getByText`），避免 CSS 深度选择器
- 测试之间独立：每个测试自己登录、自己造数据、自己清理
- 敏感数据从 `.env.local` 读取，不硬编码

## 占位样例

- [`subscribe.spec.ts`](subscribe.spec.ts) — 骨架示例
