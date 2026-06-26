# Thread Stock

A-share / HK / ADR thematic stock selection assistant — four-layer funnel (supply chain → earnings → valuation → flow), 9 pitfalls, and case studies.

## Triggers

- A股选股、板块分析、资金流向、主线判断
- AI算力链、供应链拆解、PEG筛选、量价分析
- 港股互联网、中概股、ETF仓位

## Setup

1. Install the skill (see repo root README).
2. Optional: install [a-stock-data](https://github.com/simonlin1212/a-stock-data) for richer A-share market data.
3. Run scripts from this directory:

```bash
cd plugins/thread-stock/skills/thread-stock
uv run --with yfinance --with akshare --with requests python3 scripts/fund_flow_collector.py
uv run --with yfinance --with akshare python3 scripts/weekly_scan.py
```

Local SQLite database is created at `data/fund_flow.db` (gitignored).

## Reference Files

| Path | Description |
|------|-------------|
| `references/selection-framework.md` | Four-layer funnel methodology |
| `references/supply-chain-map.md` | Industry supply chain map |
| `references/volume-price-signals.md` | Volume-price entry signals |
| `references/pitfalls/README.md` | Pitfall index |
| `references/ticker/README.md` | Case study index |
