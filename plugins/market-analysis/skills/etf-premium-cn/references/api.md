# A股 ETF 溢价率 — API 参考

## 场内 ETF 溢价估算

A 股 ETF 无 Yahoo `navPrice`，用东财 IOPV（基金份额参考净值）对比场内价格。

```python
import requests
import urllib.request

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

# 常见 A 股 ETF
ETF_MAP = {
    "510050": "上证50ETF",
    "510300": "沪深300ETF",
    "510500": "中证500ETF",
    "159915": "创业板ETF",
    "512480": "半导体ETF",
    "512760": "芯片ETF",
    "515790": "光伏ETF",
    "588000": "科创50ETF",
}


def etf_quote(code: str) -> dict:
    prefix = "sh" if code.startswith(("5", "6")) else "sz"
    url = f"https://qt.gtimg.cn/q={prefix}{code}"
    vals = urllib.request.urlopen(
        urllib.request.Request(url, headers={"User-Agent": UA}), timeout=10
    ).read().decode("gbk").split('"')[1].split("~")
    return {
        "code": code,
        "name": vals[1],
        "price": float(vals[3] or 0),
        "change_pct": float(vals[32] or 0),
        "amount_yi": round(float(vals[37] or 0) / 10000, 2),
    }


def etf_iopv(code: str) -> float | None:
    """东财 ETF 基金份额参考净值 IOPV"""
    market = 1 if code.startswith(("5", "6")) else 0
    url = "https://push2.eastmoney.com/api/qt/stock/get"
    params = {
        "fltt": "2", "invt": "2",
        "fields": "f43,f46,f60,f169,f170",
        "secid": f"{market}.{code}",
    }
    r = requests.get(url, params=params, headers={"User-Agent": UA}, timeout=10)
    d = r.json().get("data", {})
    # f46 常为 IOPV/参考净值（东财字段，实测校准）
    iopv = d.get("f46")
    return float(iopv) if iopv else None


def etf_premium(code: str) -> dict:
    q = etf_quote(code)
    iopv = etf_iopv(code)
    premium_pct = None
    if iopv and iopv > 0:
        premium_pct = round((q["price"] - iopv) / iopv * 100, 3)
    return {**q, "iopv": iopv, "premium_pct": premium_pct}


def etf_premium_batch(codes: list[str]) -> list[dict]:
    return [etf_premium(c) for c in codes]
```

## 溢价解读（A股场内 ETF）

| 溢价率 | 含义 |
|--------|------|
| < 0.1% | 正常套利区间 |
| 0.1% - 0.5% | 轻微溢价，情绪偏热 |
| 0.5% - 2% | 明显溢价，追涨需谨慎 |
| > 2% | 异常溢价，可能限购/申赎受阻 |
| < -0.5% | 折价，恐慌或流动性问题 |

## 主题 ETF 横向对比

```python
theme_etfs = ["512480", "512760", "515790", "588000"]
for r in sorted(etf_premium_batch(theme_etfs), key=lambda x: x.get("premium_pct") or 0, reverse=True):
    print(f"{r['name']}: 溢价 {r['premium_pct']}% 今日 {r['change_pct']}%")
```

## 与个股关系

ETF 溢价飙升 + 板块龙头涨停 → 情绪极端，不宜追高个股。
配合 `sector-rotation` 判断主题是否过热。
