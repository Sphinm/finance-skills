---
name: fund-flow-collector
description: >
  Collect A-share sector fund flow snapshots into local SQLite for historical trend analysis.
  Triggers: 采集板块资金, 板块资金历史, 资金流向数据库, fund flow collector,
  导出板块资金CSV, 查询板块资金近30天, sector fund flow history A-share.
---

# Fund Flow Collector — 板块资金采集

每日快照存本地 SQLite，弥补东财历史接口不可用问题。

## Step 1: Run Collection

```bash
cd plugins/screening-tools/skills/fund-flow-collector
uv run --with yfinance --with akshare --with requests python3 scripts/fund_flow_collector.py
```

## Step 2: Query History

```bash
# 查询板块近 30 天
uv run --with yfinance --with akshare --with requests python3 scripts/fund_flow_collector.py --query 半导体 --days 30
# 导出 CSV
uv run --with yfinance --with akshare --with requests python3 scripts/fund_flow_collector.py --export csv
# 统计
uv run --with yfinance --with akshare --with requests python3 scripts/fund_flow_collector.py --stats
```

## Step 3: When to Run

- 用户每次让 AI 选票/看盘时，先跑 collector 再跑 `weekly-scan`
- 不需要 cron — 聊天时顺手采集即可
- 板块资金流无法回填历史，个股行情可回填近 30 天

## Database

位置：`plugins/screening-tools/data/fund_flow.db`（gitignored，两脚本共享）

## Data Sources

| 优先级 | 源 | 用途 |
|--------|-----|------|
| 1 | akshare `stock_fund_flow_industry/concept` | 行业/概念排行 |
| 2 | 新浪 `MoneyFlow.ssl_bkzj_bk` | 备用快照 |

## Related Skills

- 扫描 → `weekly-scan`
- 板块分析 → `sector-rotation`
