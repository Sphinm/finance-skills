# A股市场情绪 — 综合评分

## 情绪指数：market_sentiment_score()

```python
import requests
import pandas as pd
from collections import Counter

UA = "Mozilla/5.0"


def ths_hot_reason(date: str = None) -> pd.DataFrame:
    from datetime import date as _date
    if date is None:
        date = _date.today().strftime("%Y-%m-%d")
    url = f"http://zx.10jqka.com.cn/event/api/getharden/date/{date}/orderby/date/orderway/desc/charset/GBK/"
    r = requests.get(url, headers={"User-Agent": UA}, timeout=10)
    data = r.json()
    rows = data.get("data") or []
    return pd.DataFrame(rows)


def theme_heat_index() -> dict:
    """题材热度：强势股数量 + reason 词频"""
    df = ths_hot_reason()
    if df.empty:
        return {"hot_count": 0, "top_themes": []}
    reasons = " ".join(str(x) for x in df.get("reason", df.get("题材归因", [])))
    words = [w for w in reasons.replace("+", " ").split() if len(w) >= 2]
    top = Counter(words).most_common(5)
    return {
        "hot_count": len(df),
        "top_themes": top,
        "avg_change_pct": float(df.get("zhangfu", df.get("涨幅%", pd.Series([0]))).astype(float).mean()),
    }


def northbound_sentiment() -> dict:
    """北向资金方向（当日）"""
    url = "https://push2.eastmoney.com/api/qt/kamt.rtmin/get"
    params = {"fields1": "f1,f2,f3,f4", "fields2": "f51,f52,f53,f54,f55,f56", "ut": "b2884a393a59ad64002292a3e90d46a5"}
    r = requests.get(url, params=params, headers={"User-Agent": UA}, timeout=10)
    # 简化：解析最新分钟净流入
    return {"source": "eastmoney_kamt", "raw": r.text[:200]}


def stock_sentiment(code: str) -> dict:
    """个股情绪：是否在热点榜 + 涨幅"""
    df = ths_hot_reason()
    if df.empty:
        return {"on_hot_list": False}
    code_col = "code" if "code" in df.columns else "代码"
    match = df[df[code_col].astype(str).str.contains(code[-6:])]
    if match.empty:
        return {"on_hot_list": False, "sentiment": "冷门"}
    row = match.iloc[0]
    reason = row.get("reason", row.get("题材归因", ""))
    change = float(row.get("zhangfu", row.get("涨幅%", 0)) or 0)
    return {
        "on_hot_list": True,
        "reason": reason,
        "change_pct": change,
        "sentiment": "极热" if change > 7 else "偏热" if change > 3 else "温和",
    }


def market_sentiment_summary() -> dict:
    theme = theme_heat_index()
    score = 50
    if theme["hot_count"] > 80:
        score += 15
    elif theme["hot_count"] > 50:
        score += 8
    if theme.get("avg_change_pct", 0) > 3:
        score += 10
    score = min(100, max(0, score))
    label = "贪婪" if score > 70 else "中性" if score > 40 else "恐惧"
    return {"score": score, "label": label, "theme": theme}
```

## 解读

| score | label | 操作参考 |
|-------|-------|----------|
| > 70 | 贪婪 | 谨慎追高，关注缩量滞涨 |
| 40-70 | 中性 | 正常选股 |
| < 40 | 恐惧 | 关注错杀龙头，小仓试探 |

## 数据源

| 维度 | 源 | skill |
|------|-----|-------|
| 题材热度 | 同花顺热点 | signal-data |
| 北向 | 东财 kamt | signal-data |
| 讨论 | 雪球 | xueqiu-reader |
| 快讯 | 财联社 | cls-reader |
