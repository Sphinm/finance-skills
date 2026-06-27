---
name: volume-price
description: >
  A-share volume-price patterns: shrinking volume new highs, MA pullback entries, sector联动,
  dangerous signals (high-turnover limit-up, volume spike with long upper shadow, distribution top).
  Triggers: 量价分析, 缩量上涨, 放量突破, 回踩均线, 入场时机, 技术形态,
  换手率, 量价背离, 涨停换手, 长上影, volume price A-share.
---

# Volume-Price — A股量价信号

## Step 1: Load Signal Library

读 `references/signals.md` — 完整量价信号库（健康趋势 4 种 + 危险信号 6 种 + A 股特有限涨跌停规则）。

## Step 2: Data Collection

| 数据 | 来源 |
|------|------|
| K线 + 换手 | `quote-data` mootdx bars + 腾讯 turnover_pct |
| 板块联动 | `signal-data` 热点 + 行业排名 |
| 龙虎榜 | `signal-data` §3.5（确认主力方向） |

## Step 3: Entry Decision Tree

```
缩量新高 + 板块净流入 → 持有/回踩5MA加仓
缩量回踩10日线 + 板块未退潮 → 买入
放量突破平台 + 板块联动3+ → 突破日进1/3仓
高换手涨停(>15%) → 不追
天量长上影 → 减仓
```

## Step 4: Regime Context

结合 thread-stock Structure-to-Regime 表：
- 主线明确 + 缩量上行 → 最佳入场环境
- 板块轮动 + 缩量 → 减仓观望

## Step 5: Output

给出具体：入场价区间、止损位（跌破10日线放量）、目标位、仓位比例。

## Reference Files

- `references/signals.md` — 量价信号完整库（含案例）
