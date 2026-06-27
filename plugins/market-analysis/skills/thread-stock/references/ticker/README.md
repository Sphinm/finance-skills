# Ticker Case Studies — 个股案例库

每个已分析的标的一个文件。按需加载——索引列出标的、事件、结论；完整文件只在需要时读取。

## Index

| 标的 | 事件 | 日期 | 结论 | Key Lesson | File |
|------|------|------|------|------------|------|
| 生益科技 | AI算力CCL涨停 | 2026-05-18 | 核心仓位候选 | 缩量涨停=最健康突破; CCL是AI"卖铲子"最确定环节 | `shengyi-2026-05.md` |
| 英维克 | 液冷叙事vs报表崩塌 | 2026-05-18 | 淘汰 | 叙事再好也要看报表; Q1利润-82%直接否决 | `yingweike-2026-05.md` |
| 亨通光电 | 光纤涨价+AI需求 | 2026-05-18 | 核心仓位候选 | PEG 0.41是极端低估; 涨价周期确认=增速可持续 | `hengtong-2026-05.md` |
| 恒生互联网 | ETF套牢+利好不涨 | 2026-05-18 | 减仓/换仓 | 利率环境>公司基本面; 机会成本>显性亏损 | `hstech-2026-05.md` |

## Quick Lookup by Pattern

- **CCL/PCB涨价+缩量突破**: `shengyi-2026-05.md`
- **叙事很美但报表崩塌**: `yingweike-2026-05.md`
- **光纤涨价周期+PEG极低**: `hengtong-2026-05.md`
- **ETF套牢+利好出尽+机会成本**: `hstech-2026-05.md`
- **追涨停择时**: `shengyi-2026-05.md`（涨停后如何参与）
- **增收不增利识别**: `yingweike-2026-05.md`
- **跨市场配置失误**: `hstech-2026-05.md`

## Adding a New Case Study

1. Copy `_template.md` to `<name>-YYYY-MM.md`
2. Fill out frontmatter
3. Document: Setup → Analysis → Decision → Outcome → Lessons
4. Add row to the index above
5. If the case yields new pitfalls, add files under `../pitfalls/` and link them
