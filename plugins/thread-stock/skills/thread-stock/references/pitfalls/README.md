# Selection Pitfalls — 选股陷阱

9 个 A 股/港股主题投资中的常见分析偏差。每个陷阱一个文件，按需加载。

## Index

| # | Severity | Title | File |
|---|----------|-------|------|
| 1 | HIGH | 蹭概念 — 主营与叙事无关 | `01-concept-stock.md` |
| 2 | HIGH | 增收不增利 — 营收涨利润跌 | `02-revenue-no-profit.md` |
| 3 | HIGH | 影子股 — 本体平庸靠持股撑估值 | `03-shadow-stock.md` |
| 4 | HIGH | PEG 失配 — 估值远超增速 | `04-peg-mismatch.md` |
| 5 | HIGH | 散户接盘 — 主力出散户进 | `05-retail-relay.md` |
| 6 | MEDIUM | 追涨停 — 高换手涨停后追入 | `06-chase-limit-up.md` |
| 7 | HIGH | ETF 套牢 — 重仓 beta 向下的宽基 | `07-etf-trap.md` |
| 8 | HIGH | 叙事压过报表 — 用故事忽略财报 | `08-narrative-over-report.md` |
| 9 | HIGH | 机会成本盲区 — 死扛亏损标的 | `09-opportunity-cost.md` |

## Quick Lookup by Situation

- **看到一只"AI概念股"想买**: 1, 8
- **标的营收很好但总觉得不对**: 2, 4
- **别人推荐的"便宜"标的**: 3, 4
- **想追今天涨停的票**: 5, 6
- **重仓ETF被套不知道怎么办**: 7, 9
- **持仓亏损但不想卖**: 7, 9
- **液冷/机器人等热门叙事**: 1, 2, 8

## Adding a New Pitfall

1. Copy `_template.md` to `NN-slug.md`（下一个序号）
2. Fill out frontmatter（`title`, `severity`, `appliesTo`, `tags`）
3. Write rule + why it matters + how to apply
4. Reference relevant case study under `../ticker/`
5. Add row to the table above
