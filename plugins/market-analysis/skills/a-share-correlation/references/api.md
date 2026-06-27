# A股相关性分析 — API 参考

## 收益率相关性矩阵

```python
import pandas as pd
from mootdx.quotes import Quotes


def fetch_returns(codes: list[str], days: int = 60) -> pd.DataFrame:
    client = Quotes.factory(market="std")
    series = {}
    for code in codes:
        bars = client.bars(symbol=code, category=4, offset=days + 5)
        if bars is None or bars.empty:
            continue
        bars = bars.set_index("datetime")["close"].pct_change().dropna()
        series[code] = bars.tail(days)
    return pd.DataFrame(series).dropna(how="all")


def correlation_matrix(codes: list[str], days: int = 60) -> pd.DataFrame:
    returns = fetch_returns(codes, days)
    return returns.corr().round(3)


# 用法：AI-PCB 产业链
codes = ["600183", "002463", "002916", "300308", "300502"]
print(correlation_matrix(codes))
```

## 滚动相关性（趋势变化）

```python
def rolling_corr(code_a: str, code_b: str, window: int = 20, days: int = 120) -> pd.Series:
    ret = fetch_returns([code_a, code_b], days)
    return ret[code_a].rolling(window).corr(ret[code_b]).dropna()
```

## 板块同业发现

1. 从 `sector-rotation/supply-chain-map.md` 取同 Tier 标的池
2. `correlation_matrix()` 找 corr > 0.7 的集群
3. corr 突降 → 独立逻辑出现（订单/公告驱动）

## Beta 估算（相对沪深300）

```python
def beta_to_index(code: str, index_code: str = "000300", days: int = 60) -> float:
    ret = fetch_returns([code, index_code], days)
    if code not in ret.columns or index_code not in ret.columns:
        return float("nan")
    cov = ret[code].cov(ret[index_code])
    var = ret[index_code].var()
    return round(cov / var, 2) if var else float("nan")
```

## 配对交易提示

| corr | 含义 | 策略 |
|------|------|------|
| > 0.8 | 高度同涨同跌 | 板块龙头/跟风配对 |
| 0.5-0.8 | 中度相关 | 供应链上下游 |
| < 0.3 | 低相关 | 分散配置有效 |
| 转负 | 背离 | 检查独立催化剂 |

## 产业链关联（非价格相关）

供应链映射优先于价格 corr — 见 `sector-rotation` supply-chain-map。
