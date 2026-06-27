# A股财报复盘 — 完整工作流

## 一键脚本：earnings_recap(code, report_date=None)

```python
import re
import urllib.request
import requests
import pandas as pd
from datetime import datetime, timedelta
from mootdx.quotes import Quotes

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"


def normalize_code(code: str) -> str:
    return re.sub(r"[^0-9]", "", code)[-6:]


def tencent_quote(code: str) -> dict:
    prefix = "sh" if code.startswith(("6", "9")) else ("bj" if code.startswith("8") else "sz")
    url = f"https://qt.gtimg.cn/q={prefix}{code}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    vals = urllib.request.urlopen(req, timeout=10).read().decode("gbk").split('"')[1].split("~")
    return {"name": vals[1], "price": float(vals[3] or 0), "change_pct": float(vals[32] or 0)}


def ths_eps_forecast(code: str) -> float | None:
    url = f"https://basic.10jqka.com.cn/new/{code}/worth.html"
    r = requests.get(url, headers={"User-Agent": UA, "Referer": "https://basic.10jqka.com.cn/"}, timeout=15)
    r.encoding = "gbk"
    dfs = pd.read_html(r.text)
    for df in dfs:
        if not df.empty:
            try:
                return float(df.iloc[0].iloc[2])
            except (ValueError, IndexError):
                pass
    return None


def get_klines(code: str, days: int = 10) -> pd.DataFrame:
    client = Quotes.factory(market="std")
    bars = client.bars(symbol=code, category=4, offset=days + 5)
    if bars is None or bars.empty:
        return pd.DataFrame()
    return bars.tail(days)


def earnings_recap(code: str) -> dict:
    code = normalize_code(code)
    quote = tencent_quote(code)
    eps_actual = None
    revenue = profit = roe = None

    client = Quotes.factory(market="std")
    fin = client.finance(symbol=code)
    if fin is not None and not fin.empty:
        latest = fin.iloc[-1]
        eps_actual = float(latest.get("eps", 0) or 0)
        revenue = float(latest.get("income", 0) or 0)
        profit = float(latest.get("profit", 0) or 0)
        roe = float(latest.get("roe", 0) or 0)
        if len(fin) >= 2:
            prev = fin.iloc[-2]
            rev_yoy = (revenue / float(prev.get("income", 1) or 1) - 1) * 100
            profit_yoy = (profit / float(prev.get("profit", 1) or 1) - 1) * 100
        else:
            rev_yoy = profit_yoy = None
    else:
        rev_yoy = profit_yoy = None

    eps_expected = ths_eps_forecast(code)
    surprise_pct = None
    if eps_actual and eps_expected and eps_expected != 0:
        surprise_pct = round((eps_actual - eps_expected) / abs(eps_expected) * 100, 1)

    klines = get_klines(code, 5)
    price_reaction_5d = None
    if not klines.empty and len(klines) >= 2:
        price_reaction_5d = round(
            (klines.iloc[-1]["close"] / klines.iloc[0]["close"] - 1) * 100, 2
        )

    verdict = "neutral"
    if surprise_pct is not None:
        if surprise_pct > 5:
            verdict = "beat"
        elif surprise_pct < -5:
            verdict = "miss"

    return {
        "code": code,
        "name": quote["name"],
        "price": quote["price"],
        "today_change_pct": quote["change_pct"],
        "eps_actual": eps_actual,
        "eps_expected": eps_expected,
        "surprise_pct": surprise_pct,
        "verdict": verdict,
        "revenue": revenue,
        "profit": profit,
        "roe": roe,
        "revenue_yoy_pct": round(rev_yoy, 1) if rev_yoy is not None else None,
        "profit_yoy_pct": round(profit_yoy, 1) if profit_yoy is not None else None,
        "price_reaction_5d_pct": price_reaction_5d,
        "generated_at": datetime.now().isoformat(),
    }


if __name__ == "__main__":
    print(earnings_recap("688017"))
```

## 量价反应解读

| 财报结果 | 股价反应 | 操作含义 |
|----------|----------|----------|
| beat | 缩量上行 | 持有/回踩加仓 |
| beat | 放量滞涨/长上影 | 利好出尽，减仓 |
| miss | 缩量阴跌 | 观望等企稳 |
| miss | 放量跌停 | 清仓，逻辑破坏 |

配合 `volume-price` skill 的 `references/signals.md` 判断形态。

## 输出模板

```
## {name}({code}) 财报复盘

**结论**: {verdict}（EPS surprise {surprise_pct}%）

| 指标 | 实际 | 预期 | 同比 |
|------|------|------|------|
| EPS | | | |
| 营收 | | | {revenue_yoy}% |
| 净利润 | | | {profit_yoy}% |
| ROE | | | |

**股价**: 财报后5日 {price_reaction_5d}% | 今日 {today_change}%

**情景更新**: bull / base / bear + 概率 + 止损位
```
