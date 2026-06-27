---
name: earnings-recap
description: >
  Post-earnings analysis for A-shares: EPS surprise vs Tonghuashun consensus, revenue/profit YoY,
  5-day price reaction via mootdx, beat/miss verdict with volume-price interpretation.
  Triggers: 财报复盘, 业绩解读, 季报解读, beat miss, 超预期, 不及预期,
  财报后分析, 业绩快报解读, earnings recap A-share, 财报出了怎么样.
---

# Earnings Recap — A股财报复盘

财报发布后生成 surprise 分析 + 量价反应解读。执行 `references/workflow.md` 中的 `earnings_recap(code)`。

## Step 1: Run Recap Script

```bash
pip install mootdx requests pandas
```

读并执行 `references/workflow.md` § `earnings_recap()`。

## Step 2: Surprise Classification

| surprise_pct | verdict |
|--------------|---------|
| > +5% | beat |
| -5% ~ +5% | inline |
| < -5% | miss |

## Step 3: Price Reaction Matrix

| 财报 | 5日涨跌 | 量价形态 | 操作 |
|------|---------|----------|------|
| beat | 涨 + 缩量 | 健康 | 持有 |
| beat | 涨 + 放量滞涨 | 利好出尽 | 减仓 |
| miss | 跌 + 缩量 | 观望 | 等企稳 |
| miss | 跌 + 放量 | 逻辑破坏 | 清仓 |

配合 `volume-price` skill 确认形态。

## Step 4: Output

按 workflow.md 模板输出，更新 bull/base/bear 情景和止损位。

## Reference Files

- `references/workflow.md` — 完整 Python 脚本 + 输出模板 + 量价矩阵
