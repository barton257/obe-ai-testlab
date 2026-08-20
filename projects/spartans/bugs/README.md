# bugs/

斯巴达缺陷记录。一 bug 一文件，便于版本追踪和 AI 检索。

## 命名

`YYYY-MM-DD-spartans-{S1|S2|S3|S4}-{简述}.md`

严重级别：

- **S1** 阻塞主流程 / 资金安全 / 数据错误
- **S2** 核心功能异常，有绕过路径
- **S3** 次要功能异常或体验问题
- **S4** 优化建议

## 结构

见根 `../../AGENTS.md` 第五节。

## 状态流转

新建 → 已确认 → 修复中 → 待验证 → 已关闭 / 已延期

状态变更用 commit 追加更新，不删旧内容。

## 当前缺陷台账（复验于 2026-08-18）

三条均为 2026-08-17 提出，2026-08-18 用 Testnet 实调复验：**全部仍存在，无一修复**。

| 缺陷 | 级别 | 复验状态 | 回归用例（xfail strict） |
|---|---|---|---|
| [订阅金额小于最小值未拦截](2026-08-17-spartans-S2-订阅金额小于最小值未拦截.md) | S2 | 仍存在，**新发现极小额度产生永久卡单** | `test_purchase_below_min_rejected` |
| [赎回金额超权益静默截断](2026-08-17-spartans-S2-赎回金额超权益静默截断.md) | S2 | 仍存在，**修复成本比原判断低** | `test_redeem_exceeds_equity_rejected` |
| [userId 与 JWT 不匹配未拦截](2026-08-17-spartans-S3-userId与JWT不匹配未拦截.md) | S3 | 仍存在，归属已二次确认不越权 | `test_purchase_wrong_user_id_rejected` |

### 共同根因

三条同属 **"入参越界/非法后静默处理，而非显式拒绝"**：

- S2-A：`min_subscribe` 配置在 purchase 路径上未被读取，拦截边界实际是 `amount > 0`（`1e-08` 可穿透）；
  且 `1e-08` 那笔在批次里卡成 `Locked`/`units=0`，永久悬挂 —— 需后端清理 `#1838`
- S2-B：权益校验存在但只拦下界，超权益时用 `min()` 钳制而非报错
- S3：`body.userId` 与 JWT 不一致时静默忽略前者

**建议一并修复**，并在 invest 模块确立编码约定：入参落在业务允许区间外一律返回
`code=1` 加具体 msg，不做静默钳制。否则同类问题会在 cancel、分润等接口重复出现。

### 回归机制

三条回归用例均用 `@pytest.mark.xfail(strict=True)`，后端修复后会转 **XPASS 失败**，
强制回来摘标记 —— 避免缺陷修好后回归用例长期躺在 xfail 里无人过问。

用例同时标了 `writes_funds`（会真实动账），默认不跑；显式启用：

```bash
pytest projects/spartans/tests/api/test_spartans_api.py -m writes_funds -v
```
