# A股流动性分析 — API 参考

## 实时流动性快照

```python
import urllib.request
from mootdx.quotes import Quotes

UA = "Mozilla/5.0"


def liquidity_snapshot(code: str) -> dict:
    """综合流动性指标"""
    prefix = "sh" if code.startswith(("6", "9")) else ("bj" if code.startswith("8") else "sz")
    url = f"https://qt.gtimg.cn/q={prefix}{code}"
    vals = urllib.request.urlopen(
        urllib.request.Request(url, headers={"User-Agent": UA}), timeout=10
    ).read().decode("gbk").split('"')[1].split("~")

    price = float(vals[3] or 0)
    turnover_pct = float(vals[38] or 0)
    amount_wan = float(vals[37] or 0)  # 成交额万元
    float_mcap_yi = float(vals[45] or 0)
    vol_ratio = float(vals[49] or 0)
    limit_up = float(vals[47] or 0)
    limit_down = float(vals[48] or 0)

    # 五档盘口 spread
    client = Quotes.factory(market="std")
    q = client.quotes(symbol=[code])
    spread_pct = None
    if q is not None and not q.empty:
        row = q.iloc[0]
        bid1, ask1 = float(row.get("bid1", 0) or 0), float(row.get("ask1", 0) or 0)
        if bid1 > 0 and ask1 > 0:
            spread_pct = round((ask1 - bid1) / bid1 * 100, 3)
    # 距涨跌停距离
    dist_limit_up = round((limit_up - price) / price * 100, 2) if limit_up and price else None
    dist_limit_down = round((price - limit_down) / price * 100, 2) if limit_down and price else None

    # 流动性评级
    if amount_wan >= 100000:  # 日成交额 > 10亿
        tier = "高流动性"
    elif amount_wan >= 30000:
        tier = "中等"
    else:
        tier = "低流动性(谨慎)"

    return {
        "code": code, "name": vals[1], "price": price,
        "turnover_pct": turnover_pct,
        "amount_yi": round(amount_wan / 10000, 2),
        "float_mcap_yi": float_mcap_yi,
        "vol_ratio": vol_ratio,
        "spread_pct": spread_pct,
        "dist_limit_up_pct": dist_limit_up,
        "dist_limit_down_pct": dist_limit_down,
        "liquidity_tier": tier,
    }
```

## 涨跌停流动性（A股特有）

| 状态 | 特征 | 交易含义 |
|------|------|----------|
| 一字涨停 | 换手 < 1%，封单极大 | 无法买入，等开板 |
| 换手涨停 5-10% | 封板坚决 | 次日溢价概率高 |
| 换手涨停 > 15% | 分歧巨大 | 不追，等次日 |
| 跌停封死 | 无量 | 无法卖出，等翘板 |

## 冲击成本估算

```python
def impact_estimate(code: str, order_pct_of_float: float = 0.01) -> str:
    """
    order_pct_of_float: 订单占流通市值比例，默认 1%
    粗估：低流动性标的 1% 订单可能冲击 0.5-2%
    """
    snap = liquidity_snapshot(code)
    if snap["liquidity_tier"] == "高流动性":
        return "冲击成本 < 0.1%，可正常交易"
    if snap["liquidity_tier"] == "中等":
        return f"预估冲击 0.2-0.5%，建议分批"
    return f"预估冲击 0.5-2%+，{order_pct_of_float*100}%流通盘订单需谨慎"
```

## 20 日平均换手

```python
def avg_turnover_20d(code: str) -> float:
    client = Quotes.factory(market="std")
    bars = client.bars(symbol=code, category=4, offset=25)
    if bars is None or bars.empty:
        return 0.0
    # mootdx bars 无换手字段，用成交额/流通市值近似
    return float(bars["amount"].tail(20).mean())
```
