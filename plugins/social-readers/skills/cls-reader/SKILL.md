---
name: cls-reader
description: >
  Read CLS (财联社) telegraph and news for A-share real-time market headlines and policy signals.
  Triggers: 财联社, CLS, 财联社快讯, 电报, 7x24, 政策利好, 财联社搜索,
  Cailianpress, real-time China finance news.
---

# CLS Reader — 财联社

## Step 1: Fetch Telegraph

执行 `references/api.md` § `cls_telegraph()` 拉最新快讯。

## Step 2: Keyword Search

用户关心特定题材时：`cls_search("半导体")`

## Step 3: Route to Stocks

快讯中出现公司名/政策 → 关联 `thread-stock` / `sector-rotation` 产业链标的。

## Step 4: opencli Fallback

```bash
opencli list | grep -i cls
```

## Reference Files

- `references/api.md` — 财联社 HTTP API + level 解读
