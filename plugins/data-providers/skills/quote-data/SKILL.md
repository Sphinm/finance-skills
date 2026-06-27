---
name: quote-data
description: >
  A-share real-time quotes and OHLCV: mootdx (K-line, order book, tick trades),
  Tencent Finance API (PE/PB/market cap/turnover/limit prices/index/ETF),
  Baidu Stock K-line with MA5/10/20. Triggers: A股行情, K线, 盘口, 五档,
  实时价格, 涨跌停, 指数行情, ETF行情, 沪深300, 创业板指, 换手率, 市值,
  mootdx, 腾讯财经, 百度K线, any request for A-share price or chart data.
---

# Quote Data — A股行情层

实时行情数据，不封 IP。读 `references/api.md` 获取完整调用代码。

## Step 1: Prerequisites

```bash
pip install mootdx requests pandas stockstats
```

读 `references/common.md` 获取市场前缀规则与 ticker 归一化。

## Step 2: Match Request

| 用户需求 | 数据源 | 参考 |
|----------|--------|------|
| K线/盘口/逐笔 | mootdx TCP | `references/api.md` §1.1 |
| PE/PB/市值/涨跌停/指数/ETF | 腾讯财经 | `references/api.md` §1.2 |
| K线+均线 MA5/10/20 | 百度股市通 | `references/api.md` §1.3 |

## Step 3: Execute

- mootdx **不提供** PE/PB/市值 — 估值字段走腾讯 API
- 批量查询优先腾讯 `tencent_quote(codes)`
- 指数代码：`000001` 上证、`000300` 沪深300、`399006` 创业板指

## Related Skills

- 估值计算 → `valuation-cn`
- 资金流向 → `fund-flow-data`
- 不确定用哪个 → `trading-data`（数据层子路由；全库入口见 `a-finance-skills`）
