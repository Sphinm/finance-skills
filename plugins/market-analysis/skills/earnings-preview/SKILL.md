---
name: earnings-preview
description: >
  Pre-earnings briefing for A-shares: consensus EPS via Tonghuashun, preview announcements via CNINFO,
  latest quarterly financials via mootdx, historical beat/miss context, sector beta.
  Triggers: 财报前瞻, 业绩预览, 季报前瞻, 年报前瞻, 业绩预告, 财报前分析,
  一致预期, beat率, 财报前看什么, upcoming earnings A-share, 业绩快报.
---

# Earnings Preview — A股财报前瞻

财报发布前 30 秒生成完整简报。执行 `references/workflow.md` 中的 `earnings_preview(code)`。

## Step 1: Run Preview Script

```bash
pip install mootdx requests pandas
```

读并执行 `references/workflow.md` § `earnings_preview()`，替换 `code` 为用户标的。

## Step 2: Interpret Key Fields

| 字段 | 阈值 | 含义 |
|------|------|------|
| analyst_count | < 3 | 覆盖不足，一致预期不可靠 |
| pe_fwd | > 50 | 预期已透支 |
| preview_announcements | 预增区间 | 与一致预期交叉验证 |
| latest_eps vs eps_forecast | 增速 | 上季基数影响 beat 难度 |

## Step 3: Historical Beat Rate

从 `research-data` 东财研报拉近 4 季 `predictThisYearEps`，对比 mootdx 实际 EPS，计算 beat 率（见 workflow.md § Beat/Miss 历史）。

## Step 4: Sector Context

激活 `signal-data` 拉所属行业近 5 日资金排名，判断板块 beta 是否顺风。

## Step 5: Output

按 workflow.md 输出模板填写，附 bull/base/bear 三情景 + 概率。

## Hard Rules

- 推荐前必须查阅最新季报（thread-stock）
- PEG > 2 不推荐

## Reference Files

- `references/workflow.md` — 完整 Python 脚本 + 输出模板
