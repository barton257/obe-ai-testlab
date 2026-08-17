/**
 * SPARTANS 订阅风险披露必须勾选。
 * 覆盖 SPARTANS_SUBSCRIBE_TEST_STRATEGY.md §3.4 第 3 行。
 *
 * 实测行为（2026-08-17）：
 *   - 打开订阅弹窗后风险披露 checkbox 默认已勾（UX 决策）
 *   - 手动取消勾选后确认按钮应变灰
 *   - 重新勾选后确认按钮应重新可用
 *
 * DOM 结构：
 *   <label>
 *     <span class="Checkbox_..."> <input type="checkbox" hidden> </span>
 *     我已阅读并同意 <a>300 SPARTANS 风险披露</a>
 *   </label>
 * 直接 .click() checkbox 不生效，用 setChecked({ force: true }) 走语义化路径。
 */
import { test, expect, type Page } from '@playwright/test';

const BOT_ALIAS = 'Kakarotto';

async function openSubscribeDialog(page: Page) {
  await page.goto(`/zh-cn/spartan-bot/${BOT_ALIAS}`);
  await page.getByRole('button', { name: '订阅' }).nth(1).click();
  await page.getByRole('spinbutton', { name: '请输入金额' }).fill('1');
}

async function setRisk(page: Page, checked: boolean) {
  await page
    .getByRole('dialog')
    .getByRole('checkbox')
    .first()
    .setChecked(checked, { force: true });
}

test.describe('订阅风险披露', () => {
  test('弹窗打开时风险披露默认已勾', async ({ page }) => {
    await openSubscribeDialog(page);
    const risk = page.getByRole('dialog').getByRole('checkbox').first();
    await expect(risk).toBeChecked();
  });

  test('取消勾选风险披露后，"确认"按钮应禁用', async ({ page }) => {
    await openSubscribeDialog(page);

    const confirm = page.getByRole('button', { name: '确认' });
    await expect(confirm).toBeEnabled();

    await setRisk(page, false);
    await expect(confirm).toBeDisabled();
  });

  test('取消勾选后重新勾选，"确认"按钮应恢复可用', async ({ page }) => {
    await openSubscribeDialog(page);

    const confirm = page.getByRole('button', { name: '确认' });
    const risk = page.getByRole('dialog').getByRole('checkbox').first();

    await setRisk(page, false);
    await expect(confirm).toBeDisabled();

    await setRisk(page, true);
    await expect(risk).toBeChecked();
    await expect(confirm).toBeEnabled();
  });
});
