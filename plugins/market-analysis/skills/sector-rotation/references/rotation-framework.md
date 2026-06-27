# 板块轮动框架 — A股主线识别

## 三层信号叠加

```
Layer 1: 资金层 — 行业/概念板块净流入排名（signal-data §3.7）
Layer 2: 题材层 — 强势股 reason 词频（signal-data §3.1）
Layer 3: 产业层 — 供应链 Tier 映射（supply-chain-map.md）
```

三层共振 → 主线确立；仅 Layer 1 或 2 → 轮动试探。

## 主线确立 checklist

| # | 条件 | 数据源 |
|---|------|--------|
| 1 | 行业板块连续 3 日净流入 Top 10 | fund-flow-collector SQLite 或 signal-data |
| 2 | 同花顺热点 reason 词频 Top 3 含同一题材 | ths_hot_reason() |
| 3 | 北向当日净流入与题材方向一致 | signal-data §3.2 |
| 4 | 产业链 Tier 1-2 标的 3+ 只同日异动 | weekly-scan |

满足 3/4 → 主线明确；满足 1-2 → 轮动期。

## 轮动周期操作

| 阶段 | 特征 | 操作 |
|------|------|------|
| 萌芽 | 板块首次进 Top20，成交温和放大 | 小仓试探龙头 |
| 主升 | 连续净流入 + 缩量上行 | 回踩 5/10 日线加仓 |
| 分化 | 龙头滞涨，跟风股放量 | 减跟风，留龙头 |
| 退潮 | 板块净流出 + 热点 reason 消失 | 清仓，等下一主线 |

## 跨市场映射

| A股主线 | 港股映射 | 美股/ETF映射 |
|---------|----------|-------------|
| AI算力 | 恒生科技 | KWEB / SMH |
| 光模块 | 中际旭创A | COHR / LITE |
| 半导体设备 | 中芯H | AMAT / LRCX |

详见 thread-stock `references/cross-market.md`。

## 供应链 Tier 优先级

```
Tier 1 上游材料（生益/亨通）→ 确定性最高，订单弹性最大
Tier 2 集成/模块（沪电/中际旭创）→ 弹性大，竞争加剧
Tier 3 设备（中微/北方华创）→ 周期长，受 capex 节奏影响
Tier 4 应用/软件 → 估值波动大，叙事驱动强
```

完整图谱见 `supply-chain-map.md`。

## 板块 beta vs 个股 alpha

**硬规则**：板块净流出时，不做逆 beta 个股做多。
- 板块 +5%，个股 +2% → alpha 负，弱于板块
- 板块 -3%，个股 +5% → 可能独立逻辑，需公告/订单验证

## 周度执行

```bash
# 1. 采集板块资金
cd plugins/screening-tools/skills/fund-flow-collector/scripts
uv run --with akshare python3 fund_flow_collector.py

# 2. 板块扫描
cd ../../weekly-scan/scripts
uv run --with akshare python3 weekly_scan.py --sector-only
```
