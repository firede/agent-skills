---
name: kimi-tools
description: "通过 Python 脚本调用 kimi search 和 kimi fetch，用于网页搜索与页面抓取任务，返回结构化数据与 Markdown 内容。"
compatibility: "需要 Kimi Code 订阅(KIMI_CODE_API_KEY)、Python 3.9+，网络访问权限。"
---

# Kimi API Tools

## 前置条件

- 需要可用的 Kimi Code 订阅，并设置为环境变量：`KIMI_CODE_API_KEY`
- 需要 Python 3.9 或更高版本，视环境采用 `python3` 或 `python` 命令
- 需要网络可访问权限

## 快速开始

1. 设置 API Key：`export KIMI_CODE_API_KEY=...`
2. 先用 `kimi_search.py` 做关键词检索。
3. 再用 `kimi_fetch.py` 按 URL 抓取正文。

## 脚本说明

### `scripts/kimi_search.py`

调用 `POST /search`。

```bash
python ./scripts/kimi_search.py \
  --query "短剧创作指南" \
  --limit 5 \
  --timeout-seconds 30
```

参数：

- `--query` -> 搜索关键词（必填）
- `--limit` -> 返回结果数量（1-20，默认 5）
- `--include-content` -> 是否启用页面抓取（默认 false）
- `--timeout-seconds` -> 超时时间（默认 30 秒）

### `scripts/kimi_fetch.py`

调用 `POST /fetch`。

```bash
python ./scripts/kimi_fetch.py \
  --url "https://example.com" \
  --timeout-seconds 30
```

参数：

- `--url` -> 目标 URL（必填）
- `--timeout-seconds` -> 超时时间（默认 30 秒）

## 逃生通道

若环境中没有 `KIMI_CODE_API_KEY`，可通过 `--api-key` 参数传入，但非常不建议在命令行中暴露敏感信息。

## Agent 使用约定

- 按需开启 `--include-content` 与 `--limit`，以控制 token 成本。
