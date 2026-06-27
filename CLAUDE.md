# CLAUDE.md

Agent skills for A-share research. Layout follows [himself65/finance-skills](https://github.com/himself65/finance-skills).

## Repository structure

```
.claude-plugin/
  marketplace.json          # cn-data-providers, cn-market-analysis, cn-screening-tools, cn-social-readers
plugins/
  market-analysis/
    skills/
      a-finance-skills/     # unified router — all A-share requests start here when unclear
      thread-stock / sector-rotation / valuation-cn / earnings-* / volume-price …
  data-providers/           # A-share data layer
    skills/
      quote-data / fund-flow-data / research-data / signal-data
      fundamental-data / news-announce / finance-sentiment-cn
      trading-data/         # data-layer sub-router only (not the top-level entry)
  screening-tools/          # weekly-scan + fund-flow-collector
  social-readers/           # eastmoney / xueqiu / cls / opencli-reader
```

## Creating a new skill

1. Choose plugin group: `data-providers`, `market-analysis`, or `screening-tools`
2. Create `plugins/<group>/skills/<skill-name>/`
3. Write `SKILL.md` with `name` + trigger-rich `description`
4. Put API code / formulas in `references/`
5. Update root `README.md` skill table
6. Update `.claude-plugin/marketplace.json` if adding a new plugin group

## Skill routing

- **Unclear / multi-topic A-share request** → `a-finance-skills` (top router across all plugin groups)
- **Clear data intent** → specialized data skill (`quote-data`, `signal-data`, …)
- **Data only, layer unclear** → `trading-data` (sub-router; usually reached via `a-finance-skills`)
- **Stock picking** → `thread-stock` + `weekly-scan`
- **Valuation math** → `valuation-cn` + `quote-data` + `research-data`

## Data attribution

API endpoints in `data-providers` derived from [a-stock-data](https://github.com/simonlin1212/a-stock-data) by Simon 林.
