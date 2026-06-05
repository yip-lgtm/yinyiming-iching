---
name: yinyiming-iching
description: "易經六爻卦爻 BTC 5m 預測：輸入時間，輸出卦象、動爻、納音、合沖、Polymarket 方向建議"
metadata:
  homepage: https://github.com/yip-lgtm/yinyiming-iching
  license: MIT
  user-invocable: true
allowed-tools:
  - read
  - write
  - exec
---

# 隱姓埋名易經卦爻 BTC 5m 預測

接收時間，執行易經六爻起卦 + 盲派分輕重 + 納音合沖分析，輸出 Polymarket BTC 5m 方向建議。

## 使用方式

輸入格式（自然語言或結構化）：

```
時間：2026-06-05 15:30:00
時區：Asia/Hong_Kong
```

或直接給我時間，我幫你翻：

```
幫我睇下聽聽3點半BTC點行
宜家BTC卦象
```

## 分析維度

1. **卦爻** — 六爻陰陽（初爻到上爻）
2. **動爻** — 哪些爻在動（决定力量傳遞）
3. **納音** — 時柱/日柱納音五行
4. **合沖** — 有合有沖 = 波動；合沖兑現 = 大行情
5. **關鍵爻** — 分輕重（位置 × 動 × 納音旺衰 × 對用神影響）
6. **預測方向** — UP / DOWN / VOLATILE，信心%，Polymarket 建議

## 實戰邏輯

- **妻財動 + 得令** → UP（資金流入）
- **兄弟動 + 強旺** → DOWN（搶奪力強）
- **合必求開** — 合局被沖開之時是轉機
- **納音加持** — 見玄真老師方法

## 依賴

```bash
pip3 install --break-system-packages sxtwl pendulum streamlit pandas numpy
```

本地已安裝，無需額外操作。

## 調用方式

```python
import sys
sys.path.insert(0, '/app/skills/yinyiming-iching')
from src.yinyiming_iching.iching import YinyimingIChing

dt = "2026-06-05 15:30:00"  # HKT
 predictor = YinyimingIChing(dt)
 result = predictor.predict_btc_5m()
```
