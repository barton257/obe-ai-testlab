/**
 * SPARTANS 订阅前端金额校验。
 * 覆盖 SPARTANS_SUBSCRIBE_TEST_STRATEGY.md §3.4 第 2 行。
 *
 * 探路结论（2026-08-17）：
 *   - 金额输入是 <input type="number" min="1" max="999999.99">
 *   - 浏览器原生拦截非数字输入（fill('abc') 会抛错）
 *   - 风险披露默认已勾（见 subscribe-risk-disclosure.spec.ts）
 *
 * 已发现 UX 缺陷（本文件用"实际行为断言 + TODO 翻转"记录）：
 *   - amount=0/0.5/空 时前端"确认"按钮未随 min 联动禁用
 *   - 与后端 S2 穿透 bug 同源（../bugs/2026-08-17-spartans-S2-订阅金额小于最小值未拦截.md）
 */
import { test, expect, type Page } from '@playwright/test';

const BOT_ALIAS = 'Kakarotto';

async function openSubscribeDialog(page: Page) {
  await page.goto(`/zh-cn/spartan-bot/${BOT_ALIAS}`);
  await page.getByRole('button', { name: '订阅' }).nth(1).click();
  await expect(page.getByRole('spinbutton', { name: '请输入金额' })).toBeVisible();
}

test.describe('订阅前端金额校验', () => {
  test('金额输入 abc（非数字）被浏览器原生拦截', async ({ page }) => {
    await openSubscribeDialog(page);
    const amount = page.getByRole('spinbutton', { name: '请输入金额' });
    await amount.pressSequentially('abc', { delay: 50 });
    await expect(amount).toHaveValue('');
  });

  test('[UX 缺陷现状] 空金额 + 已勾风险，确认按钮仍可点（应禁用）', async ({ page }) => {
    await openSubscribeDialog(page);
    await page.getByRole('spinbutton', { name: '请输入金额' }).fill('');
    // 现状记录：期望 disabled 但实际 enabled；修复后把 not. 去掉即翻转为正断言
    await expect(page.getByRole('button', { name: '确认' })).not.toBeDisabled();
  });

  test('[UX 缺陷现状] 金额 0，确认按钮仍可点（应禁用）', async ({ page }) => {
    await openSubscribeDialog(page);
    await page.getByRole('spinbutton', { name: '请输入金额' }).fill('0');
    await expect(page.getByRole('button', { name: '确认' })).not.toBeDisabled();
  });

  test('[UX 缺陷现状] 金额 0.5（< Tier min=1），确认按钮仍可点（应禁用，S2 同源）', async ({ page }) => {
    await openSubscribeDialog(page);
    await page.getByRole('spinbutton', { name: '请输入金额' }).fill('0.5');
    await expect(page.getByRole('button', { name: '确认' })).not.toBeDisabled();
  });

  test('超过 input max 时，浏览器允许输入但值应可读回', async ({ page }) => {
    await openSubscribeDialog(page);
    const amount = page.getByRole('spinbutton', { name: '请输入金额' });
    await amount.fill('99999999999');
    // input[type=number] 允许输入超 max，只在 form 提交时才校验
    // 断言值能被读回（不空）；未来若前端加了截断/提示，改断言即可
    await expect(amount).not.toHaveValue('');
  });
});
