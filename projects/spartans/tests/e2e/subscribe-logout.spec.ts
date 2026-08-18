/**
 * SPARTANS 未登录访问订阅入口 → 应跳登录 or 弹登录框。
 * 覆盖 SPARTANS_SUBSCRIBE_TEST_STRATEGY.md §3.4 第 4 行。
 *
 * 这条 spec 归 `anon` project（无 storageState），见 playwright.config.ts。
 * 探路结论：未登录时 subscribe-happy 第一次跑就弹了登录页 —— 校验此行为。
 */
import { test, expect } from '@playwright/test';
import { gotoWithRetry } from './fixtures/nav';

const BOT_ALIAS = 'Kakarotto';

test.describe('未登录订阅', () => {
  test('未登录访问机器人详情页可以浏览但点订阅会跳登录', async ({ page }) => {
    await gotoWithRetry(page, `/zh-cn/spartan-bot/${BOT_ALIAS}`);
    // 详情页本身应可见（公开）
    await expect(page.getByRole('heading', { name: BOT_ALIAS })).toBeVisible();

    // 未登录时页面右上角应有"登录"入口
    await expect(page.getByRole('link', { name: '登录' })).toBeVisible();

    // 点订阅按钮
    await page.getByRole('button', { name: '订阅' }).first().click();

    // 期望之一：跳到 /login 页 或 弹出登录框
    const onLogin = page.waitForURL(/\/login/, { timeout: 5_000 })
      .then(() => 'redirected');
    const loginDialog = page.getByRole('textbox', { name: '输入邮箱' })
      .waitFor({ state: 'visible', timeout: 5_000 })
      .then(() => 'dialog');

    const outcome = await Promise.race([onLogin, loginDialog]).catch(() => null);
    expect(outcome).not.toBeNull();
  });
});
