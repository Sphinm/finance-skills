---
name: a-finance-skills
description: >
  Unified entry point for all A-share finance skills. Use this skill whenever the user asks
  anything about Chinese stocks without naming a specific skill — the agent reads this router
  first, classifies intent, then activates the correct specialized skill(s).
  Triggers: A股, 中国股市, 帮我看看, 分析一下, 调研, 能不能买, 怎么样,
  查一下, 看看这个票, 今天市场, 有什么机会, a-finance-skills,
  any vague or multi-topic A-share request.
  User may also say "用 a-finance-skills" to force this entry. When intent is already clear
  (e.g. only 龙虎榜), skip this router and go directly to the specialized skill.
---

# A-Finance-Skills — 统一入口

**你是 A 股研究的总调度。** 用户只对你说一句话时，先在这里分类意图，再激活对应 skill，可串联多个 skill 完成复杂任务。

用户点名 `用 a-finance-skills` 时，必须走本路由。

---

## Step 1: 意图分类（只选一个主路径，复杂任务可串联）

| 用户说什么 | 主 skill | 常配合 |
|------------|----------|--------|
| 行情/价格/K线/盘口/指数/ETF价格 | `quote-data` | — |
| 北向/龙虎榜/热点/题材/解禁/板块排名 | `signal-data` | `sector-rotation` |
| 两融/大宗/股东户数/120日资金流 | `fund-flow-data` | — |
| 研报/一致预期/PDF | `research-data` | — |
| 财报/三表/F10/ROE/EPS | `fundamental-data` | — |
| 新闻/公告/巨潮 | `news-announce` | `cls-reader` |
| 财联社/东财/雪球/微博 | `cls-reader` / `eastmoney-reader` / `xueqiu-reader` | `opencli-reader` |
| 估值/PEG/贵不贵/同业对比 | `valuation-cn` | `quote-data` + `research-data` |
| 财报前/业绩预期/预告 | `earnings-preview` | `fundamental-data` |
| 财报后/超预期/beat miss | `earnings-recap` | `volume-price` |
| 量价/入场/止损/涨停换手 | `volume-price` | `quote-data` |
| 板块轮动/主线/产业链 | `sector-rotation` | `signal-data` + `thread-stock` |
| **选股/能不能买/有什么票** | `thread-stock` | `weekly-scan` → 四层漏斗 |
| 周度扫描/板块资金采集 | `weekly-scan` / `fund-flow-collector` | — |
| 相关性/联动/beta | `a-share-correlation` | `sector-rotation` |
| 流动性/冲击成本/涨跌停 | `a-share-liquidity` | — |
| ETF 溢价/折价 | `etf-premium-cn` | — |
| 市场情绪/贪婪恐惧/热度 | `finance-sentiment-cn` | `signal-data` |
| 仅数据、不知哪层 | `trading-data` | 数据子路由 |
| 意图模糊 / 跨多主题 | **本表 + 下方组合流程** | — |

---

## Step 2: 常见组合流程（自动串联，无需用户点名）

### 流程 A — 单票快速看盘（30秒）

```
quote-data → valuation-cn → signal-data(资金流) → 输出结论
```

### 流程 B — 完整选股（thread-stock 标准）

```
fund-flow-collector → weekly-scan → thread-stock 四层漏斗
  → 必要时 valuation-cn + volume-price + pitfalls
```

### 流程 C — 财报季

```
财报前: earnings-preview
财报后: earnings-recap → volume-price → 更新 valuation-cn
```

### 流程 D — 板块/主线

```
signal-data(板块+热点) → sector-rotation → valuation-cn(板块内最低PEG)
```

### 流程 E — 新标的调研

读 `trading-data/references/workflows.md` 流程 D，或串联：

```
fundamental-data → research-data → valuation-cn → signal-data → news-announce
```

---

## Step 3: 执行规则

1. **不要一次加载所有 skill** — 只激活当前步骤需要的 1-2 个
2. **数据优先于结论** — 没拉到数据前不给买卖建议
3. **thread-stock 硬规则** — 推荐前必看季报；PEG>2 不推荐；必须给止损
4. **脚本任务** — 选股必先 `weekly-scan`，采集必先 `fund-flow-collector`
5. **社媒** — 优先专用 reader，搞不定再用 `opencli-reader`

---

## Step 4: 输出

- 说明激活了哪些 skill、为什么
- 表格呈现数据
- 买卖建议附 bull/base/bear + 止损位

---

## 子 skill 索引

完整 skill 列表见 `references/skill-index.md`。
