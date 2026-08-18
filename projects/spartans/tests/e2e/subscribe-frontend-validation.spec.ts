/**
 * SPARTANS 订阅前端金额校验。
 * 覆盖 SPARTANS_SUBSCRIBE_TEST_STRATEGY.md §3.4 第 2 行。
 *
 * 探路结论（2026-08-17）：
 *   - 金额输入是 <input type="number" min="1" max="999999.99">
 *   - 浏览器原生拦截非数字输入（fill('abc') 会抛错）
 *   - 风险披露默认已勾（见 subscribe-risk-disclosure.spec.ts）
 *
 * 已发现 UX 缺陷（用 test.fail() 标记，修复后移除标记即转为回归用例）：
 *   - amount=0/0.5/空 时前端"确认"按钮未随 min 联动禁用
 *   - 与后端 S2 穿透 bug 同源（../bugs/2026-08-17-spartans-S2-订阅金额小于最小值未拦截.md）
 *
 * 断言状态与登录态强相关（2026-08-18 实测，可作为 TODO P0-1 的判据）：
 *   - 单跑本文件（登录态正常）：确认按钮 enabled → 缺陷复现
 *   - 全量跑（storageState 失效弹 auth-modal）：按钮 disabled，原因是未登录而非 min 联动
 *   所以本文件失败时先确认登录态，别直接当成前端已修复。
 */
import { test, expect, type Page } from '@playwright/test';
import { gotoWithRetry } from './fixtures/nav';

const BOT_ALIAS = 'Kakarotto';

async function openSubscribeDialog(page: Page) {
  await gotoWithRetry(page, `/zh-cn/spartan-bot/${BOT_ALIAS}`);
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

  test('空金额时确认按钮应禁用', async ({ page }) => {
    test.fail(); // 已知 UX 缺陷：当前按钮未禁用，前端修复后移除此标记
    await openSubscribeDialog(page);
    await page.getByRole('spinbutton', { name: '请输入金额' }).fill('');
    await expect(page.getByRole('button', { name: '确认' })).toBeDisabled();
  });

  test('金额为 0 时确认按钮应禁用', async ({ page }) => {
    test.fail(); // 已知 UX 缺陷：当前按钮未禁用，前端修复后移除此标记
    await openSubscribeDialog(page);
    await page.getByRole('spinbutton', { name: '请输入金额' }).fill('0');
    await expect(page.getByRole('button', { name: '确认' })).toBeDisabled();
  });

  test('金额低于最小值（0.5 < 1）时确认按钮应禁用', async ({ page }) => {
    test.fail(); // 已知 UX 缺陷：当前按钮未禁用，与 S2 bug 同源，修复后移除此标记
    await openSubscribeDialog(page);
    await page.getByRole('spinbutton', { name: '请输入金额' }).fill('0.5');
    await expect(page.getByRole('button', { name: '确认' })).toBeDisabled();
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
