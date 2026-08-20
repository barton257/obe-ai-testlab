/**
 * 登录流程本身的 e2e 覆盖。
 * 覆盖：邮箱 OTP 双因素登录，Testnet OTP 固定 123456。
 *
 * 为什么用 User2 而不是 User1（2026-08-18，TODO P0-1 定因后修改）：
 *   本 spec 会真实登录，服务端 session 单点 —— 用 User1 会把 auth.setup.ts
 *   抓的 User1 session 顶掉，导致后续 chromium 用例全部弹 auth-modal。
 *   实测：排除本 spec → 15 passed；含本 spec（用 User1）→ 9 failed。
 *   本 spec 是"验证登录流程"，与账号无关，因此改用 User2 隔离。
 *   ⚠️ 不要改回 User1，也不要给其他 spec 加登录 —— 登录只发生在 setup 和这里。
 */
import { test, expect } from '@playwright/test';
import { loginViaUI } from './fixtures/login';

test.describe('登录流程', () => {
  test('User2 邮箱 + 密码 + OTP 登录成功', async ({ page }) => {
    const email = process.env.USER2_EMAIL!;
    const password = process.env.USER2_PASSWORD!;
    if (!email || !password) test.skip(true, 'USER2_EMAIL/PASSWORD 未配置');

    await loginViaUI(page, { email, password });

    await expect(page).not.toHaveURL(/\/login/);
    // 登录成功后右上角昵称/头像应出现（选择器需 codegen 二次校准）
    // await expect(page.getByRole('link', { name: /我的|Profile/ })).toBeVisible();
  });
});
