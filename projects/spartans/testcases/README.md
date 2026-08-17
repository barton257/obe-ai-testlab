# testcases/

结构化测试用例（YAML）。用于人工/AI 共同维护、可 diff、可 grep、可作为自动化测试的输入。

## 文件命名

`{业务}-{模块}-{P0|P1|P2|P3}-{正常|异常|边界}-{简述}.yaml`

例：
- `spartans-subscribe-P0-正常-最小订阅金额.yaml`
- `spartans-redeem-P1-异常-流动性不足排队.yaml`

## YAML 骨架

见根 `../../AGENTS.md` 第四节。

## 与 maps/ 的关系

`maps/` 里的用例分支定稿后同步过来。同步顺序：脑图演绎 → YAML 落地 → 转换为自动化脚本（`tests/api|e2e/`）。

## AI 生成流程

1. 输入：`docs/SPARTANS_FEATURE_AUDIT.md` + `maps/*.mm`
2. 调用：`ai-testlab/skills/testcase-generator/`
3. 输出：本目录 `.yaml`
4. 人工审核：QA 补 `reviewed_by` 字段后 commit
