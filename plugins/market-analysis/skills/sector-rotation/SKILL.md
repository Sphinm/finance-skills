---
name: sector-rotation
description: >
  A-share sector rotation: industry fund flow ranking, thematic main-line identification,
  supply chain tier mapping, rotation cycle playbook, cross-market mapping (A/H/US).
  Triggers: 板块轮动, 主线判断, 产业链, 供应链拆解, AI算力链, 半导体链,
  板块资金, 行业对比, 题材轮动, 哪个板块在涨, sector rotation A-share.
---

# Sector Rotation — A股板块轮动

## Step 1: Pull Live Sector Data

1. 行业板块排名 + 资金 → `signal-data` §3.7
2. 历史趋势 → `fund-flow-collector` SQLite
3. 题材归因 → `signal-data` §3.1 `ths_hot_reason()`

## Step 2: Apply Rotation Framework

读 `references/rotation-framework.md`：
- 三层信号叠加（资金 + 题材 + 产业）
- 主线确立 checklist（4 项满足 3 项）
- 轮动周期四阶段操作表

## Step 3: Supply Chain Tier

读 `references/supply-chain-map.md` 定位标的 Tier，优先 Tier 1-2。

## Step 4: Cross-Market Check

若 A 股主线与港股/美股背离，加载 thread-stock `references/cross-market.md`。

## Step 5: Output

| 输出项 | 内容 |
|--------|------|
| 当前主线 | 题材 + 证据 |
| 阶段 | 萌芽/主升/分化/退潮 |
| 推荐标的 | 板块内 PEG 最低（配合 valuation-cn） |
| 仓位 | 主线明确 20-25%，轮动期 8-10% |

## Reference Files

| 文件 | 内容 |
|------|------|
| `references/rotation-framework.md` | 主线识别 + 轮动操作框架 |
| `references/supply-chain-map.md` | AI 产业链图谱 + 标的 Tier |
