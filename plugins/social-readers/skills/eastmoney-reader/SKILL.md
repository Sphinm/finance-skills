---
name: eastmoney-reader
description: >
  Read Eastmoney (东方财富) for A-share research: stock news, reports, fund flow, dragon-tiger list,
  sector quotes, hot stocks via opencli. Triggers: 东财, 东方财富, eastmoney, 东财新闻,
  东财研报, 东财资金流, 东财龙虎榜, 东财热点, fetch Eastmoney.
  Prefer this over opencli-reader when source is explicitly Eastmoney.
---

# Eastmoney Reader — 东方财富

通过 [opencli](https://github.com/jackwener/opencli) 只读访问东财数据。

## Step 1: Ensure opencli

```bash
npm install -g @jackwener/opencli
opencli doctor
```

## Step 2: Execute

读 `references/commands.md`，用 `opencli eastmoney <command> --help` 确认参数后执行。

## Step 3: Fallback

opencli 不可用时，激活 `quote-data` / `signal-data` / `news-announce` 直连 HTTP API。

## Reference Files

- `references/commands.md` — 常用东财命令表
