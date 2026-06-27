#!/usr/bin/env python3
"""
板块/个股资金流向数据采集器 — 每日运行，存入本地 SQLite

可用数据源（2026-05 验证）:
  ✅ akshare stock_fund_flow_industry  (即时/3日/5日/10日/20日)  — 90 行业板块
  ✅ akshare stock_fund_flow_concept   (即时/3日/5日/10日/20日)  — 387 概念板块
  ✅ 新浪 MoneyFlow.ssl_bkzj_bk       (行业fenlei=1, 概念fenlei=0) — 备用源
  ❌ akshare stock_sector_fund_flow_hist     — 东方财富 push2his 被墙
  ❌ akshare stock_individual_fund_flow      — 同上
  ❌ akshare stock_individual_fund_flow_rank — 同上
  ❌ 新浪历史资金流接口 — 已废弃

策略: 每日快照存 SQLite，随时间积累历史数据。

用法:
  # 采集当日快照（所有维度）
  uv run --with "yfinance akshare requests" python3 fund_flow_collector.py

  # 仅采集行业板块
  uv run --with "yfinance akshare requests" python3 fund_flow_collector.py --industry-only

  # 查询历史数据
  uv run --with "yfinance akshare requests" python3 fund_flow_collector.py --query 半导体 --days 30

  # 导出 CSV
  uv run --with "yfinance akshare requests" python3 fund_flow_collector.py --export csv

Cron（每日收盘后 15:30 运行）:
  30 15 * * 1-5 cd <skill-root>/scripts && uv run --with "yfinance akshare requests" python3 fund_flow_collector.py >> /tmp/fund_flow.log 2>&1
"""

import argparse
import json
import os
import sqlite3
import sys
import warnings
from datetime import datetime, timedelta
from pathlib import Path

warnings.filterwarnings("ignore")

DB_DIR = Path(__file__).resolve().parents[3] / "data"
DB_PATH = DB_DIR / "fund_flow.db"


def get_db():
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sector_flow (
            date       TEXT NOT NULL,
            type       TEXT NOT NULL,       -- 'industry' or 'concept'
            period     TEXT NOT NULL,       -- '即时', '3日', '5日', '10日', '20日'
            name       TEXT NOT NULL,
            idx_value  REAL,
            change_pct REAL,
            inflow     REAL,               -- 亿
            outflow    REAL,               -- 亿
            net_flow   REAL,               -- 亿
            company_count INTEGER,
            lead_stock TEXT,
            source     TEXT DEFAULT 'akshare',
            created_at TEXT DEFAULT (datetime('now','localtime')),
            PRIMARY KEY (date, type, period, name)
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS stock_flow_snapshot (
            date       TEXT NOT NULL,
            code       TEXT NOT NULL,
            name       TEXT NOT NULL,
            price      REAL,
            change_pct REAL,
            net_flow   REAL,               -- 万
            main_flow  REAL,               -- 主力净流入(万)
            source     TEXT DEFAULT 'sina',
            created_at TEXT DEFAULT (datetime('now','localtime')),
            PRIMARY KEY (date, code)
        )
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_sector_name ON sector_flow(name, date)
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_stock_code ON stock_flow_snapshot(code, date)
    """)
    conn.commit()
    return conn


def collect_akshare_sectors(conn, today):
    """akshare 板块资金流向 (主数据源)"""
    import akshare as ak

    periods = ["即时", "3日排行", "5日排行", "10日排行", "20日排行"]
    period_labels = ["即时", "3日", "5日", "10日", "20日"]

    for func_name, stype in [
        ("stock_fund_flow_industry", "industry"),
        ("stock_fund_flow_concept", "concept"),
    ]:
        func = getattr(ak, func_name)
        for period, label in zip(periods, period_labels):
            try:
                df = func(symbol=period)
                rows = []
                for _, row in df.iterrows():
                    if period == "即时":
                        name = row["行业"]
                        idx_val = float(row.get("行业指数", 0) or 0)
                        chg = float(row.get("行业-涨跌幅", 0) or 0)
                        inf = float(row.get("流入资金", 0) or 0)
                        outf = float(row.get("流出资金", 0) or 0)
                        net = float(row.get("净额", 0) or 0)
                        cnt = int(row.get("公司家数", 0) or 0)
                        lead = row.get("领涨股", "")
                    else:
                        name = row["行业"]
                        idx_val = float(row.get("行业指数", 0) or 0)
                        chg_raw = row.get("阶段涨跌幅", "0")
                        chg = float(str(chg_raw).replace("%", "")) if chg_raw else 0
                        inf = float(row.get("流入资金", 0) or 0)
                        outf = float(row.get("流出资金", 0) or 0)
                        net = float(row.get("净额", 0) or 0)
                        cnt = int(row.get("公司家数", 0) or 0)
                        lead = ""

                    rows.append((today, stype, label, name, idx_val, chg, inf, outf, net, cnt, lead, "akshare"))

                conn.executemany(
                    "INSERT OR REPLACE INTO sector_flow VALUES (?,?,?,?,?,?,?,?,?,?,?,?,datetime('now','localtime'))",
                    rows,
                )
                conn.commit()
                print(f"  ✅ {func_name}({period}): {len(rows)} rows")
            except Exception as e:
                print(f"  ❌ {func_name}({period}): {e}")


def collect_sina_sectors(conn, today):
    """新浪板块资金流 (备用数据源，字段不同)"""
    import requests

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://vip.stock.finance.sina.com.cn/",
    }

    for fenlei, stype in [("1", "industry"), ("0", "concept")]:
        try:
            url = (
                f"https://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/"
                f"MoneyFlow.ssl_bkzj_bk?page=1&num=200&sort=netamount&asc=0&fenlei={fenlei}"
            )
            r = requests.get(url, headers=headers, timeout=15)
            data = json.loads(r.text)
            if not isinstance(data, list):
                print(f"  ❌ sina {stype}: unexpected response")
                continue

            rows = []
            for item in data:
                name = item.get("name", "")
                net = float(item.get("netamount", 0)) / 1e8
                inf = float(item.get("inamount", 0)) / 1e8
                outf = float(item.get("outamount", 0)) / 1e8
                chg = float(item.get("avg_changeratio", 0)) * 100
                lead = item.get("ts_name", "")
                rows.append((today, stype, "即时", name, 0, chg, inf, outf, net, 0, lead, "sina"))

            conn.executemany(
                "INSERT OR REPLACE INTO sector_flow VALUES (?,?,?,?,?,?,?,?,?,?,?,?,datetime('now','localtime'))",
                rows,
            )
            conn.commit()
            print(f"  ✅ sina {stype}: {len(rows)} rows")
        except Exception as e:
            print(f"  ❌ sina {stype}: {e}")


def collect_stock_snapshots(conn, today, tickers):
    """用 yfinance 采集关注个股的当日快照"""
    import yfinance as yf

    rows = []
    for code, (name, market, _tier) in tickers.items():
        suffix = ".SS" if market == "sh" else ".SZ"
        try:
            t = yf.Ticker(code + suffix)
            h = t.history(period="5d")
            if len(h) == 0:
                continue
            price = h["Close"].iloc[-1]
            chg = ((h["Close"].iloc[-1] / h["Close"].iloc[-2]) - 1) * 100 if len(h) >= 2 else 0
            rows.append((today, code, name, price, chg, 0, 0, "yfinance"))
        except Exception:
            pass

    if rows:
        conn.executemany(
            "INSERT OR REPLACE INTO stock_flow_snapshot VALUES (?,?,?,?,?,?,?,?,datetime('now','localtime'))",
            rows,
        )
        conn.commit()
    print(f"  ✅ stock snapshots: {len(rows)} stocks")


def backfill_stock_history(conn, tickers, days=30):
    """回填缺失交易日的个股行情数据（yfinance 支持历史回溯）"""
    import yfinance as yf

    cursor = conn.execute(
        "SELECT DISTINCT date FROM stock_flow_snapshot ORDER BY date"
    )
    existing_dates = {row[0] for row in cursor.fetchall()}

    period = f"{days}d"
    filled_count = 0
    sample_code = list(tickers.keys())[0]
    sample_market = tickers[sample_code][1]
    sample_suffix = ".SS" if sample_market == "sh" else ".SZ"
    sample_hist = yf.Ticker(sample_code + sample_suffix).history(period=period)
    if len(sample_hist) == 0:
        print("  ⚠️ 无法获取历史行情")
        return

    trading_dates = [d.strftime("%Y-%m-%d") for d in sample_hist.index]
    missing_dates = [d for d in trading_dates if d not in existing_dates]

    if not missing_dates:
        print(f"  ✅ 无缺失交易日（已有 {len(existing_dates)} 天）")
        return

    print(f"  发现 {len(missing_dates)} 个缺失交易日，开始回填...")

    for code, (name, market, _tier) in tickers.items():
        suffix = ".SS" if market == "sh" else ".SZ"
        try:
            t = yf.Ticker(code + suffix)
            h = t.history(period=period)
            if len(h) < 2:
                continue
            rows = []
            for i in range(1, len(h)):
                date_str = h.index[i].strftime("%Y-%m-%d")
                if date_str not in missing_dates:
                    continue
                price = h["Close"].iloc[i]
                chg = ((h["Close"].iloc[i] / h["Close"].iloc[i - 1]) - 1) * 100
                rows.append((date_str, code, name, price, chg, 0, 0, "yfinance-backfill"))
            if rows:
                conn.executemany(
                    "INSERT OR IGNORE INTO stock_flow_snapshot VALUES (?,?,?,?,?,?,?,?,datetime('now','localtime'))",
                    rows,
                )
                filled_count += len(rows)
        except Exception:
            pass

    conn.commit()
    print(f"  ✅ 回填完成: {filled_count} 条记录, 覆盖 {len(missing_dates)} 个交易日")
    print(f"  ⚠️ 板块资金流无法回填（接口仅提供实时快照）")


def query_history(conn, keyword, days=30):
    """查询某板块/概念的历史资金流"""
    cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    cursor = conn.execute(
        """
        SELECT date, type, period, name, net_flow, change_pct, lead_stock
        FROM sector_flow
        WHERE name LIKE ? AND period='即时' AND date >= ?
        ORDER BY date DESC
        """,
        (f"%{keyword}%", cutoff),
    )
    rows = cursor.fetchall()
    if not rows:
        print(f"未找到 '{keyword}' 的历史数据（{days}天内）。")
        print(f"数据库位置: {DB_PATH}")
        print("提示: 需要每日运行采集后才有历史数据积累。")
        return

    print(f"\n{'日期':<12} {'类型':<10} {'板块':<12} {'净流入(亿)':>10} {'涨跌%':>7} {'领涨股':<10}")
    print("-" * 65)
    for row in rows:
        date, stype, _period, name, net, chg, lead = row
        print(f"{date:<12} {stype:<10} {name:<12} {net:>+9.2f} {chg:>+6.2f}% {lead or '':<10}")

    if len(rows) >= 2:
        nets = [r[4] for r in rows]
        avg_net = sum(nets) / len(nets)
        print(f"\n平均日净流入: {avg_net:+.2f}亿 (共{len(rows)}天数据)")
        consecutive_in = sum(1 for n in nets if n > 0)
        print(f"净流入天数: {consecutive_in}/{len(rows)} ({consecutive_in/len(rows)*100:.0f}%)")


def export_data(conn, fmt="csv"):
    """导出全部数据"""
    import csv
    from io import StringIO

    out_dir = DB_DIR / "exports"
    out_dir.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M")

    cursor = conn.execute("SELECT * FROM sector_flow ORDER BY date DESC, type, period, name")
    rows = cursor.fetchall()
    cols = [desc[0] for desc in cursor.description]

    if fmt == "csv":
        path = out_dir / f"sector_flow_{ts}.csv"
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f)
            w.writerow(cols)
            w.writerows(rows)
        print(f"✅ 导出 {len(rows)} 行 → {path}")
    elif fmt == "json":
        path = out_dir / f"sector_flow_{ts}.json"
        data = [dict(zip(cols, row)) for row in rows]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ 导出 {len(rows)} 行 → {path}")


def show_stats(conn):
    """显示数据库统计信息"""
    cursor = conn.execute("SELECT COUNT(*), MIN(date), MAX(date) FROM sector_flow")
    total, min_date, max_date = cursor.fetchone()
    cursor2 = conn.execute("SELECT COUNT(DISTINCT date) FROM sector_flow")
    days = cursor2.fetchone()[0]
    cursor3 = conn.execute("SELECT COUNT(*) FROM stock_flow_snapshot")
    stock_rows = cursor3.fetchone()[0]

    print(f"\n📊 数据库统计:")
    print(f"  位置: {DB_PATH}")
    print(f"  大小: {DB_PATH.stat().st_size / 1024:.0f} KB" if DB_PATH.exists() else "  (新建)")
    print(f"  板块资金流: {total} 条, {days} 天 ({min_date or 'N/A'} ~ {max_date or 'N/A'})")
    print(f"  个股快照: {stock_rows} 条")


def main():
    sys.path.insert(0, str(Path(__file__).parent))
    from weekly_scan import AI_CHAIN_TICKERS

    parser = argparse.ArgumentParser(description="板块资金流向数据采集器")
    parser.add_argument("--industry-only", action="store_true", help="仅采集行业板块")
    parser.add_argument("--query", type=str, help="查询某板块历史 (如: 半导体)")
    parser.add_argument("--days", type=int, default=30, help="查询天数 (默认30)")
    parser.add_argument("--export", choices=["csv", "json"], help="导出数据")
    parser.add_argument("--stats", action="store_true", help="显示数据库统计")
    parser.add_argument("--no-stock", action="store_true", help="跳过个股快照采集")
    parser.add_argument("--backfill", type=int, metavar="DAYS", help="回填最近N天的个股行情 (如: --backfill 30)")
    args = parser.parse_args()

    conn = get_db()

    if args.query:
        query_history(conn, args.query, args.days)
        conn.close()
        return

    if args.export:
        export_data(conn, args.export)
        conn.close()
        return

    if args.stats:
        show_stats(conn)
        conn.close()
        return

    today = datetime.now().strftime("%Y-%m-%d")
    print(f"📡 资金流向数据采集 — {today}")

    print("\n[1/4] akshare 板块资金流向...")
    collect_akshare_sectors(conn, today)

    if not args.industry_only:
        print("\n[2/4] 新浪板块资金流 (备用源)...")
        collect_sina_sectors(conn, today)

    if not args.no_stock:
        print("\n[3/4] 个股行情快照...")
        collect_stock_snapshots(conn, today, AI_CHAIN_TICKERS)

    backfill_days = args.backfill or 30
    print(f"\n[4/4] 回填缺失交易日 (最近{backfill_days}天)...")
    backfill_stock_history(conn, AI_CHAIN_TICKERS, days=backfill_days)

    show_stats(conn)
    conn.close()
    print("\n采集完成。")


if __name__ == "__main__":
    main()
