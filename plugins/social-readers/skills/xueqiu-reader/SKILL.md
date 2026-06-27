---
name: xueqiu-reader
description: >
  Read Xueqiu (雪球) for A-share social sentiment: stock discussions, hot topics, user posts, search.
  Triggers: 雪球, xueqiu, 雪球讨论, 雪球热度, 雪球大V, 雪球评论, pull Xueqiu feed.
  Prefer this over opencli-reader when source is Xueqiu.
---

# Xueqiu Reader — 雪球

## Step 1: Ensure opencli

```bash
npm install -g @jackwener/opencli
```

## Step 2: Execute

读 `references/commands.md`。Ticker 格式 `SH600519` / `SZ000001`。

## Step 3: Sentiment Analysis

讨论量 + 股价走势交叉验证，配合 `finance-sentiment-cn`。

## Reference Files

- `references/commands.md` — 雪球 opencli 命令 + 情绪解读
