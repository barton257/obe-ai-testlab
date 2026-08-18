/**
 * SPARTANS 订阅按钮国际化。
 * 覆盖 SPARTANS_SUBSCRIBE_TEST_STRATEGY.md §3.4 第 5 行。
 *
 * 探路结论（2026-08-17）：
 *   - zh-cn 路径: /zh-cn/spartan-bot/<alias>
 *   - en    路径: /spartan-bot/<alias>（无 en 前缀）
 *   - zh-tw 路径: /zh-tw/spartan-bot/<alias>
 *
 * 简单文案校验：每种语言下"订阅"按钮文本能被对应正则匹配到。
 */
import { test, expect } from '@playwright/test';
import { gotoWithRetry } from './fixtures/nav';

const BOT_ALIAS = 'Kakarotto';

const cases = [
  { locale: 'zh-CN', urlSeg: '/zh-cn', label: /订阅/ },
  { locale: 'en',    urlSeg: '',        label: /Subscribe/i },
  { locale: 'zh-TW', urlSeg: '/zh-tw', label: /訂閱/ },
];

test.describe('订阅按钮 i18n', () => {
  for (const { locale, urlSeg, label } of cases) {
    test(`${locale} — 详情页显示订阅按钮`, async ({ page }) => {
      await gotoWithRetry(page, `${urlSeg}/spartan-bot/${BOT_ALIAS}`);
      await expect(page.getByRole('button', { name: label }).first()).toBeVisible();
    });

    test(`${locale} — 详情页可以打开订阅弹窗`, async ({ page }) => {
      await gotoWithRetry(page, `${urlSeg}/spartan-bot/${BOT_ALIAS}`);
      // 打开订阅弹窗（点第二个订阅按钮），断言金额输入框出现
      await page.getByRole('button', { name: label }).nth(1).click();
      const amountInput = page.locator('input[type=number][placeholder]').first();
      await expect(amountInput).toBeVisible();
    });
  }
});
