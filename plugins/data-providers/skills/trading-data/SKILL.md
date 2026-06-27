---
name: trading-data
description: >
  Router skill for A-share **data layer only** — use when request is data-specific but layer
  is unclear. For any general A-share question, use `a-finance-skills` unified entry instead.
  Triggers: 拉数据, 哪个API, 数据层路由 (NOT general 分析/选股/估值 — those go to a-finance-skills).
---

# Trading Data — A股数据路由

当用户请求跨多层数据或意图不明确时，按以下路由分发。**意图明确时优先激活专项 skill，勿走本路由。**

## Routing Table

| 用户意图 | 激活 Skill |
|----------|------------|
| 行情/K线/盘口/指数/ETF | `quote-data` |
| 北向/龙虎榜/热点/解禁/板块排名 | `signal-data` |
| 两融/大宗/股东户数/120日资金流 | `fund-flow-data` |
| 研报/一致预期/iwencai | `research-data` |
| 财报/三表/F10 | `fundamental-data` |
| 新闻/公告/财联社 | `news-announce` |
| PEG/前向PE/估值框架 | `valuation-cn` |
| 选股/扫描/板块资金 | `weekly-scan` |
| 相关性/beta | `a-share-correlation` |
| 流动性/冲击成本 | `a-share-liquidity` |
| ETF溢价 | `etf-premium-cn` |
| 市场情绪 | `finance-sentiment-cn` |
| 东财/雪球/财联社 | `cn-social-readers` |

## Multi-Layer Workflows

完整调研流程见 `references/workflows.md`：
- 流程 A：单票完整估值（30秒）
- 流程 B：批量估值对比
- 流程 C：主题研报批量检索
- 流程 D：新标的快速调研

## FAQ

常见问题见 `references/faq.md`（mootdx vs 腾讯、海外 IP、iwencai 401 等）。

## Attribution

数据端点源自 [a-stock-data](https://github.com/simonlin1212/a-stock-data)（Simon 林），本仓库按层拆分为专项 skills。
