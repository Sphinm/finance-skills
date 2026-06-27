# A股财报前瞻 — 完整工作流

## 一键脚本：earnings_preview(code)

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
    resp = urllib.request.urlopen(req, timeout=10)
    vals = resp.read().decode("gbk").split('"')[1].split("~")
    return {
        "name": vals[1],
        "price": float(vals[3] or 0),
        "pe_ttm": float(vals[39] or 0),
        "change_pct": float(vals[32] or 0),
        "mcap_yi": float(vals[44] or 0),
    }


def ths_eps_forecast(code: str) -> pd.DataFrame:
    url = f"https://basic.10jqka.com.cn/new/{code}/worth.html"
    r = requests.get(url, headers={"User-Agent": UA, "Referer": "https://basic.10jqka.com.cn/"}, timeout=15)
    r.encoding = "gbk"
    dfs = pd.read_html(r.text)
    for df in dfs:
        cols = [str(c) for c in df.columns]
        if any("每股收益" in c or "均值" in c for c in cols):
            return df
    return dfs[0] if dfs else pd.DataFrame()


def cninfo_search(code: str, keyword: str = "业绩预告", limit: int = 10) -> list[dict]:
    plate = "sh" if code.startswith("6") else ("bj" if code.startswith("8") else "sz")
    payload = {
        "stock": f"{code},{plate}",
        "tabName": "fulltext", "pageSize": str(limit), "pageNum": "1",
        "column": "SSE" if plate == "sh" else "SZSE",
        "category": "", "plate": "", "seDate": "",
        "searchkey": keyword, "secid": "",
        "sortName": "", "sortType": "", "isHLtitle": "true",
    }
    r = requests.post(
        "https://www.cninfo.com.cn/new/hisAnnouncement/query",
        data=payload,
        headers={"User-Agent": UA, "Referer": "https://www.cninfo.com.cn/", "Origin": "https://www.cninfo.com.cn"},
        timeout=15,
    )
    return [
        {"date": a.get("announcementTime", ""), "title": a.get("announcementTitle", ""), "type": a.get("announcementTypeName", "")}
        for a in (r.json().get("announcements") or [])
    ]


def mootdx_latest_finance(code: str) -> dict:
    client = Quotes.factory(market="std")
    fin = client.finance(symbol=code)
    if fin is None or (hasattr(fin, "empty") and fin.empty):
        return {}
    row = fin.iloc[-1] if hasattr(fin, "iloc") else fin
    return {
        "eps": float(row.get("eps", 0) or 0),
        "roe": float(row.get("roe", 0) or 0),
        "profit": float(row.get("profit", 0) or 0),
        "income": float(row.get("income", 0) or 0),
    }


def earnings_preview(code: str) -> dict:
    code = normalize_code(code)
    quote = tencent_quote(code)
    forecast_df = ths_eps_forecast(code)
    finance = mootdx_latest_finance(code)
    previews = cninfo_search(code, "业绩预告")
    reports = cninfo_search(code, "业绩快报")

    # 解析一致预期（表格结构可能变化，取首行均值列）
    eps_forecast = analyst_count = None
    if not forecast_df.empty:
        try:
            row0 = forecast_df.iloc[0]
            analyst_count = int(row0.iloc[1]) if pd.notna(row0.iloc[1]) else 0
            eps_forecast = float(row0.iloc[2]) if pd.notna(row0.iloc[2]) else None
        except (ValueError, IndexError):
            pass

    pe_fwd = quote["price"] / eps_forecast if eps_forecast and eps_forecast > 0 else None

    return {
        "code": code,
        "name": quote["name"],
        "price": quote["price"],
        "pe_ttm": quote["pe_ttm"],
        "pe_fwd": round(pe_fwd, 1) if pe_fwd else None,
        "eps_forecast": eps_forecast,
        "analyst_count": analyst_count,
        "latest_eps": finance.get("eps"),
        "latest_roe": finance.get("roe"),
        "latest_revenue": finance.get("income"),
        "latest_profit": finance.get("profit"),
        "preview_announcements": previews[:5],
        "express_announcements": reports[:3],
        "generated_at": datetime.now().isoformat(),
    }


# 用法
if __name__ == "__main__":
    r = earnings_preview("688017")
    print(r)
```

## 输出模板

| 字段 | 来源 | 解读 |
|------|------|------|
| pe_fwd | 股价 / 一致预期EPS | < 30x 成长股合理区间 |
| analyst_count | 同花顺 | < 3 家覆盖 → 预期不可靠 |
| preview_announcements | 巨潮 | 预增/预减/扭亏区间 |
| latest_eps vs eps_forecast | mootdx vs THS | 上季实际 vs 下季预期增速 |

## Beat/Miss 历史（手动扩展）

从 `research-data` 东财研报 API 拉 `predictThisYearEps`，与 mootdx 各季实际 EPS 对比，计算近 4 季 beat 率：

```python
# 见 research-data references/api.md eastmoney_reports()
# 对比 record['predictThisYearEps'] 与 mootdx finance 历史季度 eps
```

## 板块 Beta 上下文

财报发布前拉 `signal-data` 行业板块排名，看所属行业近 5 日资金净流入排名。
