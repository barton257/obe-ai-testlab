// 骨架示例：斯巴达订阅 UI 端到端。
// testcase: projects/spartans/testcases/spartans-subscribe-P0-正常-最小订阅金额.yaml

import { test, expect } from '@playwright/test';

test.skip('skeleton placeholder — waiting for real base URL and login flow', () => {});

test.describe('SPARTANS 订阅', () => {
  test.skip('订阅者可以在最小金额下完成订阅（skeleton）', async ({ page }) => {
    const baseUrl = process.env.OBE_TESTNET_BASE_URL!;
    const botName = 'OBE-Jason';
    const minAmount = process.env.SPARTANS_MIN_SUBSCRIBE_AMOUNT ?? '10';

    // TODO: 使用 automation/page-objects/login 完成登录
    await page.goto(`${baseUrl}/zh-cn/spartan-bot/${botName}`);

    await page.getByRole('button', { name: '订阅' }).click();
    await page.getByPlaceholder(/USDT/i).fill(minAmount);
    await page.getByLabel(/风险披露/).check();
    await page.getByRole('button', { name: '确认' }).click();

    await expect(page.getByText(/订阅已提交/)).toBeVisible();

    await page.goto(`${baseUrl}/zh-cn/spartan-subscriptions`);
    await expect(
      page.getByRole('cell', { name: new RegExp(`订阅 ${botName}`) }),
    ).toBeVisible();
  });
});
