# page-objects/

页面对象模型（Page Object Model, POM）。封装 UI 元素定位与操作，供 E2E 测试调用。

---

## 当前状态

**未采用 POM 模式。** E2E 用例直接在 spec 文件中定位元素：

```typescript
// projects/spartans/tests/e2e/subscribe-risk-disclosure.spec.ts
await page.locator('button[data-testid="subscribe-btn"]').click();
await page.locator('input[type="checkbox"]').uncheck();
```

---

## POM 的价值

**何时需要**：
1. 同一个 UI 元素在 ≥3 个用例中重复定位
2. 元素定位器复杂（多层嵌套、动态属性）
3. 前端频繁改版，集中维护定位器降低维护成本

**何时不需要**（当前情况）：
- 用例总数 < 20 条
- UI 相对稳定，改版频率 < 1 次/月
- 定位器简单（`data-testid` / `role` / 简单 CSS）

**过早抽象的代价**：
- 改一个按钮要动 3 个文件（page object + 多个 spec）
- 调试时要跨文件跳转，查元素定位在哪
- 新人写用例要先学 POM API

---

## 如果要接入

### 结构

```
page-objects/
  spartans/
    bot-list.page.ts        # 机器人列表页
    bot-detail.page.ts      # 机器人详情页
    subscribe-modal.page.ts # 订阅弹窗
    user-center.page.ts     # 用户中心
```

### 示例

```typescript
// bot-detail.page.ts
export class BotDetailPage {
  constructor(private page: Page) {}

  async goto(botId: string) {
    await this.page.goto(`/zh-cn/bots/${botId}`);
  }

  async clickSubscribe() {
    await this.page.locator('[data-testid="subscribe-btn"]').click();
  }

  async getNavValue() {
    return this.page.locator('[data-testid="nav-value"]').textContent();
  }
}
```

用例中：
```typescript
const botDetail = new BotDetailPage(page);
await botDetail.goto('123');
await botDetail.clickSubscribe();
```

---

## 引入时机

**触发条件（满足任一即考虑引入）**：
1. E2E 用例总数 > 30 条
2. UI 一个月内改版 ≥2 次，导致批量改定位器
3. 出现 ≥3 个用例因同一个元素定位失效而失败

在此之前保持当前直接定位的方式，**不要为了"架构完整性"强行抽象**。

---

## 替代方案

若只是想复用定位器，不必上 POM，可用 **locator 常量**：

```typescript
// projects/spartans/tests/e2e/locators.ts
export const LOCATORS = {
  subscribeBtn: '[data-testid="subscribe-btn"]',
  riskCheckbox: 'input[type="checkbox"][name="risk-disclosure"]',
  confirmBtn: 'button:has-text("确认")',
};

// 用例中
import { LOCATORS } from './locators';
await page.locator(LOCATORS.subscribeBtn).click();
```

这是 POM 的轻量替代，适合当前规模。

---

## 相关

- E2E 测试：[`../projects/spartans/tests/e2e/`](../projects/spartans/tests/e2e/)
- Playwright 最佳实践：[官方文档 - Page Object Models](https://playwright.dev/docs/pom)
