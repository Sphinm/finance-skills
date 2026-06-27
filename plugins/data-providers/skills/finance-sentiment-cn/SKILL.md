---
name: finance-sentiment-cn
description: >
  A-share market sentiment: theme heat index from Tonghuashun hot stocks, individual stock
  hot-list status, market greed/fear score. Triggers: 市场情绪, 情绪指数, 热度, 贪婪恐惧,
  题材热度, 今天市场热吗, 这只股票热吗, sentiment A-share, market mood China stocks.
---

# Finance Sentiment CN — A股市场情绪

## Step 1: Market-Wide Sentiment

执行 `references/api.md` § `market_sentiment_summary()`：

```python
# → score 0-100, label 贪婪/中性/恐惧, top_themes
```

## Step 2: Individual Stock

```python
stock_sentiment("688017")  # on_hot_list, reason, sentiment
```

## Step 3: Cross-Validate

| 信号 | 确认 |
|------|------|
| 情绪贪婪 + 板块净流出 | 背离，谨慎 |
| 情绪恐惧 + 龙头缩量不跌 | 可能底部 |
| 个股极热 + 龙虎榜机构卖出 | 分发信号 |

配合 `signal-data` + `xueqiu-reader`。

## Reference Files

- `references/api.md` — 情绪评分完整代码 + 解读表
