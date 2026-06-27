# finance-skills

> [!WARNING]
> Educational purposes only. Not financial advice.

**finance-skills** 是面向 A 股（沪深）研究的 Agent Skills 合集，供 Claude Code、Cursor 等 AI 编程助手安装使用。把行情与基本面数据、估值与财报分析、周度选股扫描、东财/雪球/财联社阅读等能力封装成可复用 skill，避免每次会话从零拼 API 和流程。

仓库按职责拆成四个 plugin：`cn-data-providers`（行情、资金流、研报、信号、财报、新闻等数据层）、`cn-market-analysis`（选股、估值、财报、量价、相关性、ETF 溢价等分析）、`cn-screening-tools`（周度扫描与板块资金采集）、`cn-social-readers`（社交媒体与快讯阅读）。意图不明确时从 **`a-finance-skills`** 总入口进入，由它路由到各 plugin 下的专项 skill；只要数据且层不明时，再由 `trading-data` 做数据层子路由。

## Skill Routing

| Router | Scope | When to use |
|--------|-------|-------------|
| **`a-finance-skills`** | 全库总入口（data / analysis / screening / readers） | A 股问题意图不明、跨多主题、或用户说「用 a-finance-skills」 |
| `trading-data` | 仅 cn-data-providers 数据层子路由 | 只要数据、但不知该用哪类 API（通常由 `a-finance-skills` 转入） |
| 专项 skill | 单一领域 | 意图已清晰（如只问龙虎榜 → `signal-data`）时直达，跳过路由 |

安装 `cn-market-analysis` 即可获得 `a-finance-skills`；其余 plugin 按需添加。

## Quick Start

```bash
npx plugins add Sphinm/finance-skills
npx plugins add Sphinm/finance-skills/cn-data-providers
npx plugins add Sphinm/finance-skills/cn-market-analysis
npx plugins add Sphinm/finance-skills/cn-social-readers
```

## Plugin Groups

### cn-data-providers (8 skills)

| Skill | Description |
|-------|-------------|
| quote-data | mootdx + 腾讯 + 百度K线 |
| fund-flow-data | 两融/大宗/股东户数/120日资金流 |
| research-data | 东财研报 + 同花顺一致预期 |
| signal-data | 热点/北向/龙虎榜/解禁/板块 |
| fundamental-data | 财报/F10/新浪三表 |
| news-announce | 新闻 + 巨潮公告 |
| finance-sentiment-cn | 市场情绪评分 + 题材热度 |
| trading-data | 数据层子路由（非全库入口） |

### cn-market-analysis (10 skills)

| Skill | Description |
|-------|-------------|
| **a-finance-skills** | **全库统一入口 — 自动路由到各 plugin 下专项 skill** |
| thread-stock | 主题选股四层漏斗 + 踩坑 + 案例 |
| sector-rotation | 板块轮动 + 主线识别 |
| valuation-cn | PEG / 前向PE / 同业对比 |
| earnings-preview | 财报前瞻（完整 workflow） |
| earnings-recap | 财报复盘（surprise + 量价） |
| volume-price | 量价信号库 |
| a-share-correlation | 相关性矩阵 / beta |
| a-share-liquidity | 流动性 / 冲击成本 / 涨跌停 |
| etf-premium-cn | 场内 ETF 溢价率 |

### cn-screening-tools (2 skills)

| Skill | Description |
|-------|-------------|
| weekly-scan | 周度选股扫描 |
| fund-flow-collector | 板块资金 SQLite 采集 |

### cn-social-readers (4 skills)

| Skill | Description |
|-------|-------------|
| eastmoney-reader | 东财 opencli |
| xueqiu-reader | 雪球讨论/情绪 |
| cls-reader | 财联社快讯 |
| opencli-reader | 中国区 opencli fallback |

## Dependencies

- **mootdx** / **requests** / **pandas** — data & analysis skills
- **akshare** / **yfinance** — screening scripts
- **opencli** — social readers (`npm i -g @jackwener/opencli`)

## License

MIT
