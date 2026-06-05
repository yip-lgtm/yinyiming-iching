#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
隱姓埋名易經卦爻 核心 engine v2.0
梅花易數 + sxtwl精確八字 + 盲派納音 + 妻財兄弟分析
專為 Polymarket BTC 5m UP/DOWN 設計
"""

from datetime import datetime
from typing import Dict, List, Any

import sxtwl

# ============================================================
# 常數
# ============================================================

GAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
ZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

NAYIN_MAP = {
    "甲子": "海中金", "乙丑": "海中金",
    "丙寅": "爐中火", "丁卯": "爐中火",
    "戊辰": "大林木", "己巳": "大林木",
    "庚午": "路旁土", "辛未": "路旁土",
    "壬申": "劍鋒金", "癸酉": "劍鋒金",
    "甲戌": "山頭火", "乙亥": "山頭火",
    "丙子": "澗下水", "丁丑": "澗下水",
    "戊寅": "城頭土", "己卯": "城頭土",
    "庚辰": "白蠟金", "辛巳": "白蠟金",
    "壬午": "楊柳木", "癸未": "楊柳木",
    "甲申": "泉中水", "乙酉": "泉中水",
    "丙戌": "屋上土", "丁亥": "屋上土",
    "戊子": "霹靂火", "己丑": "霹靂火",
    "庚寅": "松柏木", "辛卯": "松柏木",
    "壬辰": "長流水", "癸巳": "長流水",
    "甲午": "沙中金", "乙未": "沙中金",
    "丙申": "山下火", "丁酉": "山下火",
    "戊申": "大驛土", "己酉": "大驛土",
    "庚戌": "釵釧金", "辛亥": "釵釧金",
    "壬子": "桑柘木", "癸丑": "桑柘木",
    "甲寅": "大溪水", "乙卯": "大溪水",
    "丙辰": "砂中土", "丁巳": "砂中土",
    "戊午": "天上火", "己未": "天上火",
    "庚申": "石榴木", "辛酉": "石榴木",
    "壬戌": "大海水", "癸亥": "大海水",
}

BAGUA = ['乾', '兌', '離', '震', '巽', '坎', '艮', '坤']
BAGUA_NUMS = {b: i + 1 for i, b in enumerate(BAGUA)}

# 梅花易數 64卦
HEX64_NAMES = {
    (1,1):"乾為天", (1,2):"天澤履", (1,3):"天火同人", (1,4):"天雷無妄", (1,5):"天風姤", (1,6):"天水讼", (1,7):"天山遯", (1,8):"地天泰",
    (2,1):"澤天夬", (2,2):"兌為澤", (2,3):"澤火革", (2,4):"澤雷隨", (2,5):"澤風大過", (2,6):"澤水困", (2,7):"澤山咸", (2,8):"地澤臨",
    (3,1):"火天大有", (3,2):"火澤睽", (3,3):"離為火", (3,4):"火雷噬嗑", (3,5):"火風鼎", (3,6):"火水未濟", (3,7):"火山旅", (3,8):"地火晉",
    (4,1):"雷天大壯", (4,2):"雷澤歸妹", (4,3):"雷火豐", (4,4):"震為雷", (4,5):"雷風恆", (4,6):"雷水解", (4,7):"雷山小過", (4,8):"地雷復",
    (5,1):"風天大畜", (5,2):"風澤中孚", (5,3):"風火家人", (5,4):"風雷益", (5,5):"巽為風", (5,6):"風水漸", (5,7):"風山漸", (5,8):"地風升",
    (6,1):"水天需", (6,2):"水澤節", (6,3):"水火既濟", (6,4):"水雷屯", (6,5):"水風井", (6,6):"坎為水", (6,7):"水山蹇", (6,8):"地水師",
    (7,1):"山天大畜", (7,2):"山澤損", (7,3):"山火賁", (7,4):"山雷頤", (7,5):"山風蠱", (7,6):"山水蒙", (7,7):"艮為山", (7,8):"地山謙",
    (8,1):"天地否", (8,2):"地澤臨", (8,3):"地火晉", (8,4):"地雷復", (8,5):"地風升", (8,6):"地水師", (8,7):"地山謙", (8,8):"坤為地",
}

ELEMENT = {
    "甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土",
    "己": "土", "庚": "金", "辛": "金", "壬": "水", "癸": "水"
}

HE_PAIRS = {"甲": "己", "乙": "庚", "丙": "辛", "丁": "壬", "戊": "癸"}

# 地支藏干表 {index: [main_stem, ...]}
ZANGAN = {
    0: ['癸'], 1: ['己', '癸', '甲'], 2: ['甲', '丙', '戊'], 3: ['乙'],
    4: ['戊', '乙', '癸'], 5: ['丙', '庚', '戊'], 6: ['丁', '己'], 7: ['己', '丁', '乙'],
    8: ['庚', '壬', '戊'], 9: ['辛'], 10: ['戊', '辛', '丁'], 11: ['壬', '甲']
}

# 地支本氣五行
ZHI_ELEM = {
    "子": "水", "丑": "土", "寅": "木", "卯": "木", "辰": "土",
    "巳": "火", "午": "火", "未": "土", "申": "金", "酉": "金",
    "戌": "土", "亥": "水"
}

# 六爻類型對應（盲派分輕重）
LINE_TYPE = {1: "子孫", 2: "妻財", 3: "兄弟", 4: "兄弟", 5: "妻財", 6: "官鬼"}


# ============================================================
# 核心類
# ============================================================

class YinyimingIChing:

    def __init__(self, dt_str: str, tz: str = "Asia/Hong_Kong"):
        self.dt = datetime.fromisoformat(dt_str)
        self.tz = tz
        self.bazi = self._get_bazi()
        self.meihua = self._meihua_hexagram()
        self.nayin = self._get_nayin()

    def _get_bazi(self) -> Dict[str, Any]:
        day = sxtwl.fromSolar(self.dt.year, self.dt.month, self.dt.day)
        ygz = day.getYearGZ()
        mgz = day.getMonthGZ()
        dgz = day.getDayGZ()
        hgz = day.getHourGZ(self.dt.hour)

        bazi = {
            "year":  GAN[ygz.tg] + ZHI[ygz.dz],
            "month": GAN[mgz.tg] + ZHI[mgz.dz],
            "day":   GAN[dgz.tg] + ZHI[dgz.dz],
            "hour":  GAN[hgz.tg] + ZHI[hgz.dz],
        }
        # 藏干
        bazi["hidden"] = {
            "year":  ZANGAN.get(ygz.dz, []),
            "month": ZANGAN.get(mgz.dz, []),
            "day":   ZANGAN.get(dgz.dz, []),
            "hour":  ZANGAN.get(hgz.dz, []),
        }
        return bazi

    def _meihua_hexagram(self) -> Dict[str, Any]:
        day = sxtwl.fromSolar(self.dt.year, self.dt.month, self.dt.day)
        ygz = day.getYearGZ()
        mgz = day.getMonthGZ()
        dgz = day.getDayGZ()
        hgz = day.getHourGZ(self.dt.hour)

        Y = ygz.tg
        M = mgz.tg
        D = dgz.tg
        H = hgz.dz

        upper = (Y + M + D) % 8
        if upper == 0: upper = 8
        lower = (Y + M + D + H) % 8
        if lower == 0: lower = 8
        dongyao = (Y + M + D + H + self.dt.minute) % 6
        if dongyao == 0: dongyao = 6

        gua_name = HEX64_NAMES.get((lower, upper), f"{BAGUA[upper-1]}{BAGUA[lower-1]}")

        # 三爻卦
        trigram_table = {
            1: [1,1,1], 2: [1,1,0], 3: [1,0,1], 4: [1,0,0],
            5: [0,1,1], 6: [0,1,0], 7: [0,0,1], 8: [0,0,0],
        }
        upper_lines = trigram_table.get(BAGUA_NUMS[BAGUA[upper-1]], [0,0,0])
        lower_lines = trigram_table.get(BAGUA_NUMS[BAGUA[lower-1]], [0,0,0])

        all_lines = lower_lines + upper_lines
        di = dongyao - 1
        all_lines[di] = 1 - all_lines[di]

        return {
            "upper_gua": BAGUA[upper - 1],
            "lower_gua": BAGUA[lower - 1],
            "gua_name": gua_name,
            "hexagram_lines": all_lines,
            "dongyao_position": dongyao,
            "dongyao_idx": di,
        }

    def _get_nayin(self) -> str:
        hour_jiazi = self.bazi["hour"]
        return NAYIN_MAP.get(hour_jiazi, "平地木")

    def _analyze_he_chong(self) -> Dict[str, Any]:
        dz = self.bazi["day"][1]
        hz = self.bazi["hour"][1]

        chong = [("子","午"),("午","子"),("丑","未"),("未","丑"),
                 ("寅","申"),("申","寅"),("卯","酉"),("酉","卯"),
                 ("辰","戌"),("戌","辰"),("巳","亥"),("亥","巳")]
        he = [("子","丑"),("丑","子"),("寅","亥"),("亥","寅"),("卯","戌"),
              ("戌","卯"),("辰","酉"),("酉","辰"),("巳","申"),("申","巳"),
              ("午","未"),("未","午")]

        is_chong = (dz, hz) in chong or (hz, dz) in chong
        is_he = (dz, hz) in he or (hz, dz) in he

        if is_chong and is_he:
            summary = "有合有沖 → 波動大，方向待確認（合必求開）"
        elif is_chong:
            summary = "六沖 → 震蕩明顯，突破方向關鍵"
        elif is_he:
            summary = "六合 → 能量累積，蓄勢待發（合必求開）"
        else:
            summary = "無明顯合沖 → 相對穩定"

        return {"is_chong": is_chong, "is_he": is_he, "summary": summary}

    def analyze(self) -> Dict[str, Any]:
        bazi = self.bazi
        mh = self.meihua
        dong = mh["dongyao_position"]

        day_gan = bazi["day"][0]
        day_zhi = bazi["day"][1]
        month_zhi = bazi["month"][1]
        hour_zhi = bazi["hour"][1]

        day_hidden = bazi["hidden"]["day"]
        hour_hidden = bazi["hidden"]["hour"]

        # 妻財：日干合化之干
        cai = HE_PAIRS.get(day_gan, "")
        # 兄弟：同氣之干（劫財）
        brothers = [g for g in GAN if ELEMENT.get(g) == ELEMENT.get(day_gan) and g != day_gan]
        cai_count = sum(1 for h in day_hidden + hour_hidden for c in [cai] if h == c)
        brother_count = sum(1 for h in day_hidden + hour_hidden for b in brothers if h == b)

        line_type = LINE_TYPE.get(dong, "其他")

        # 權重：位置 + 月令
        weight = 3 if dong in [5, 6] else 2 if dong in [3, 4] else 1
        month_elem = ZHI_ELEM.get(month_zhi, "土")
        if ELEMENT.get(day_gan) == month_elem:
            weight += 1

        he_info = self._analyze_he_chong()

        # 納音分輕重（盲派實戰心法）
        # 劍鋒金、霹靂火 → 妻財加持最強（+10）
        # 白蠟金、爐中火、城頭土 → 妻財加持（+5）
        # 大海水、澗下水、長流水、泉中水 → 兄弟波動加持（+5）
        # 沙中金、桑柘木 → 官鬼加持（+3）
        nayin_wealth_boost = 0
        if any(n in self.nayin for n in ["劍鋒金", "霹靂火"]):
            nayin_wealth_boost = 10
        elif any(n in self.nayin for n in ["白蠟金", "爐中火", "城頭土"]):
            nayin_wealth_boost = 5

        nayin_brother_boost = 0
        if any(n in self.nayin for n in ["大海水", "澗下水", "長流水", "泉中水"]):
            nayin_brother_boost = 5
        elif any(n in self.nayin for n in ["沙中金", "桑柘木"]):
            nayin_brother_boost = 3

        # 預測
        direction = "VOLATILE / SIDEWAYS"
        confidence = 50
        reason = he_info["summary"]

        # UP 條件（放寬）
        if line_type == "妻財" and weight >= 3:
            direction = "UP"
            confidence = min(60 + weight + nayin_wealth_boost, 95)
            reason = f"妻財{dong}爻動 + 權重{weight} + 納音{self.nayin}加持，資金流入信號強"
        elif weight >= 5:
            direction = "UP"
            confidence = min(65, 95)
            reason = f"動爻權重{weight}，能量強，市場有機會順勢"
        elif line_type == "妻財" and cai_count >= 1:
            direction = "UP"
            confidence = 58
            reason = f"妻財藏干旺 + 動爻妻財位，資金信號"
        elif he_info["is_he"] and not he_info["is_chong"] and weight >= 2:
            # 六合（合必求開）+ 權重不低 → 蓄勢向上
            direction = "UP"
            confidence = 55
            reason = f"六合格局（合必求開），蓄勢待發，權重{weight}"

        # DOWN 條件
        elif line_type == "兄弟" and brother_count >= 2:
            direction = "DOWN"
            confidence = min(55 + weight + nayin_brother_boost, 95)
            reason = f"兄弟{brother_count}個 + 動爻在兄弟位 + 納音{self.nayin}，波動/回調壓力"
        elif line_type == "兄弟" and brother_count >= 1:
            direction = "DOWN"
            confidence = 52
            reason = f"兄弟信號{brother_count}個 + 動爻兄弟位，波動"
        elif line_type == "官鬼":
            direction = "DOWN"
            confidence = 55
            reason = "官鬼爻動，回調/壓力信號明確"
        elif he_info["is_chong"] and he_info["is_he"]:
            direction = "VOLATILE"
            confidence = 45
            reason = "有合有沖，波動加大，方向未明，建議觀望"
        elif he_info["is_chong"]:
            direction = "VOLATILE"
            confidence = 50
            reason = "六沖格局，市場可能快速突破，順勢跟蹤"

        return {
            "datetime": self.dt.isoformat(),
            "bazi": {
                "year": bazi["year"],
                "month": bazi["month"],
                "day": bazi["day"],
                "hour": bazi["hour"],
            },
            "meihua": {
                "upper_gua": mh["upper_gua"],
                "lower_gua": mh["lower_gua"],
                "gua_name": mh["gua_name"],
                "hexagram_lines": mh["hexagram_lines"],
                "dongyao_position": mh["dongyao_position"],
            },
            "nayin": self.nayin,
            "analysis": {
                "moving_line_type": line_type,
                "moving_line_weight": weight,
                "cai_count": cai_count,
                "brother_count": brother_count,
                "he_chong": he_info,
            },
            "prediction": {
                "direction": direction,
                "confidence": confidence,
                "reason": reason,
                "polymarket_suggestion": f"Polymarket BTC 5m {direction} Yes/No 參考",
            },
        }

    def predict_btc_5m(self) -> Dict:
        return self.analyze()


if __name__ == "__main__":
    p = YinyimingIChing("2026-06-05 15:30:00")
    r = p.predict_btc_5m()
    print(f"=== 隱姓埋名易經卦爻 BTC 5m ===")
    print(f"時間: {r['datetime']}")
    print(f"八字: {r['bazi']['year']} {r['bazi']['month']} {r['bazi']['day']} {r['bazi']['hour']}")
    print(f"卦象: {r['meihua']['gua_name']} ({r['meihua']['upper_gua']}/{r['meihua']['lower_gua']})")
    print(f"動爻: 第{r['meihua']['dongyao_position']}爻 ({r['analysis']['moving_line_type']}, 權重{r['analysis']['moving_line_weight']})")
    print(f"納音: {r['nayin']}")
    print(f"妻財信號: {r['analysis']['cai_count']}, 兄弟信號: {r['analysis']['brother_count']}")
    print(f"合沖: {r['analysis']['he_chong']['summary']}")
    print(f"\n預測: {r['prediction']['direction']}")
    print(f"信心: {r['prediction']['confidence']}%")
    print(f"理由: {r['prediction']['reason']}")
