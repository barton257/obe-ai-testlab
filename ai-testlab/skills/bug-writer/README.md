# bug-writer

把现场描述（口述/截图 OCR/日志片段）整理成标准化缺陷报告。

## 输入

- 现象描述、复现步骤、环境信息
- 相关附件（截图、日志、HAR）

## 输出

- Markdown 文件，落到 `projects/<x>/bugs/`
- 命名和结构遵循 `../../../AGENTS.md` 第三/五节

## 使用

```
现象：斯巴达详情页点击赎回按钮无响应
环境：Testnet Web Chrome 128
现有日志：<粘贴>
调用 bug-writer → 输出到 projects/spartans/bugs/
```

## 特别注意

- 敏感字段（UID、订单号、真实金额）在生成前脱敏
- 严重级别由 AI 建议 + 人工确认，不能 AI 说了算

## 待补充

- `prompt.md`
- `examples/`
