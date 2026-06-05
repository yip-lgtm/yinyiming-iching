#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Threshold 對比測試：≥4 vs ≥5 vs ≥6
用真正 YinyimingIChing engine 重新跑美國段數據
"""
import pandas as pd
import sys
sys.path.insert(0, '/app/skills/yinyiming-iching')
from src.yinyiming_iching.iching import YinyimingIChing

US_SESSION = list(range(13, 22))


def run_backtest_with_threshold(price_df: pd.DataFrame, threshold: int):
    """用指定 threshold 跑 backtest"""
    results = []
    for _, row in price_df.iterrows():
        dt_str = row['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
        p = YinyimingIChing(dt_str)

        h = p.dt.hour
        if h not in US_SESSION:
            pred = 'HOLD'
        else:
            kl = p.analyze_key_lines()
            ww = max([l.get('weight', 0) for l in kl.values() if l.get('type') == '妻財'], default=0)
            bw = max([l.get('weight', 0) for l in kl.values() if l.get('type') == '兄弟'], default=0)

            if ww >= threshold and bw <= 5:
                pred = 'UP'
            elif bw >= threshold and ww <= 4:
                pred = 'DOWN'
            else:
                pred = 'HOLD'

        results.append({
            'timestamp': row['timestamp'],
            'prediction': pred,
        })
    return pd.DataFrame(results)


def analyze_results(res: pd.DataFrame, label: str, merged: pd.DataFrame):
    print(f"\n{'='*50}")
    print(f"  Threshold {label}")
    print(f"{'='*50}")
    print(res['prediction'].value_counts().to_string())

    us = res[res['timestamp'].dt.hour.isin(US_SESSION)].copy()
    us = us.merge(merged[['timestamp', 'actual']], on='timestamp', how='left')

    for pred_type in ['UP', 'DOWN', 'HOLD']:
        mask = us['prediction'] == pred_type
        t = mask.sum()
        c = (mask & (us['actual'] == pred_type)).sum()
        print(f"  {pred_type}: {c/t*100:.1f}% ({c}/{t})" if t > 0 else f"  {pred_type}: 0% (0/0)")

    total = len(us)
    correct = (us['prediction'] == us['actual']).sum()
    print(f"\n  整體 accuracy: {correct/total*100:.1f}%" if total > 0 else "")


if __name__ == '__main__':
    price_df = pd.read_csv('/home/node/.openclaw/workspace/btc_5m_1000plus.csv', parse_dates=['timestamp'])
    result_df = pd.read_csv('/home/node/.openclaw/workspace/btc_5m_backtest_results.csv', parse_dates=['timestamp'])
    merged = price_df.merge(result_df[['timestamp', 'actual']], on='timestamp', how='left')

    us_count = price_df['timestamp'].dt.hour.isin(US_SESSION).sum()
    print(f"美國段總數據量: {us_count} 筆 / {len(price_df)} 總筆\n")

    for thresh, label in [(4, '≥4'), (5, '≥5'), (6, '≥6')]:
        print(f"跑 threshold={label}...", end=" ", flush=True)
        res = run_backtest_with_threshold(price_df, thresh)
        merged_res = res.merge(merged[['timestamp', 'actual']], on='timestamp', how='left')
        analyze_results(merged_res, f"threshold={label}", merged)
        print()

    print("建議：threshold 越高 → 信號越少但越精（適合高風險策略）")
    print("建議：threshold 越低 → 信號越多但有機會更多假信號")
