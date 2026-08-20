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
import { gotoWithRetry } from './fixtures/nav';

const BOT_ALIAS = 'Kakarotto';
const AMOUNT = process.env.SPARTANS_E2E_AMOUNT ?? '1';

test.describe('订阅 happy path', () => {
  test('1 USDT 订阅 Kakarotto，走完完整确认链路', async ({ page }) => {
    // 1. 打开机器人详情
    await gotoWithRetry(page, `/zh-cn/spartan-bot/${BOT_ALIAS}`);
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

    // 7. 打开"我的订阅" → "操作记录"
    //    注意："进行中" tab 是按 bot 聚合的（Kakarotto 一行显示累计金额），
    //    拿不到单条订阅；单条记录只在"操作记录"里。校准于 2026-08-18。
    await page.getByRole('button', { name: '我的订阅' }).click();
    await page.getByText('操作记录', { exact: true }).click();

    // 8. 断言最新一条记录就是本次订阅
    //    表结构：["操作类型", "金额 (USDT)", "状态", "时间"]，按时间倒序，row(0) 是表头
    const latest = page.getByRole('row').nth(1);
    const cells = latest.getByRole('cell');

    await expect(cells.nth(0)).toHaveText(`订阅 ${BOT_ALIAS}`);
    // 金额为负（扣款），且绝对值等于本次订阅金额
    await expect(cells.nth(1)).toHaveText(`-${Number(AMOUNT).toFixed(2)}`);
    await expect(cells.nth(2)).toHaveText('成功');

    // 时间戳形如 "2026-08-17 21:02:05"，断言落在本次运行的 5 分钟窗口内，
    // 以此排除"历史已有同 bot 同金额订阅"导致的误通过
    const ts = (await cells.nth(3).textContent())?.trim() ?? '';
    expect(ts, `时间戳格式不符预期: ${ts}`).toMatch(/^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$/);
    const ageMs = Date.now() - new Date(ts.replace(' ', 'T')).getTime();
    expect(ageMs, `最新记录时间 ${ts} 不在近 5 分钟内，可能是历史记录`)
      .toBeLessThan(5 * 60_000);
  });
});
