# scripts/

本地一次性小工具，不属于测试主流程。

## 典型内容

- 数据导出 / 转换
- 用例批量重命名
- XMind → Markdown 转换
- 迁移脚本（一次性）

## 与 automation/ 的区别

- `automation/` — 测试运行时依赖的**框架代码**
- `scripts/` — 手工触发的**辅助工具**

## 命名

- Shell：`{动词}-{对象}.sh`（例：`export-testcases.sh`）
- Python：`{动词}_{对象}.py`

## 保留期

三个月未使用可以删除。
