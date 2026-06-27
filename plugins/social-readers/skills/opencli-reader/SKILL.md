---
name: opencli-reader
description: >
  Generic read-only opencli fallback for A-share sources without a dedicated reader —
  Sina Finance, Tonghuashun, Weibo, Zhihu, and other China finance sites.
  Triggers: opencli读, 用opencli抓, 新浪财经, 微博财经, 知乎股票,
  sinafinance, weibo finance, any China finance site opencli covers without dedicated skill.
  FALLBACK — prefer eastmoney-reader, xueqiu-reader, cls-reader when source matches.
---

# OpenCLI Reader — A股通用只读

当请求无法由 `eastmoney-reader` / `xueqiu-reader` / `cls-reader` 覆盖时使用。

## Step 1: Check Dedicated Skills First

| 源 | 用 |
|----|-----|
| 东财 | eastmoney-reader |
| 雪球 | xueqiu-reader |
| 财联社 | cls-reader |
| 其他 | 本 skill |

## Step 2: Ensure opencli

```bash
npm install -g @jackwener/opencli
opencli doctor
```

## Step 3: Discover & Execute

```bash
opencli list | grep -i <keyword>
opencli <site> <command> --help
```

读 `references/cn-sources.md` 中国区站点速查表。

## Step 4: HTTP Fallback

opencli 不可用时 → `data-providers` 直连 skills。

## Reference Files

- `references/cn-sources.md` — 中国区 opencli 站点 + fallback 链
