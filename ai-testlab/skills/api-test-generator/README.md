# api-test-generator

根据接口定义（OpenAPI / Markdown / 自然语言描述）生成符合本仓库风格的 **pytest 接口用例**。

## 输入

支持任一种或组合：

- OpenAPI / Swagger 规范（`.json` / `.yaml` 片段）
- Markdown 接口描述（路径、方法、参数、返回结构）
- 自然语言描述 + 一个成功响应样本
- 已存在的业务 client 方法列表

## 输出

- `test_{业务}_{模块}.py` 落到 `projects/<业务>/tests/api/`
- 若需新接口 → **同时**给出 `projects/<业务>/tests/api/client.py` 的补丁

## 使用

```
输入：斯巴达开放平台申请接口的 curl 样本 + 一个成功返回 JSON
调用 api-test-generator
输出：
  - test_spartans_openplatform.py（含 smoke / error branches / e2e 三段）
  - client.py 补丁（新增 apply_openplatform 方法）
```

## 覆盖要求

每个接口至少：

- 1 条 happy path（含关键字段值断言）
- 1 条分页/过滤边界（若接口支持）
- 每个业务参数的异常值（`amount=0`、金额过大、无效 ID）
- 权限失败（无 auth → HTTP 401）
- 副作用接口打 `@pytest.mark.e2e` + `@pytest.mark.slow`

**不覆盖**：并发/幂等 → 归 perf/；mock 层 → 不属于本 skill。

## 关键约定

生成的代码必须遵循 [`prompt.md`](prompt.md) 中的 **OBE 接口约定**：

- 成功判定看业务 `code`，不看 HTTP status
- 业务错误用 `exc.value.msg` 断言
- HTTP 层错误（401/403）用 `exc.value.code`
- 复用 `automation/clients/obe_http.py` + 业务 `client.py`

## 参考实现

[`projects/spartans/tests/api/test_spartans_api.py`](../../../../projects/spartans/tests/api/test_spartans_api.py) —— 手写的风格标杆。AI 生成结果应视觉上与此接近。

## 结构

- [`prompt.md`](prompt.md) — 主 prompt（约定 + 覆盖要求 + 自检清单）
- [`cases/`](cases/) — 历史修正案例（当前空，等首次真实生成）
- `examples/` — 待补，示例输入输出对照
