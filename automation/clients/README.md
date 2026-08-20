# clients/

OBE 通用 API 客户端。**只放业务无关的 HTTP 底座**：session 管理、header 注入、
业务错误码转异常、重试策略。

## 已有

| 文件 | 内容 |
|---|---|
| [`obe_http.py`](obe_http.py) | `ObeClient`（session + header + 重试）、`ObeApiError`（`code != 0` 转异常） |

## 边界

| 放这里 | 放 `projects/<业务>/tests/api/client.py` |
|---|---|
| `authorization` / `identify` / `platform` header 拼装 | `/botapi/v1/invest/purchase` 端点封装 |
| `code != 0` → `ObeApiError` | `amount` / `settleAmount` 参数名 |
| 重试、超时、连接池 | bot 状态机、Tier 参数 |

判断口诀：**出现 `spartans`、`bot`、`invest` 等业务字眼 → 不属于这里。**

## 用法

```python
from automation.clients.obe_http import ObeClient, ObeApiError

client = ObeClient.from_env()          # 读 SPARTANS_API_BASE / AUTH_TOKEN / AUTH_IDENTIFY
try:
    client.post("/botapi/v1/invest/user/summary", {})
except ObeApiError as e:
    print(e.code, e.msg, e.path)
```

业务层在此之上再封一层，见 `projects/spartans/tests/api/client.py`。

## 重试策略（改动前必读）

`obe_http.py` 的 `Retry` **只重试 connect 阶段**，`read=0` / `status=0` 是刻意的：

- connect 失败 ⇒ 请求没到服务端 ⇒ 重试安全
- read 超时 ⇒ 请求可能已执行 ⇒ 重试 `POST /invest/purchase` 会**重复扣款**

放开 `read` / `status` 重试等于给资金接口加了重复提交风险。要改先想清楚幂等性。

## 版本策略

本目录的接口被多业务引用，破坏性变更需在 PR 里列出所有引用点并一起改。
新增可选参数优先，不要改已有参数的语义。
