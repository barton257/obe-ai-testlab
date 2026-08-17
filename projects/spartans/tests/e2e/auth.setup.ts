/**
 * Setup: 用 UI 登录一次，把完整浏览器 storage 保存到 .auth/user1.json。
 * 后续所有 spec 通过 playwright.config.ts 的 project.use.storageState 加载，跳过登录。
 *
 * 触发时机：
 *   - 首次运行
 *   - .auth/user1.json 过期或不存在
 *   - 手动删掉 .auth/user1.json 强制刷新
 */
import { test as setup, expect } from '@playwright/test';
import { loginViaUI } from './fixtures/login';
import * as path from 'path';
import * as fs from 'fs';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const authFile = path.resolve(__dirname, '.auth/user1.json');

setup('authenticate as User1', async ({ page, context }) => {
  const email = process.env.USER1_EMAIL;
  const password = process.env.USER1_PASSWORD;
  if (!email || !password) throw new Error('USER1_EMAIL/PASSWORD 未在 .env.local 设置');

  // 每次都重新登录，避免 storageState 里 cookie 过期导致业务 spec 失败
  // 每轮 setup 只多 ~6s，比排查过期问题划算
  if (fs.existsSync(authFile)) fs.rmSync(authFile);

  await loginViaUI(page, { email, password });

  // 断言登录成功：URL 不再是 /login，且 localStorage 有 auth-storage
  await expect(page).not.toHaveURL(/\/login/);
  const authStorage = await page.evaluate(() => localStorage.getItem('auth-storage'));
  expect(authStorage).toContain('isAuth');

  // 先进一次业务页面，让所有 store（auth-storage/user-storage）都 hydrate 后再存快照
  await page.goto('/zh-cn/spartan-bot/Kakarotto');
  await page.waitForLoadState('networkidle');

  fs.mkdirSync(path.dirname(authFile), { recursive: true });
  await context.storageState({ path: authFile });
});
