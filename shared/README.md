# shared/

跨业务、跨测试类型的共享资源。

## 目录

| 目录/文件 | 内容 |
|---|---|
| [`glossary.md`](glossary.md) | OBE / 合约 / 斯巴达等业务术语的统一定义 |
| [`env/`](env/) | 环境定义（testnet / staging / prod URL、账号约定） |
| [`secrets/`](secrets/) | 只放 `*.example.env`。真值走本地 `.env.local`（已 gitignore） |
| [`conventions/`](conventions/) | 用例命名、优先级、缺陷分级、commit message 规则 |

## 修改规则

`shared/` 下的内容影响所有业务和工具，改动需要人工发起（AI 不能直接改，见 `../AGENTS.md` 第六节）。
