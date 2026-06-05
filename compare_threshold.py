#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Threshold 對比測試：≥4 vs ≥5
用真正 YinyimingIChing engine 重新跑美國段數據
"""
import pandas as pd
import sys
sys.path.insert(0, '/app/skills/yinyiming-iching')
from src.yinyiming_iching.iching import YinyimingIChing
from src.yinyiming_iching.backtest import Backtester

US_SESSION = list(range(13, 22))
DATA_PATH = '/home/node/.openclaw/workspace/btc_5m_1000plus.csv'

def run_backtest_with_threshold(df: pd.DataFrame, threshold: int):
    """用指定 threshold 跑 backtest"""
    from src.yinyiming_iching.backtest import Backtester

    class ThresholdWrapper:
        def __init__(self, thresh):
            self.thresh = thresh
        def predict(self, dt_str: str) -> dict:
            p = YinyimingIChing(dt_str)
            r = p.predict_btc_5m()
            h = r.get('current_hour_utc', r.get('hour', p.dt.hour))
            if h not in US_SESSION:
                return {'direction': 'HOLD', 'confidence': 20}
            ww = 0
            bw = 0
            for l in r.get('key_lines_analysis', {}).values():
                if l.get('type') == '妻財':
                    ww = max(ww, l.get('weight', 0))
                elif l.get('type') == '兄弟':
                    bw = max(bw, l.get('weight', 0))
            if ww >= self.thresh and bw <= 5:
                conf = min(52 + (ww - 4) * 5, 80)
                return {'direction': 'UP', 'confidence': conf}
            elif bw >= self.thresh and ww <= 4:
                return {'direction': 'DOWN', 'confidence': min(48 + (bw - 5) * 5, 75)}
            return {'direction': 'HOLD', 'confidence': 40}

    results = []
    for _, row in df.iterrows():
        dt_str = row['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
        pred = ThresholdWrapper(threshold).predict(dt_str)
        change = 0.0
        if 'actual_change_pct' in df.columns:
            change = row.get('actual_change_pct', 0.0)
        results.append({
            'timestamp': row['timestamp'],
            'prediction': pred['direction'],
            'confidence': pred['confidence'],
            'actual_change_pct': change,
        })
    return pd.DataFrame(results)


def analyze_results(res: pd.DataFrame, label: str):
    print(f"\n{'='*50}")
    print(f"  Threshold {label}")
    print(f"{'='*50}")
    print(res['prediction'].value_counts().to_string())

    us = res[res['timestamp'].dt.hour.isin(US_SESSION)]
    for pred in ['UP', 'DOWN', 'HOLD']:
        t = (us['prediction'] == pred).sum()
        c = ((us['prediction'] == pred) & (us['actual'] == pred)).sum()
        if t > 0:
            print(f"  {pred}: {c/t*100:.1f}% ({c}/{t})")

    total = len(res)
    correct = (res['prediction'] == res['actual']).sum()
    print(f"\n  整體 accuracy: {correct/total*100:.1f}%")


if __name__ == '__main__':
    df = pd.read_csv(DATA_PATH)
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    print("用真正 engine 跑，請稍候...")
    for thresh, label in [(4, '≥4'), (5, '≥5'), (6, '≥6')]:
        res = run_backtest_with_threshold(df, thresh)
        analyze_results(res, f"threshold={label}")

    print("\n\n建議：threshold 越高 → 信號越少但越精（適合高風險策略）")
    print("建議：threshold 越低 → 信號越多但有機會出現更多假信號")
