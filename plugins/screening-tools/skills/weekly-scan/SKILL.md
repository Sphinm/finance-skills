---
name: weekly-scan
description: >
  Run A-share weekly stock screening: sector fund flow ranking + stock pool scan,
  outputs short/mid/long-term candidates. Triggers: 帮我选票, 有什么可以买的,
  周度扫描, 持仓检查, 板块资金哪个在流入, 短线候选, 长线候选, weekly scan A-share.
---

# Weekly Scan — A股周度选股扫描

**选股时必须先运行脚本**，禁止凭印象手动列候选。

## Step 1: Collect Fresh Data

先运行 `fund-flow-collector` 采集当日板块快照（若今日未采集）：

```bash
cd plugins/screening-tools/skills/fund-flow-collector
uv run --with yfinance --with akshare --with requests python3 scripts/fund_flow_collector.py
```

## Step 2: Run Scan

```bash
cd plugins/screening-tools/skills/weekly-scan
# 完整扫描
uv run --with yfinance --with akshare python3 scripts/weekly_scan.py
# 带持仓检查
uv run --with yfinance --with akshare python3 scripts/weekly_scan.py --holdings 600487,002463
# 仅板块资金
uv run --with yfinance --with akshare python3 scripts/weekly_scan.py --sector-only
```

## Step 3: Interpret Output

加载 thread-stock 参考文件：
- 完整选股流程 → `../../market-analysis/skills/thread-stock/references/screening-workflow.md`
- 持仓检查 → `weekly-checklist.md`
- 短/中长线策略 → `strategy-by-horizon.md`

## Step 4: Apply Funnel

脚本输出三层候选后，用 `thread-stock` 四层漏斗过滤（供应链→财报→PEG→资金）。

## Database

`fund-flow-collector` 写入 `plugins/screening-tools/data/fund_flow.db`（gitignored），`weekly_scan.py` 自动读取。
