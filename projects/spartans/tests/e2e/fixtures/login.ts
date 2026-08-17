/**
 * 通过 UI 登录的通用 helper（含邮箱 OTP，Testnet 固定 123456）。
 *
 * 之所以还留 UI 登录：`fixtures/auth.ts` 是 JWT 注入 cookie 跳过 UI；
 * 但登录流程本身也要被 e2e 覆盖，此 helper 支持 login.spec.ts。
 */
import type { Page } from '@playwright/test';

export interface LoginCreds {
  email: string;
  password: string;
  otp?: string;
}

export async function loginViaUI(page: Page, creds: LoginCreds): Promise<void> {
  const otp = creds.otp ?? '123456'; // Testnet 固定 OTP

  await page.goto('/zh-cn/login');

  await page.getByRole('textbox', { name: '输入邮箱' }).fill(creds.email);
  await page.getByRole('textbox', { name: '输入登录密码' }).fill(creds.password);
  await page.getByRole('button', { name: '登录' }).click();

  // 邮箱 OTP 弹窗
  await page.getByRole('textbox', { name: 'Verification code' }).fill(otp);

  // 登录成功后会跳转到首页或 landing；等 URL 变化断言登录完成
  await page.waitForURL((url) => !/\/login/.test(url.pathname), { timeout: 15_000 });
}
