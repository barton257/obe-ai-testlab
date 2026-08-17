/**
 * SPARTANS 订阅 happy path — 用户视角完整走一遍。
 *
 * 覆盖 SPARTANS_SUBSCRIBE_TEST_STRATEGY.md §3.4 第 1 行。
 * 选择器基于 2026-08-17 codegen 校准。
 *
 * 认证：由 auth.setup.ts 抓的 .auth/user1.json 提供。
 * 前提：Kakarotto bot 处于 Running 状态，User1 钱包可用余额 ≥ 1 USDT。
 */
import { test, expect } from '@playwright/test';

const BOT_ALIAS = 'Kakarotto';
const AMOUNT = process.env.SPARTANS_E2E_AMOUNT ?? '1';

test.describe('订阅 happy path', () => {
  test('1 USDT 订阅 Kakarotto，走完完整确认链路', async ({ page }) => {
    // 1. 打开机器人详情
    await page.goto(`/zh-cn/spartan-bot/${BOT_ALIAS}`);
    await expect(page).toHaveURL(new RegExp(BOT_ALIAS));

    // 2. 页面上有两个"订阅"按钮（顶部 + 侧栏），点第二个弹出订阅框
    await page.getByRole('button', { name: '订阅' }).nth(1).click();

    // 3. 输入金额
    const amountInput = page.getByRole('spinbutton', { name: '请输入金额' });
    await expect(amountInput).toBeVisible();
    await amountInput.fill(AMOUNT);

    // 4. 勾选风险披露（弹窗内第一个 checkbox；被 span 包裹要 force）
    await page
      .getByRole('dialog')
      .getByRole('checkbox')
      .first()
      .setChecked(true, { force: true });

    // 5. 提交
    await page.getByRole('button', { name: '确认' }).click();

    // 6. 成功弹窗 → 点"好的"关闭
    const successBtn = page.getByRole('button', { name: '好的' });
    await expect(successBtn).toBeVisible({ timeout: 15_000 });
    await successBtn.click();

    // 7. 打开"我的订阅"验证记录出现
    await page.getByRole('button', { name: '我的订阅' }).click();
    await expect(
      page.getByRole('heading', { name: BOT_ALIAS }).first(),
    ).toBeVisible();
  });
});
