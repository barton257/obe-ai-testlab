import { defineConfig, devices } from '@playwright/test';
import * as path from 'path';
import * as dotenv from 'dotenv';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// 加载 obe-ai-testlab 根目录的 .env.local
dotenv.config({ path: path.resolve(__dirname, '../../../../.env.local') });

const FRONTEND_BASE = process.env.SPARTANS_FRONTEND_BASE ?? 'https://testnet.1bullex.com';

export default defineConfig({
  testDir: '.',
  timeout: 60_000,
  expect: { timeout: 10_000 },
  fullyParallel: false,
  workers: 1,
  reporter: [['list'], ['html', { open: 'never', outputFolder: 'playwright-report' }]],
  use: {
    baseURL: FRONTEND_BASE,
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    locale: 'zh-CN',
    viewport: { width: 1440, height: 900 },
  },
  projects: [
    // setup: UI 登录抓 storageState
    { name: 'setup', testMatch: /auth\.setup\.ts$/ },

    // 认证态下跑的业务 spec
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
        storageState: path.resolve(__dirname, '.auth/user1.json'),
      },
      dependencies: ['setup'],
      testIgnore: [/auth\.setup\.ts$/, /login\.spec\.ts$/, /subscribe-logout\.spec\.ts$/],
    },

    // 未登录场景单独 project，不加载 storageState
    {
      name: 'anon',
      use: { ...devices['Desktop Chrome'] },
      testMatch: /(login|subscribe-logout)\.spec\.ts$/,
    },
  ],
});
