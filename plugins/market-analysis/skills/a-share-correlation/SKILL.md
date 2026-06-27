---
name: a-share-correlation
description: >
  Analyze A-share stock correlations: return correlation matrix, rolling correlation,
  beta to CSI 300, sector peer clustering, supply chain sympathy plays.
  Triggers: 相关性, 联动, 同涨同跌, beta, 和沪深300关系, 产业链联动,
  配对交易,  sympathy play, 板块同业, correlation A-share, 哪些股票一起涨.
---

# A-Share Correlation — A股相关性分析

## Step 1: Route Request

| 用户问 | 方法 | 参考 |
|--------|------|------|
| 多只股票相关性矩阵 | `correlation_matrix(codes)` | `references/api.md` |
| 两只股票关系变化 | `rolling_corr(a, b)` | §滚动相关性 |
| 相对大盘 beta | `beta_to_index(code)` | §Beta |
| 产业链谁跟谁 | supply-chain-map | `sector-rotation` skill |

## Step 2: Execute

```bash
pip install mootdx pandas
```

读 `references/api.md` 执行对应函数，默认回看 60 交易日。

## Step 3: Interpret

- corr > 0.8：同板块/同叙事，龙头涨跟风跟
- corr 骤降：独立订单或公告驱动
- beta > 1.5：高弹性，板块行情时放大

## Reference Files

- `references/api.md` — 相关性矩阵 / 滚动 corr / beta 完整代码
