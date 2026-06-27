---
name: a-share-liquidity
description: >
  A-share liquidity analysis: turnover, daily amount, bid-ask spread via mootdx order book,
  distance to limit up/down, impact cost estimate, limit-up liquidity tiers.
  Triggers: 流动性, 换手率, 成交额, 盘口价差, 冲击成本, 涨跌停,
  封单, 能不能买进, 能不能卖出, 流动性分析 A-share, 小盘股流动性.
---

# A-Share Liquidity — A股流动性分析

## Step 1: Snapshot

执行 `references/api.md` § `liquidity_snapshot(code)`。

## Step 2: Interpret Tiers

| liquidity_tier | 日成交额 | 建议 |
|----------------|----------|------|
| 高流动性 | > 10亿 | 正常仓位 |
| 中等 | 3-10亿 | 分批建仓 |
| 低流动性 | < 3亿 | 卫星仓，避免大单 |

## Step 3: Limit-Up/Down Context

A 股涨跌停制度下，距涨停距离 < 3% 且换手已高 → 追高风险极大。
读 `references/api.md` § 涨跌停流动性表。

## Step 4: Impact Check

大单前运行 `impact_estimate(code)` 评估冲击成本。

## Reference Files

- `references/api.md` — 流动性快照 / 冲击成本 / 涨跌停规则
