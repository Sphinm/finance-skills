---
name: signal-data
description: >
  A-share market signals: Tonghuashun hot stocks + theme tags, northbound flow (北向资金),
  Baidu concept attribution + minute fund flow, dragon-tiger list (龙虎榜),
  unlock calendar (限售解禁), sector/industry rankings.
  Triggers: 强势股, 题材, 热点, 概念归因, 北向资金, 沪股通, 深股通,
  龙虎榜, 席位, 净买入, 解禁, 限售, 行业轮动, 板块排名, 主线判断.
---

# Signal Data — A股信号层

题材、资金方向、事件信号。读 `references/api.md`（内容较多，按需加载对应章节）。

## Step 1: Prerequisites

```bash
pip install requests pandas
```

## Step 2: Match Request

| 用户需求 | 数据源 | 参考 |
|----------|--------|------|
| 当日强势股+题材归因 | 同花顺热点 | §3.1 |
| 北向分钟/历史 | 同花顺 hsgtApi | §3.2 |
| 概念板块归属 | 百度股市通 | §3.3 |
| 分钟级个股资金流 | 百度股市通 | §3.4 |
| 个股龙虎榜席位 | 东财 datacenter | §3.5 |
| 限售解禁日历 | 东财 datacenter | §3.6 |
| 行业板块排名 | 东财（V3.0） | §3.7 |
| 全市场龙虎榜 | 东财 datacenter | §3.8 |
| 题材+资金组合验证 | 多源组合 | §3.9 |

## Step 3: Combo Workflow

题材热度（§3.1 reason 词频）+ 北向流向（§3.2）+ 行业资金（§3.7）→ 验证主线是否成立。

## Related Skills

- 两融/股东户数 → `fund-flow-data`
- 板块轮动分析 → `sector-rotation`
- 周度扫描 → `weekly-scan`
