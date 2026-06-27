---
name: etf-premium-cn
description: >
  Calculate A-share on-exchange ETF premium/discount vs IOPV (Eastmoney reference NAV),
  batch compare theme ETFs (semiconductor, photovoltaics, ChiNext).
  Triggers: ETF溢价, ETF折价, IOPV, 基金溢价率, 510300溢价, 半导体ETF溢价,
  场内ETF估值, ETF套利, premium discount A-share ETF.
---

# ETF Premium CN — A股ETF溢价率

## Step 1: Single ETF

执行 `references/api.md` § `etf_premium(code)`。

## Step 2: Theme Comparison

批量对比同主题 ETF 溢价率，找情绪最热的品种：

```python
etf_premium_batch(["512480", "512760", "588000"])
```

## Step 3: Interpret

| premium_pct | 操作含义 |
|-------------|----------|
| > 2% | 情绪过热，不追 |
| 0.5-2% | 偏热，轻仓 |
| ±0.1% | 正常 |
| < -0.5% | 折价机会或流动性问题，查成交额 |

## Step 4: Cross with Sector

ETF 溢价极端时，查 `signal-data` 板块排名验证是否 whole-sector 狂热。

## Reference Files

- `references/api.md` — IOPV 拉取 + 溢价计算 + 主题 ETF 对比
