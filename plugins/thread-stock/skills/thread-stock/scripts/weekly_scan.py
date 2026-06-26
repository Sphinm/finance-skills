#!/usr/bin/env python3
"""
AI 产业链周度扫描脚本

数据源:
  - akshare: 行业资金流向、财务指标
  - yfinance: 行情数据（价格、均线、RSI、成交量）

用法:
  uv run --with "yfinance akshare" python3 weekly_scan.py
  uv run --with "yfinance akshare" python3 weekly_scan.py --holdings 600487,002463
  uv run --with "yfinance akshare" python3 weekly_scan.py --sector-only
"""

import argparse
import sys
import warnings
from datetime import datetime
from pathlib import Path

warnings.filterwarnings("ignore")

AI_CHAIN_TICKERS = {
    "600183": ("生益科技", "sh", "Tier1-CCL"),
    "688519": ("南亚新材", "sh", "Tier1-CCL"),
    "600487": ("亨通光电", "sh", "Tier1-光纤"),
    "600522": ("中天科技", "sh", "Tier1-光纤"),
    "601869": ("长飞光纤", "sh", "Tier1-光纤"),
    "002463": ("沪电股份", "sz", "Tier2-PCB"),
    "002916": ("深南电路", "sz", "Tier2-PCB"),
    "603986": ("兆易创新", "sh", "Tier2-存储"),
    "688008": ("澜起科技", "sh", "Tier2-存储接口"),
    "688809": ("强一股份", "sh", "Tier2-探针卡"),
    "300308": ("中际旭创", "sz", "Tier2-光模块"),
    "300502": ("新易盛", "sz", "Tier2-光模块"),
    "002281": ("光迅科技", "sz", "Tier2-光模块"),
    "688012": ("中微公司", "sh", "Tier3-设备"),
    "002371": ("北方华创", "sz", "Tier3-设备"),
    "688072": ("拓荆科技", "sh", "Tier3-设备"),
    "300604": ("长川科技", "sz", "Tier3-设备"),
    "002475": ("立讯精密", "sz", "Tier3.5-连接器"),
    "688800": ("瑞可达", "sh", "Tier3.5-连接器"),
    "002851": ("麦格米特", "sz", "Tier3.5-电源"),
    "002837": ("英维克", "sz", "Tier3.5-液冷"),
    "300499": ("高澜股份", "sz", "Tier3.5-液冷"),
    "603019": ("中科曙光", "sh", "Tier4-集成"),
    "688041": ("海光信息", "sh", "Tier4-芯片"),
    "000977": ("浪潮信息", "sz", "Tier4-集成"),
    "688256": ("寒武纪", "sh", "Tier4-芯片"),
}


def _load_history(sector_name, days=5):
    """从本地 SQLite 加载板块历史资金流"""
    import sqlite3
    from datetime import timedelta

    db_path = Path(__file__).parent.parent / "data" / "fund_flow.db"
    if not db_path.exists():
        return None
    try:
        conn = sqlite3.connect(str(db_path))
        cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        cursor = conn.execute(
            "SELECT date, net_flow, change_pct FROM sector_flow "
            "WHERE name=? AND type='industry' AND period='即时' AND date>=? "
            "ORDER BY date",
            (sector_name, cutoff),
        )
        rows = cursor.fetchall()
        conn.close()
        return rows if rows else None
    except Exception:
        return None


def scan_sector_flows():
    """拉取行业资金流向 Top 10 + 本地历史对比"""
    import akshare as ak

    print("=" * 60)
    print("【板块资金流向】")
    print("=" * 60)

    try:
        df = ak.stock_fund_flow_industry(symbol="即时")
        df["净额"] = df["净额"].astype(float)
        top10 = df.head(10)
        print(f"\n净流入 Top 10 板块:")
        print(f"{'序号':<4} {'板块':<10} {'净流入(亿)':<10} {'涨跌幅%':<8} {'领涨股':<10} {'历史趋势':<12}")
        print("-" * 65)
        for _, row in top10.iterrows():
            name = row["行业"]
            net = float(row["净额"])
            hist = _load_history(name, days=7)
            trend_str = ""
            if hist and len(hist) >= 2:
                nets = [h[1] for h in hist]
                avg = sum(nets) / len(nets)
                in_days = sum(1 for n in nets if n > 0)
                if net > avg * 1.5:
                    trend_str = f"🔥加速({in_days}/{len(nets)}日入)"
                elif in_days >= len(nets) * 0.7:
                    trend_str = f"📈持续({in_days}/{len(nets)}日入)"
                elif net < 0 and avg > 0:
                    trend_str = "⚠️转出"
                else:
                    trend_str = f"({in_days}/{len(nets)}日入)"
            print(
                f"{row['序号']:<4} {name:<10} "
                f"{net:>+8.2f}  "
                f"{float(row['行业-涨跌幅']):>+6.2f}%  "
                f"{row['领涨股']:<10} {trend_str}"
            )

        semi_row = df[df["行业"].str.contains("半导体")]
        if len(semi_row) > 0:
            r = semi_row.iloc[0]
            net_val = float(r["净额"])
            msg = f"\n半导体板块: 排名第{r['序号']}, 净流入{net_val:+.2f}亿, 涨跌{float(r['行业-涨跌幅']):+.2f}%"
            hist = _load_history("半导体", days=10)
            if hist and len(hist) >= 2:
                nets = [h[1] for h in hist]
                msg += f" | 近{len(nets)}天均值{sum(nets)/len(nets):+.1f}亿"
            print(msg)
    except Exception as e:
        print(f"  ⚠️ akshare 行业资金流获取失败: {e}")
        print("  → 请手动查看: https://data.eastmoney.com/bkzj/hy.html")


def scan_stocks(holdings=None):
    """对 AI 产业链标的进行全面扫描"""
    import yfinance as yf

    print("\n" + "=" * 60)
    print("【个股扫描】")
    print("=" * 60)

    results = []

    for code, (name, market, tier) in AI_CHAIN_TICKERS.items():
        suffix = ".SS" if market == "sh" else ".SZ"
        ticker = code + suffix
        try:
            t = yf.Ticker(ticker)
            h = t.history(period="3mo")
            if len(h) < 20:
                continue
            c = h["Close"]
            price = c.iloc[-1]

            ma5 = c.rolling(5).mean().iloc[-1]
            ma10 = c.rolling(10).mean().iloc[-1]
            ma20 = c.rolling(20).mean().iloc[-1]

            delta = c.diff()
            gain = delta.where(delta > 0, 0).rolling(14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
            rs = gain / loss
            rsi = float((100 - 100 / (1 + rs)).iloc[-1])

            avg20 = h["Volume"].tail(20).mean()
            vol_ratio = h["Volume"].iloc[-1] / avg20 if avg20 > 0 else 0

            chg5 = (c.iloc[-1] / c.iloc[-6] - 1) * 100 if len(c) >= 6 else 0
            chg20 = (c.iloc[-1] / c.iloc[-21] - 1) * 100 if len(c) >= 21 else 0

            dev_ma20 = (price / ma20 - 1) * 100

            info = t.info or {}
            fwd_pe = info.get("forwardPE", None)
            rev_growth = info.get("revenueGrowth", None)
            earn_growth = info.get("earningsGrowth", None)
            profit_margin = info.get("profitMargins", None)

            leverage = None
            if rev_growth and earn_growth and rev_growth > 0:
                leverage = earn_growth / rev_growth

            peg = None
            if fwd_pe and earn_growth and earn_growth > 0:
                peg = fwd_pe / (earn_growth * 100)

            signals = []
            if rsi > 80:
                signals.append("🔴RSI>80")
            elif rsi > 70:
                signals.append("🟡RSI>70")
            if abs(dev_ma20) < 5 and 40 < rsi < 60:
                signals.append("🟢回踩区")
            if vol_ratio > 2:
                signals.append("⚡放量")

            is_holding = holdings and code in holdings

            results.append({
                "code": code,
                "name": name,
                "tier": tier,
                "price": price,
                "rsi": rsi,
                "dev_ma20": dev_ma20,
                "vol_ratio": vol_ratio,
                "chg5": chg5,
                "chg20": chg20,
                "fwd_pe": fwd_pe,
                "leverage": leverage,
                "peg": peg,
                "profit_margin": profit_margin,
                "signals": signals,
                "is_holding": is_holding,
            })
        except Exception:
            pass

    results.sort(key=lambda x: x.get("peg") or 999)

    # Print overview
    print(f"\n{'名称':<8} {'层级':<12} {'价格':>7} {'RSI':>5} {'距MA20':>7} {'5日%':>6} {'20日%':>7} {'PEG':>6} {'杠杆比':>6} {'信号':<15}")
    print("-" * 95)
    for r in results:
        peg_str = f"{r['peg']:.2f}" if r['peg'] else "  N/A"
        lev_str = f"{r['leverage']:.1f}x" if r['leverage'] else " N/A"
        sig_str = " ".join(r["signals"]) if r["signals"] else ""
        hold_mark = "★" if r["is_holding"] else " "
        print(
            f"{hold_mark}{r['name']:<7} {r['tier']:<12} "
            f"{r['price']:>7.2f} {r['rsi']:>5.1f} {r['dev_ma20']:>+6.1f}% "
            f"{r['chg5']:>+5.1f}% {r['chg20']:>+6.1f}% "
            f"{peg_str:>6} {lev_str:>6} {sig_str}"
        )

    # === 分层候选输出 ===
    print("\n" + "=" * 60)
    print("【短线候选】量价异动 + 动量 (3-5天)")
    print("  条件: 量比≥1.5 + 5日涨5~15% + RSI 50-75")
    print("=" * 60)
    swing = [
        r for r in results
        if r["vol_ratio"] >= 1.5
        and 5 <= r["chg5"] <= 15
        and 50 < r["rsi"] < 75
    ]
    if swing:
        for r in swing:
            print(
                f"  ⚡ {r['name']}({r['code']}) "
                f"量比={r['vol_ratio']:.1f} 5日{r['chg5']:+.1f}% "
                f"RSI={r['rsi']:.0f} 距MA20={r['dev_ma20']:+.1f}%"
            )
    else:
        print("  暂无满足条件的短线标的。")

    print("\n" + "=" * 60)
    print("【中线候选】四层漏斗 + 回踩均线 (2周-3月)")
    print("  条件: PEG<1 + RSI 40-65 + 距MA20<+10% + 经营杠杆>1")
    print("=" * 60)
    position = [
        r for r in results
        if r.get("peg") and r["peg"] < 1.0
        and 40 < r["rsi"] < 65
        and r["dev_ma20"] < 10
    ]
    if position:
        for r in position:
            lev = f"{r['leverage']:.1f}x" if r.get("leverage") else "N/A"
            flag = " ⚠️杠杆<1" if r.get("leverage") and r["leverage"] < 1.0 else ""
            print(
                f"  ✅ {r['name']}({r['code']}) "
                f"PEG={r['peg']:.2f} 杠杆={lev} "
                f"RSI={r['rsi']:.0f} 距MA20={r['dev_ma20']:+.1f}%{flag}"
            )
    else:
        print("  暂无满足全部条件的中线候选。")

    print("\n" + "=" * 60)
    print("【长线候选】产业周期 + 深度低估 (3月-1年)")
    print("  条件: PEG<0.5 + 利润率>10% + 杠杆>1.5 + Tier1/2")
    print("=" * 60)
    trend = [
        r for r in results
        if r.get("peg") and r["peg"] < 0.5
        and r.get("profit_margin") and r["profit_margin"] > 0.10
        and r.get("leverage") and r["leverage"] > 1.5
        and r["tier"].startswith(("Tier1", "Tier2"))
    ]
    if trend:
        for r in trend:
            print(
                f"  💎 {r['name']}({r['code']}) "
                f"PEG={r['peg']:.2f} 利润率={r['profit_margin']*100:.1f}% "
                f"杠杆={r['leverage']:.1f}x RSI={r['rsi']:.0f} "
                f"[{r['tier']}]"
            )
    else:
        low_peg_tier12 = [
            r for r in results
            if r.get("peg") and r["peg"] < 0.5
            and r["tier"].startswith(("Tier1", "Tier2"))
        ]
        if low_peg_tier12:
            print("  暂无全部满足，以下接近条件:")
            for r in low_peg_tier12:
                pm = f"{r['profit_margin']*100:.1f}%" if r.get("profit_margin") else "N/A"
                lev = f"{r['leverage']:.1f}x" if r.get("leverage") else "N/A"
                print(
                    f"  🔸 {r['name']}({r['code']}) "
                    f"PEG={r['peg']:.2f} 利润率={pm} 杠杆={lev} [{r['tier']}]"
                )
        else:
            print("  暂无。")

    # Overbought warnings
    print("\n" + "=" * 60)
    print("【超买预警】RSI > 70 — 三种周期都不追")
    print("=" * 60)
    overbought = [r for r in results if r["rsi"] > 70]
    if overbought:
        for r in overbought:
            hold_mark = " ★持仓" if r["is_holding"] else ""
            print(
                f"  ⚠️ {r['name']}({r['code']}) "
                f"RSI={r['rsi']:.0f} 距MA20={r['dev_ma20']:+.1f}% "
                f"20日{r['chg20']:+.1f}%{hold_mark}"
            )
    else:
        print("  无超买标的。")

    # Holdings health check
    if holdings:
        print("\n" + "=" * 60)
        print("【持仓健康检查】")
        print("=" * 60)
        for r in results:
            if not r["is_holding"]:
                continue
            status = "🟢健康"
            if r["rsi"] > 80:
                status = "🔴严重超买"
            elif r["rsi"] > 70:
                status = "🟡超买预警"
            elif r["rsi"] < 30:
                status = "🟡超卖"

            print(
                f"  {r['name']}({r['code']}): {status} "
                f"| RSI={r['rsi']:.0f} | 距MA20={r['dev_ma20']:+.1f}% "
                f"| 5日{r['chg5']:+.1f}% | 量比={r['vol_ratio']:.2f}"
            )

    return results


def main():
    parser = argparse.ArgumentParser(description="AI产业链周度扫描")
    parser.add_argument(
        "--holdings", type=str, default=None,
        help="持仓代码，逗号分隔 (如: 600487,002463)"
    )
    parser.add_argument(
        "--sector-only", action="store_true",
        help="仅扫描板块资金流向"
    )
    args = parser.parse_args()

    print(f"📊 AI产业链周度扫描 — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print()

    scan_sector_flows()

    if not args.sector_only:
        holdings = set(args.holdings.split(",")) if args.holdings else None
        scan_stocks(holdings=holdings)

    print(f"\n{'='*60}")
    print("扫描完成。详细分析请结合 screening-workflow.md 执行。")


if __name__ == "__main__":
    main()
