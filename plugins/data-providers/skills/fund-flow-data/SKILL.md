---
name: fund-flow-data
description: >
  A-share fund flow and chip structure: margin trading (融资融券), block trades (大宗交易),
  shareholder count changes (股东户数), dividend history, 120-day daily fund flow (主力/大单).
  Triggers: 融资融券, 两融, 大宗交易, 股东户数, 筹码集中, 分红送转,
  主力资金, 120日资金流, 大单净流入, 筹码分析, any A-share capital flow or holder data.
---

# Fund Flow Data — A股资金面/筹码层

筹码与资金面数据，东财 datacenter + push2his。读 `references/api.md`。

## Step 1: Prerequisites

```bash
pip install requests pandas
```

读 `references/common.md` 获取 `eastmoney_datacenter()` 共用 helper。

## Step 2: Match Request

| 用户需求 | 端点 | 参考 |
|----------|------|------|
| 融资融券明细 | datacenter-web | `references/api.md` §4.1 |
| 大宗交易 | datacenter-web | §4.2 |
| 股东户数变化 | datacenter-web | §4.3 |
| 分红送转历史 | datacenter-web | §4.4 |
| 120日主力/大单资金流 | push2his | §4.5 |

## Step 3: Signal Interpretation

- 股东户数持续减少 → 筹码集中，可能主力吸筹
- 近 20 日主力净流入累计 → 与 `signal-data` 分钟级流向交叉验证

## Related Skills

- 北向/龙虎榜/热点 → `signal-data`
- 板块资金扫描 → `weekly-scan`（screening-tools）
