/**
 * 登录流程本身的 e2e 覆盖（不走 fixtures/auth.ts 的 JWT 注入）。
 * 覆盖：邮箱 OTP 双因素登录，Testnet OTP 固定 123456。
 */
import { test, expect } from '@playwright/test';
import { loginViaUI } from './fixtures/login';

test.describe('登录流程', () => {
  test('User1 邮箱 + 密码 + OTP 登录成功', async ({ page }) => {
    const email = process.env.USER1_EMAIL!;
    const password = process.env.USER1_PASSWORD!;
    if (!email || !password) test.skip(true, 'USER1_EMAIL/PASSWORD 未配置');

    await loginViaUI(page, { email, password });

    await expect(page).not.toHaveURL(/\/login/);
    // 登录成功后右上角昵称/头像应出现（选择器需 codegen 二次校准）
    // await expect(page.getByRole('link', { name: /我的|Profile/ })).toBeVisible();
  });
});
