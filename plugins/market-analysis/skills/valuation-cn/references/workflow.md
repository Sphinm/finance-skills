# A股估值 — 完整工作流

## 单票估值：full_valuation(code)

```python
import math
import re
import urllib.request
import requests
import pandas as pd

UA = "Mozilla/5.0"


def normalize_code(code: str) -> str:
    return re.sub(r"[^0-9]", "", code)[-6:]


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


def full_valuation(code: str) -> dict:
    code = normalize_code(code)
    prefix = "sh" if code.startswith(("6", "9")) else ("bj" if code.startswith("8") else "sz")
    url = f"https://qt.gtimg.cn/q={prefix}{code}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    vals = urllib.request.urlopen(req, timeout=10).read().decode("gbk").split('"')[1].split("~")
    price = float(vals[3])
    mcap = float(vals[44])
    pe_ttm = float(vals[39] or 0)
    pb = float(vals[46] or 0)
    name = vals[1]

    df = ths_eps_forecast(code)
    eps_cur = eps_next = None
    analyst_count = 0
    if not df.empty:
        try:
            eps_cur = float(df.iloc[0].iloc[2])
            analyst_count = int(df.iloc[0].iloc[1])
            if len(df) > 1:
                eps_next = float(df.iloc[1].iloc[2])
        except (ValueError, IndexError):
            pass

    pe_fwd = price / eps_cur if eps_cur and eps_cur > 0 else float("inf")
    cagr = (eps_next / eps_cur - 1) if (eps_cur and eps_next and eps_cur > 0) else 0
    peg = pe_fwd / (cagr * 100) if cagr > 0 else float("inf")
    digest = math.log(pe_fwd / 30) / math.log(1 + cagr) if pe_fwd > 30 and cagr > 0 else 0

    # 评级
    if peg != float("inf") and peg < 1:
        rating = "低估"
    elif peg != float("inf") and peg <= 1.5:
        rating = "合理"
    elif peg != float("inf") and peg <= 2:
        rating = "偏贵"
    else:
        rating = "不推荐(PEG>2)"

    return {
        "code": code, "name": name, "price": price, "mcap_yi": mcap,
        "pe_ttm": pe_ttm, "pb": pb,
        "eps_cur": eps_cur, "eps_next": eps_next,
        "pe_fwd": round(pe_fwd, 1) if eps_cur else None,
        "cagr_pct": round(cagr * 100, 1) if cagr else None,
        "peg": round(peg, 2) if peg != float("inf") else None,
        "digest_years": round(digest, 1),
        "analyst_count": analyst_count,
        "rating": rating,
    }
```

## 同业横向对比：peer_valuation(codes)

```python
def peer_valuation(codes: list[str]) -> pd.DataFrame:
    rows = []
    for c in codes:
        try:
            rows.append(full_valuation(c))
        except Exception as e:
            rows.append({"code": c, "error": str(e)})
    df = pd.DataFrame(rows)
    if "peg" in df.columns:
        df = df.sort_values("peg", na_position="last")
    return df


# AI-PCB 同业示例
peer_valuation(["002463", "002916", "600183", "688519"])
```

## 相对估值（可比公司法）

| 步骤 | 动作 |
|------|------|
| 1 | 确定同业池（同细分环节，非跨行业） |
| 2 | `peer_valuation()` 拉 PE_fwd / PEG |
| 3 | 目标 PEG < 同业中位数 → 板块内低估 |
| 4 | 增速需高于同业均值才值得溢价 |

## SOTP 简化（产业链标的）

对跨环节 conglomerate，按分部利润占比拆分：
- 分部 A 利润 × 分部 A 同业 PE × 权重
- 分部 B 利润 × 分部 B 同业 PE × 权重
- 加总 / 总股本 = 隐含股价

详见 `sector-rotation/references/supply-chain-map.md` 定位分部。

## 公式

见 `formulas.md`。
