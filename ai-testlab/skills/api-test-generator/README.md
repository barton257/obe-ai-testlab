# api-test-generator

根据 OpenAPI / 接口文档生成 pytest 接口用例。

## 输入

- OpenAPI/Swagger 规范文件
- 目标接口列表（可选，默认全量）
- 认证方式描述

## 输出

- pytest 文件到 `projects/<x>/tests/api/`
- 使用 `automation/clients/` 已有的通用客户端，不重复造轮子

## 使用

```
输入：斯巴达订阅接口 OpenAPI 片段
调用 api-test-generator
输出：test_spartans_subscribe.py（含 happy path + 参数校验 + 权限失败）
```

## 覆盖要求

每个接口至少生成：

- 1 条 happy path
- 每个参数的边界/异常值
- 权限失败（未登录、越权）
- 幂等/并发（如适用）

## 待补充

- `prompt.md`
- `examples/`
