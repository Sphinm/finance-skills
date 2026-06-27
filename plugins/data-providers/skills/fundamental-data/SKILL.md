---
name: fundamental-data
description: >
  A-share fundamental data: mootdx quarterly financials (37 fields) and F10 company profile,
  Eastmoney stock info, Sina three financial statements (balance sheet/income/cash flow).
  Triggers: 财报, 财务数据, 利润表, 资产负债表, 现金流量表, ROE, EPS,
  季报, 年报, F10, 总股本, 流通股, 主营收入, 净利润, any A-share financial statement query.
---

# Fundamental Data — A股基础数据层

## Step 1: Prerequisites

```bash
pip install mootdx requests pandas
```

## Step 2: Match Request

| 用户需求 | 数据源 | 参考 |
|----------|--------|------|
| 季报快照 37 字段 | mootdx finance | `references/api.md` §6.1 |
| 公司资料 9 大类 | mootdx F10 | §6.2 |
| 行业/股本/市值/上市日 | 东财 push2 | §6.3 |
| 三表（资产负债/利润/现金流） | 新浪 | §6.4 |

## Step 3: Earnings Analysis

财报分析配合 `earnings-preview` / `earnings-recap`；估值配合 `valuation-cn`。

## Related Skills

- 公告全文 → `news-announce`
- 一致预期 → `research-data`
