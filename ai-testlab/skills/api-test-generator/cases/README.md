# api-test-generator / cases

**已解决过的真实案例**归档。记录：AI 生成的原始 pytest 文件 → 人工修改后的终版 → 修改原因。

同类目录说明见 `../../testcase-generator/cases/README.md`。

## 什么时候写一个 case

**api-test-generator 触发条件**：

- AI 生成用了 raw `requests.post` 而没有用业务 client
- 错误断言只用 HTTP 状态码而没检查业务 `code` / `msg`
- 副作用接口没打 `@pytest.mark.e2e` 就混进 smoke
- 硬编码金额 / UID / bot ID 没抽环境变量
- 断言只判字段存在（`assert "xx" in data`）不判值
- 新接口没同步补 `client.py`，测试代码里直接调 `http.post`
- 业务错误 msg 与实际不一致（例如 AI 写 `amount_invalid` 但实际是 `amount_not_allowed`）

不写：变量名调整、注释增删。

## 结构

沿用 testcase-generator 案例的三段式：**Input** + **AI First Draft** + **Final Version**，加一段 **学习点**（提炼可复用的判断规则）。

## api-test-generator 案例的特有关注

写案例时着重记录：

1. **业务错误码词表**——AI 猜的 msg 字符串 vs 实际 msg，逐个校对补进 prompt
2. **client.py 增量补丁模式**——新接口如何优雅新增到已有 client class
3. **E2E 顺序依赖**——测试方法顺序依赖 pytest 收集顺序，命名如何保证正确
4. **环境变量抽离粒度**——哪些常量必须抽（真实 UID），哪些可以留字面值（分页 limit=5）

## 参考实现

尚无案例。**手写标杆**：[`projects/spartans/tests/api/test_spartans_api.py`](../../../../projects/spartans/tests/api/test_spartans_api.py) — AI 生成的目标应对齐此风格。

## 首个案例候选时机

- 下次让 AI 生成新接口（如开放平台申请、白名单管理）测试文件时留档
- 或对现有 `test_spartans_api.py` 做 prompt 回归实验：让 AI 用 `bot_summary` 的接口描述生成，对比与手写终版差距，落成首个案例
