# reporters/

测试报告生成与上传。包括 **报告格式转换**（pytest/Playwright 原始输出 → HTML/Allure）
与 **通知推送**（失败时发 Slack/企微）。

---

## 当前状态

**未配置任何自定义报告。** 当前使用框架默认输出：

- **pytest** — 终端彩色输出 + `-v` 详细模式
- **Playwright** — `npx playwright show-report` HTML 报告（本地生成，未上传）

---

## 报告类型

### 1. 终端输出（已有）

**pytest**：
```bash
pytest projects/spartans/tests/api/ -v
# ✅ 实时看到每条用例通过/失败
# ✅ 失败时自动打印 traceback
```

**Playwright**：
```bash
npx playwright test --reporter=list
# ✅ 逐行显示用例执行进度
```

**优点**：零配置，本地调试友好。
**缺点**：CI 日志刷屏，无法归档，无截图/视频。

### 2. HTML 报告（Playwright 已有 / pytest 待补）

**Playwright**（已配置）：
```bash
npx playwright test --reporter=html
npx playwright show-report  # 打开浏览器查看
```

生成位置：`playwright-report/index.html`（.gitignore 已排除）。

**pytest**（待补充）：
```bash
pip install pytest-html
pytest --html=report.html --self-contained-html
```

**适用场景**：本地调试、给 PM 演示失败用例。

### 3. Allure 报告（推荐，待接入）

**优势**：
- 支持 pytest + Playwright 双端
- 历史趋势图（成功率曲线、用例耗时变化）
- 失败用例自动分组（同一个 bug 导致的批量失败）
- 可集成 Jenkins / GitLab CI

**安装**：
```bash
# Python
pip install allure-pytest
pytest --alluredir=allure-results

# Playwright
npm install -D allure-playwright
# 在 playwright.config.ts 中添加 reporter: 'allure-playwright'

# 生成报告
allure generate allure-results -o allure-report
allure open allure-report
```

**何时接入**：
- CI 流水线搭建完成后
- 用例总数 > 50 条（当前 API 5 条 + E2E 18 条 = 23 条，暂不急）

### 4. 自定义 JSON（待补充）

若需对接内部测试平台（如飞书/Jira 自动建单），导出结构化数据：

```bash
pytest --json-report --json-report-file=report.json
```

输出包含：
- 每条用例的状态、耗时、错误堆栈
- 可编程解析，自动提缺陷单

---

## 通知推送

### 失败告警

**触发时机**：
- CI 中任一用例失败
- 压测性能指标不达标

**通知渠道**（待确认）：
- Slack / 企微 / 飞书？
- 通知到哪个群？@谁？

**示例脚本**（CI 中调用）：
```bash
# automation/reporters/notify.sh
#!/bin/bash
RESULT=$1  # passed / failed
if [ "$RESULT" = "failed" ]; then
  curl -X POST https://hooks.slack.com/... \
    -d '{"text": "❌ Spartans API 测试失败，查看报告: <CI_REPORT_URL>"}'
fi
```

### 定时汇总（可选）

每日早 9 点自动发送：
- 昨日用例通过率
- 新增失败用例
- 性能指标对比（P95 响应时间趋势）

---

## 截图与视频

**Playwright 已自动配置**（`playwright.config.ts`）：
- **截图** — 失败时自动截图，存 `test-results/`
- **视频** — 默认关闭（开启会拖慢执行）

若需开启视频录制：
```typescript
// playwright.config.ts
use: {
  video: 'retain-on-failure',  // 仅失败用例保留视频
}
```

**存储与清理**：
- 本地：手动清理 `test-results/`
- CI：上传到 artifact 或 S3，保留 7 天

---

## 文件结构（待补充）

```
reporters/
  allure-config.json       # Allure 配置（失败重试次数、分类规则）
  notify.sh                # Slack/企微推送脚本
  html-to-slack.py         # 将 HTML 报告转成 Slack 消息卡片
  pytest-json-parser.py    # 解析 pytest JSON 输出，提取失败用例
  README.md                # 本文件
```

---

## 相关

- CI 配置：[`../ci/README.md`](../ci/README.md)
- Playwright 配置：[`../../projects/spartans/tests/e2e/playwright.config.ts`](../../projects/spartans/tests/e2e/playwright.config.ts)
- Allure 官方文档：[https://docs.qameta.io/allure/](https://docs.qameta.io/allure/)
