# finance-skills

> [!WARNING]
> This project is for educational and informational purposes only. Nothing here constitutes financial advice. Always do your own research and consult a qualified financial advisor before making investment decisions.

Claude skills marketplace for Chinese equity thematic stock selection. Layout follows the [himself65/finance-skills](https://github.com/himself65/finance-skills) convention.

## Quick Start

### Claude Code — Install the plugin

```bash
npx plugins add Sphinm/finance-skills
```

### Claude Code — Install just the skill

```bash
npx skills add Sphinm/finance-skills
```

### Local development install (from a clone)

```bash
git clone https://github.com/Sphinm/finance-skills.git ~/finance-skills
ln -s ~/finance-skills/plugins/thread-stock/skills/thread-stock ~/.claude/skills/thread-stock
# Cursor:
ln -s ~/finance-skills/plugins/thread-stock/skills/thread-stock ~/.cursor/skills/thread-stock
```

## Available Skills

| Skill | Description |
|-------|-------------|
| [thread-stock](plugins/thread-stock/skills/thread-stock/) | A-share thematic selection — supply chain + earnings + valuation + flow funnel, 9 pitfalls + case studies |

## Data Dependencies

- **akshare** / **yfinance** — used by bundled scripts (`weekly_scan.py`, `fund_flow_collector.py`)
- Optional: [a-stock-data](https://github.com/simonlin1212/a-stock-data) for extended A-share data endpoints

## License

MIT
