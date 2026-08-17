/**
 * 通过注入 JWT 到 cookie + localStorage 快速登录。
 *
 * 前提：.env.local 中 AUTH_TOKEN 有效（当前 User1 token 有效期至 2027-08）。
 *
 * 前端会同时读：
 *   - cookie `auth_token`（服务端 SSR 判定登录态）
 *   - localStorage `auth-storage`（Zustand persist store，客户端 hydrate 用）
 * 缺任一路径都会弹登录框。
 */
import { test as base, expect, type Page } from '@playwright/test';

export type AuthedFixtures = {
  authedPage: Page;
};

const FRONTEND_BASE = process.env.SPARTANS_FRONTEND_BASE ?? 'https://testnet.1bullex.com';
const AUTH_TOKEN = process.env.AUTH_TOKEN;
const USER_EMAIL = process.env.USER1_EMAIL ?? '';
const USER_UID = process.env.USER1_UID ?? '';

export const test = base.extend<AuthedFixtures>({
  authedPage: async ({ browser }, use) => {
    if (!AUTH_TOKEN) throw new Error('AUTH_TOKEN 未设置，检查 .env.local');
    const url = new URL(FRONTEND_BASE);
    const context = await browser.newContext({ baseURL: FRONTEND_BASE, locale: 'zh-CN' });

    // 1) cookie（不带 "Bearer " 前缀，与真实登录后一致）
    await context.addCookies([
      { name: 'auth_token', value: AUTH_TOKEN, domain: `.${url.hostname.split('.').slice(-2).join('.')}`, path: '/', httpOnly: false, secure: true, sameSite: 'Lax' },
      { name: 'locale',     value: 'zh-CN',    domain: url.hostname, path: '/', httpOnly: false, secure: true, sameSite: 'Lax' },
    ]);

    // 2) 在页面加载前注入 localStorage 的 auth-storage
    const authStorage = {
      state: {
        token: `Bearer ${AUTH_TOKEN}`,
        isAuth: true,
        userInfo: {
          UUID: USER_UID,
          email: USER_EMAIL,
          currency: 'USDT',
          isKYC: false,
          isEmailBind: true,
        },
      },
      version: 0,
    };
    await context.addInitScript(([key, val]) => {
      window.localStorage.setItem(key, val);
    }, ['auth-storage', JSON.stringify(authStorage)]);

    const page = await context.newPage();
    await use(page);
    await context.close();
  },
});

export { expect };
