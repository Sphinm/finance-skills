"""找资金持续建仓但涨幅温和的板块和个股"""
import akshare as ak
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

pd.set_option('display.unicode.east_asian_width', True)

print('='*60)
print('【概念板块】连续多日净流入 + 涨幅温和 = 资金暗中建仓')
print('='*60)

df_1d = ak.stock_fund_flow_concept(symbol='即时')
df_3d = ak.stock_fund_flow_concept(symbol='3日排行')
df_5d = ak.stock_fund_flow_concept(symbol='5日排行')
df_10d = ak.stock_fund_flow_concept(symbol='10日排行')

for df in [df_1d, df_3d, df_5d, df_10d]:
    df.columns = [c.strip() for c in df.columns]

cols_1d = df_1d.columns.tolist()
cols_10d = df_10d.columns.tolist()

merged = df_1d[[cols_1d[0], cols_1d[2], cols_1d[3]]].merge(
    df_10d[[cols_10d[0], cols_10d[2], cols_10d[3]]],
    on=cols_1d[0], suffixes=('_1d', '_10d')
)
merged.columns = ['板块', '今日净流入', '今日涨幅', '10日净流入', '10日涨幅']

for c in ['今日净流入', '今日涨幅', '10日净流入', '10日涨幅']:
    merged[c] = pd.to_numeric(merged[c], errors='coerce')

building = merged[
    (merged['10日净流入'] > 0) &
    (merged['今日净流入'] > 0) &
    (merged['10日涨幅'] < 15) &
    (merged['10日涨幅'] > 0)
].sort_values('10日净流入', ascending=False).head(20)

print(f'\n筛选: 10日净流入>0 + 今日净流入>0 + 10日涨幅<15%')
print(f'{"板块":<14} {"今日流入(亿)":>10} {"今日涨%":>8} {"10日流入(亿)":>10} {"10日涨%":>8}')
print('-'*60)
for _, row in building.iterrows():
    print(f'{row["板块"]:<14} {row["今日净流入"]:>+10.2f} {row["今日涨幅"]:>+8.2f} {row["10日净流入"]:>+10.2f} {row["10日涨幅"]:>+8.2f}')

# 同样看行业板块
print('\n')
print('='*60)
print('【行业板块】连续多日净流入 + 涨幅温和')
print('='*60)

df_ind_1d = ak.stock_fund_flow_industry(symbol='即时')
df_ind_10d = ak.stock_fund_flow_industry(symbol='10日排行')

for df in [df_ind_1d, df_ind_10d]:
    df.columns = [c.strip() for c in df.columns]

cols_i1 = df_ind_1d.columns.tolist()
cols_i10 = df_ind_10d.columns.tolist()

merged_ind = df_ind_1d[[cols_i1[0], cols_i1[2], cols_i1[3]]].merge(
    df_ind_10d[[cols_i10[0], cols_i10[2], cols_i10[3]]],
    on=cols_i1[0], suffixes=('_1d', '_10d')
)
merged_ind.columns = ['板块', '今日净流入', '今日涨幅', '10日净流入', '10日涨幅']

for c in ['今日净流入', '今日涨幅', '10日净流入', '10日涨幅']:
    merged_ind[c] = pd.to_numeric(merged_ind[c], errors='coerce')

building_ind = merged_ind[
    (merged_ind['10日净流入'] > 0) &
    (merged_ind['今日净流入'] > 0) &
    (merged_ind['10日涨幅'] < 15) &
    (merged_ind['10日涨幅'] > 0)
].sort_values('10日净流入', ascending=False).head(15)

print(f'\n{"板块":<14} {"今日流入(亿)":>10} {"今日涨%":>8} {"10日流入(亿)":>10} {"10日涨%":>8}')
print('-'*60)
for _, row in building_ind.iterrows():
    print(f'{row["板块"]:<14} {row["今日净流入"]:>+10.2f} {row["今日涨幅"]:>+8.2f} {row["10日净流入"]:>+10.2f} {row["10日涨幅"]:>+8.2f}')

# 从建仓板块中选出领涨股，获取个股数据
print('\n')
print('='*60)
print('【潜力个股】从建仓板块中挖掘')
print('='*60)

# 手动选几个有意思的方向的代表个股进行扫描
# 根据板块结果动态选取
potential_tickers = {
    # 军工电子（今日+14.9亿，持续流入）
    '600562': '国睿科技',
    '688002': '睿创微纳',
    '600760': '中航沈飞',
    '000768': '中航西飞',
    # 小金属/稀土（+45亿，新能源+军工双驱动）
    '600111': '北方稀土',
    '600259': '广晟有色',
    '002460': '赣锋锂业',
    # 金属新材料
    '688122': '西部超导',
    '688981': '中芯国际',
    # 电子化学品
    '300236': '上海新阳',
    '688396': '华润微',
    # 通信设备（未在AI链主池的）
    '002396': '星网锐捷',
    '300602': '飞荣达',
    # 光伏/储能（可能资金暗中布局）
    '002129': '中环股份',  # TCL中环
    '300274': '阳光电源',
    # 机器人（新方向）
    '300124': '汇川技术',
    '688169': '石头科技',
    '002747': '埃斯顿',
}

print(f'\n扫描 {len(potential_tickers)} 只潜力标的...\n')
print(f'{"名称":<10} {"代码":<8} {"价格":>8} {"RSI":>5} {"距MA20":>8} {"5日%":>7} {"20日%":>7} {"信号"}')
print('-'*70)

import numpy as np

def calc_rsi(prices, period=14):
    delta = prices.diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

results = []
for code, name in potential_tickers.items():
    try:
        suffix = '.SS' if code.startswith('6') else '.SZ'
        ticker = code + suffix
        data = yf.download(ticker, period='60d', progress=False)
        if data.empty or len(data) < 20:
            continue
        close = data['Close'].squeeze()
        price = close.iloc[-1]
        ma20 = close.rolling(20).mean().iloc[-1]
        ma5 = close.rolling(5).mean().iloc[-1]
        rsi = calc_rsi(close).iloc[-1]
        dev_ma20 = (price - ma20) / ma20 * 100
        chg5 = (price / close.iloc[-6] - 1) * 100 if len(close) > 5 else 0
        chg20 = (price / close.iloc[-21] - 1) * 100 if len(close) > 20 else 0
        
        vol_recent = data['Volume'].squeeze().iloc[-5:].mean()
        vol_prev = data['Volume'].squeeze().iloc[-20:-5].mean()
        vol_ratio = vol_recent / vol_prev if vol_prev > 0 else 1
        
        signal = ''
        if rsi > 75:
            signal = '⚠️超买'
        elif rsi < 35:
            signal = '🔵超卖'
        elif 38 <= rsi <= 55 and -5 <= dev_ma20 <= 3 and vol_ratio > 1.2:
            signal = '🟢建仓信号'
        elif 38 <= rsi <= 60 and -5 <= dev_ma20 <= 5:
            signal = '🟡回踩蓄力'
        elif rsi > 65 and dev_ma20 > 10:
            signal = '🟡偏高'
        
        results.append({
            'name': name, 'code': code, 'price': price,
            'rsi': rsi, 'dev_ma20': dev_ma20, 'chg5': chg5,
            'chg20': chg20, 'vol_ratio': vol_ratio, 'signal': signal
        })
        
        print(f'{name:<10} {code:<8} {price:>8.2f} {rsi:>5.1f} {dev_ma20:>+7.1f}% {chg5:>+6.1f}% {chg20:>+6.1f}% {signal}')
    except Exception as e:
        pass

# 筛选建仓特征的
print('\n')
print('='*60)
print('【精选】建仓信号明确的标的（RSI 38-55 + 贴MA20 + 放量）')
print('='*60)
acc = [r for r in results if '建仓' in r['signal'] or ('回踩' in r['signal'] and r['vol_ratio'] > 1.1)]
if acc:
    print(f'\n{"名称":<10} {"代码":<8} {"RSI":>5} {"距MA20":>8} {"5日%":>7} {"量比":>6} {"信号"}')
    print('-'*60)
    for r in sorted(acc, key=lambda x: x['vol_ratio'], reverse=True):
        print(f'{r["name"]:<10} {r["code"]:<8} {r["rsi"]:>5.1f} {r["dev_ma20"]:>+7.1f}% {r["chg5"]:>+6.1f}% {r["vol_ratio"]:>5.2f}x {r["signal"]}')
else:
    print('  暂无完美匹配。')
    print('\n  接近条件的:')
    near = [r for r in results if 38 <= r['rsi'] <= 60 and -8 <= r['dev_ma20'] <= 8]
    for r in sorted(near, key=lambda x: abs(x['dev_ma20'])):
        print(f'  {r["name"]:<10} {r["code"]:<8} RSI={r["rsi"]:.0f} 距MA20={r["dev_ma20"]:+.1f}% 5日{r["chg5"]:+.1f}% 量比{r["vol_ratio"]:.2f}x')
