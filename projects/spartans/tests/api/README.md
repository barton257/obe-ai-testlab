# tests/api/

斯巴达接口用例。

## 技术选型

- 主：pytest + httpx（Python 3.11+）
- 辅：`.http` 文件（VSCode REST Client / IntelliJ HTTP Client），用于手工探索

## 运行

```bash
# 项目根目录
cp shared/secrets/obe-api.example.env .env.local  # 首次
uv sync                                            # 或 pip install -r requirements.txt
pytest projects/spartans/tests/api/ -v
```

## 编写要求

- 每个测试文件头部注释对应 YAML 用例路径
- 使用 `automation/clients/` 的通用客户端，不重复实现认证
- 断言错误码 + 错误信息，不只断状态码
- 涉及资金操作的用例必须清理（回滚订阅、取消赎回）

## 占位样例

- [`test_subscribe_example.py`](test_subscribe_example.py) — 骨架示例，需要接入真实 OpenAPI 后补全
