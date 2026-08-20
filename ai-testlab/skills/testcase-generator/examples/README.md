# testcase-generator / examples

真实调用示例。每一份 input 对应实际落地的 YAML 用例，便于 prompt 迭代时做回归。

## 示例列表

### input-01：Vegeta 走查产出 → 4 条 YAML 用例

- **输入**：[`projects/spartans/bots/examples/Vegeta-subscribe-walkthrough.md`](../../../../projects/spartans/bots/examples/Vegeta-subscribe-walkthrough.md)
- **选中问题**：V1（切换周期未重置分页）、V2（跨页面数据不一致）、V3（前端最小金额未校验）、V5（并发订阅双扣）
- **输出**：
  - `projects/spartans/testcases/spartans-market-P0-异常-同周期收益率跨页面一致性.yaml`（V2）
  - `projects/spartans/testcases/spartans-subscribe-P0-异常-并发订阅双扣.yaml`（V5）
  - `projects/spartans/testcases/spartans-subscribe-P1-边界-最小金额前端校验.yaml`（V3）
  - `projects/spartans/testcases/spartans-market-P1-异常-切换周期未重置分页.yaml`（V1）

### 转化模式

| 走查问题特征 | 生成用例数 | 拆分逻辑 |
|---|---|---|
| 数据一致性（V2） | 1 条 P0 异常 | 需要跨页面/接口对比 |
| 并发/幂等（V5） | 1 条 P0 异常（含清理） | 涉及资金，必须 P0 |
| 前端校验缺失（V3） | 1 条 P1 边界（含 5 个 edge_cases） | 边界值场景多 |
| 交互 bug（V1） | 1 条 P1 异常 | 单场景可覆盖 |

### 待补充的转化示例

- Kakarotto 走查 → 用例（体验类问题如何转化为可验证用例）
- Frieza 走查 → 用例（规则/合规类问题需要制度层验证）
- 需求文档 → 用例（无走查记录时的生成模式）
