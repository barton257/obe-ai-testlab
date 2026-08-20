/**
 * 带重试的页面导航。
 *
 * 为什么需要（2026-08-18，TODO P0-1 排查产出）：
 *   Testnet 前端偶发 net::ERR_CONNECTION_CLOSED，page.goto 直接抛错。
 *   实测同一批用例连续三轮，命中的 spec 每次都不同（i18n / risk-disclosure 轮换），
 *   属于连接层抖动，不是用例缺陷。
 *
 * 为什么不用 playwright.config.ts 的 retries：
 *   整条用例重试会顺带掩盖真实的断言不稳定 —— 例如 P0-1 的 auth-modal 问题
 *   本身就是靠"稳定复现的失败"才定位到的。这里只对导航这一个动作重试，
 *   业务断言失败仍然一次就红。
 */
import type { Page } from '@playwright/test';

const CONNECTION_ERRORS = [
  'ERR_CONNECTION_CLOSED',
  'ERR_CONNECTION_RESET',
  'ERR_NETWORK_CHANGED',
  'ERR_EMPTY_RESPONSE',
];

export async function gotoWithRetry(
  page: Page,
  url: string,
  attempts = 3,
): Promise<void> {
  let lastError: unknown;

  for (let i = 1; i <= attempts; i++) {
    try {
      await page.goto(url);
      return;
    } catch (error) {
      lastError = error;
      const message = error instanceof Error ? error.message : String(error);
      const isTransient = CONNECTION_ERRORS.some((code) => message.includes(code));

      // 非连接类错误（4xx/超时/选择器等）立即抛出，不浪费重试次数
      if (!isTransient || i === attempts) throw error;

      // 退避后重试：1s、2s
      await page.waitForTimeout(1_000 * i);
    }
  }

  throw lastError;
}
