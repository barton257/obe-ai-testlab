# walkthrough-recorder

把走查过程（口述、录屏字幕、截图批注）整理成结构化审计报告。

## 输入

- 走查笔记 / 录音转录 / 截图批注
- 目标业务和范围

## 输出

- Markdown 文件到 `projects/<x>/docs/{YYYYMMDD}_WALKTHROUGH.md`
- 若走查覆盖较全 → 更新对应的 `*_FEATURE_AUDIT.md`（人工确认后）

## 使用

```
输入走查录音字幕 + 截图目录
调用 walkthrough-recorder
输出：分节的走查报告（信息架构 → 订阅侧 → 创建者侧 → 异常态）
```

## 待补充

- `prompt.md`
- `examples/`
