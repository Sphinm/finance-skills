# Skill 全索引

用户点名时直接用 **name** 列；不点名时由 `a-finance-skills` 路由自动选择。

## 统一入口

| name | 用途 |
|------|------|
| **a-finance-skills** | 总路由，意图不明时用 |

## cn-data-providers

| name | 一句话 |
|------|--------|
| quote-data | 行情/K线/盘口/指数/ETF |
| fund-flow-data | 两融/大宗/股东户数/120日资金流 |
| research-data | 研报/一致预期/iwencai |
| signal-data | 热点/北向/龙虎榜/解禁/板块 |
| fundamental-data | 财报/F10/新浪三表 |
| news-announce | 新闻/巨潮公告 |
| finance-sentiment-cn | 市场情绪评分 |
| trading-data | 仅数据层子路由 |

## cn-market-analysis

| name | 一句话 |
|------|--------|
| a-finance-skills | 统一入口（本 skill） |
| thread-stock | 主题选股四层漏斗（核心） |
| sector-rotation | 板块轮动/主线 |
| valuation-cn | PEG/前向PE/同业对比 |
| earnings-preview | 财报前瞻 |
| earnings-recap | 财报复盘 |
| volume-price | 量价信号 |
| a-share-correlation | 相关性/beta |
| a-share-liquidity | 流动性/冲击成本 |
| etf-premium-cn | ETF溢价率 |

## cn-screening-tools

| name | 一句话 |
|------|--------|
| weekly-scan | 周度选股脚本 |
| fund-flow-collector | 板块资金SQLite采集 |

## cn-social-readers

| name | 一句话 |
|------|--------|
| eastmoney-reader | 东财 opencli |
| xueqiu-reader | 雪球讨论 |
| cls-reader | 财联社快讯 |
| opencli-reader | 其他国内站 fallback |

## 用户怎么说 → 走哪

| 用户输入示例 | 路由 |
|--------------|------|
| `用 a-finance-skills 看看 688017` | 自动拆 quote + valuation + signal |
| `帮我选股` | thread-stock + weekly-scan |
| `今天市场怎么样` | finance-sentiment-cn + signal-data |
| `这只票贵不贵` | valuation-cn |
| 只提「龙虎榜」 | 直达 signal-data，跳过本路由 |
