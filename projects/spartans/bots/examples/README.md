# bots/examples/

三个测试人格针对**同一功能（订阅流程）**的走查产出示例。对照阅读可以直观感受三视角的关注差异。

## 示例文件

| 文件 | 人格 | 发现问题数 | 最高级别 |
|---|---|---|---|
| [`Kakarotto-subscribe-walkthrough.md`](Kakarotto-subscribe-walkthrough.md) | 新手订阅者 | 7 条 | S2 |
| [`Vegeta-subscribe-walkthrough.md`](Vegeta-subscribe-walkthrough.md) | 激进短线玩家 | 7 条 | S1 |
| [`Frieza-subscribe-walkthrough.md`](Frieza-subscribe-walkthrough.md) | 机构/KOL 创建者 | 6 条 | S1 |

## 三视角关注点对比

| 维度 | Kakarotto | Vegeta | Frieza |
|---|---|---|---|
| **核心问题类型** | 文案/引导/反馈 | 数据一致性/边界/并发 | 规则披露/合规/计算 |
| **最易发现** | 新手认知落差 | 技术型 bug | 制度漏洞 |
| **容易忽略** | 数据准确性 | 用户引导体验 | 前端交互细节 |
| **S1 风险点** | 几乎不触及 | 并发/幂等问题 | 分润计算错误 |

## 如何使用示例

1. **格式参考**：AI 生成走查产出时以这三份为格式模板
2. **内容对比**：同一功能让三个人格各走一遍，覆盖盲区
3. **生成用例**：把产出里的"问题"交给 `ai-testlab/skills/testcase-generator/` 转化为 YAML 用例
