# projects/

业务模块目录。每个子目录代表一个 OneBullEx 业务线，内部结构统一。

## 子目录约定

每个业务下必须包含：

```
<业务>/
├── README.md            # 业务概述、走查环境、入口路径
├── docs/                # 需求解读、功能审计、走查报告
├── maps/                # 思维导图（.xmind + .mm 双份，便于协作）
├── testcases/           # 结构化用例（YAML/MD）
├── bugs/                # 缺陷记录（一 bug 一文件）
├── roadmap/             # 迭代/版本计划
├── bots/                # 该业务专用的测试人格 prompt
└── tests/               # 可执行测试
    ├── api/             # 接口用例
    ├── e2e/             # UI 端到端
    ├── perf/            # 压测
    └── fixtures/        # 静态测试数据（脱敏）
```

## 已有业务

- **[spartans/](spartans/)** — 300 SPARTANS 策略机器人平台

## 新增业务

复制 `spartans/` 结构，替换业务名，更新根 `README.md` 的业务列表。详见 `../AGENTS.md` 第九节。
