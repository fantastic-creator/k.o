import sxtwl
import datetime
import math
from typing import Tuple, Dict

class BaziCalculator:
    """精确的八字计算器，基于sxtwl天文历法库"""

    # 天干
    HEAVENLY_STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    # 地支
    EARTHLY_BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

    def __init__(self, year: int, month: int, day: int, hour: int):
        """初始化八字计算器"""
        self.lunar_day = sxtwl.fromSolar(year, month, day)

        # 计算四柱
        self.year_pillar = self._calculate_year_pillar()
        self.month_pillar = self._calculate_month_pillar()
        self.day_pillar = self._calculate_day_pillar()
        self.hour_pillar = self._calculate_hour_pillar(hour)

    def _calculate_year_pillar(self) -> Tuple[int, int]:
        """计算年柱 (干支)"""
        gz = self.lunar_day.getYearGZ(False)  # 以立春为界
        return (gz.tg, gz.dz)

    def _calculate_month_pillar(self) -> Tuple[int, int]:
        """计算月柱 (干支)"""
        gz = self.lunar_day.getMonthGZ()
        return (gz.tg, gz.dz)

    def _calculate_day_pillar(self) -> Tuple[int, int]:
        """计算日柱 (干支)"""
        gz = self.lunar_day.getDayGZ()
        return (gz.tg, gz.dz)

    def _calculate_hour_pillar(self, hour: int) -> Tuple[int, int]:
        """计算时柱 (干支)"""
        gz = self.lunar_day.getHourGZ(hour)
        return (gz.tg, gz.dz)

    def get_bazi_string(self) -> str:
        """获取八字字符串表示"""
        y_stem, y_branch = self.year_pillar
        m_stem, m_branch = self.month_pillar
        d_stem, d_branch = self.day_pillar
        h_stem, h_branch = self.hour_pillar

        return f"{self.HEAVENLY_STEMS[y_stem]}{self.EARTHLY_BRANCHES[y_branch]} " \
               f"{self.HEAVENLY_STEMS[m_stem]}{self.EARTHLY_BRANCHES[m_branch]} " \
               f"{self.HEAVENLY_STEMS[d_stem]}{self.EARTHLY_BRANCHES[d_branch]} " \
               f"{self.HEAVENLY_STEMS[h_stem]}{self.EARTHLY_BRANCHES[h_branch]}"

    def get_heavenly_stems(self) -> list:
        """获取四柱天干列表"""
        return [
            self.HEAVENLY_STEMS[self.year_pillar[0]],
            self.HEAVENLY_STEMS[self.month_pillar[0]],
            self.HEAVENLY_STEMS[self.day_pillar[0]],
            self.HEAVENLY_STEMS[self.hour_pillar[0]]
        ]

    def get_earthly_branches(self) -> list:
        """获取四柱地支列表"""
        return [
            self.EARTHLY_BRANCHES[self.year_pillar[1]],
            self.EARTHLY_BRANCHES[self.month_pillar[1]],
            self.EARTHLY_BRANCHES[self.day_pillar[1]],
            self.EARTHLY_BRANCHES[self.hour_pillar[1]]
        ]


def calculate_beads_distribution(heavenly_stems, earthly_branches):
    """计算八字五行珠子分配"""
    # 天干到五行的映射
    stem_to_element = {
        '甲': '木', '乙': '木',
        '丙': '火', '丁': '火',
        '戊': '土', '己': '土',
        '庚': '金', '辛': '金',
        '壬': '水', '癸': '水'
    }

    # 地支的天干组成
    branch_to_stems = {
        '子': ['癸'],
        '丑': ['己', '癸', '辛'],
        '寅': ['甲', '丙', '戊'],
        '卯': ['乙'],
        '辰': ['戊', '乙', '癸'],
        '巳': ['丙', '庚', '戊'],
        '午': ['丁', '己'],
        '未': ['己', '丁', '乙'],
        '申': ['庚', '壬', '戊'],
        '酉': ['辛'],
        '戌': ['戊', '辛', '丁'],
        '亥': ['壬', '甲']
    }

    # 四柱地支总分
    branch_total_scores = {0: 100, 1: 150, 2: 100, 3: 100}

    # 初始化五行分数
    element_scores = {'金': 0, '木': 0, '水': 0, '火': 0, '土': 0}

    # 计算天干分数
    for stem in heavenly_stems:
        element = stem_to_element[stem]
        element_scores[element] += 40

    # 计算地支分数
    for i, branch in enumerate(earthly_branches):
        branch_score = branch_total_scores[i]
        stems = branch_to_stems[branch]

        # 根据天干数量分配分数
        if len(stems) == 1:
            scores = [branch_score]
        elif len(stems) == 2:
            first_score = math.floor(branch_score * 0.7)
            second_score = branch_score - first_score
            scores = [first_score, second_score]
        elif len(stems) == 3:
            first_score = math.floor(branch_score * 0.7)
            second_score = math.floor(branch_score * 0.2)
            third_score = branch_score - first_score - second_score
            scores = [first_score, second_score, third_score]

        # 分配分数到对应五行
        for j, stem in enumerate(stems):
            element = stem_to_element[stem]
            element_scores[element] += scores[j]

    # 验证总分
    total_score = sum(element_scores.values())
    assert total_score == 610, f"总分数错误: {total_score} ≠ 610"

    # 计算互补比例
    original_ratios = {e: score / total_score for e, score in element_scores.items()}
    complementary_ratios = {e: 1 - ratio for e, ratio in original_ratios.items()}
    comp_total = sum(complementary_ratios.values())
    normalized_comp_ratios = {e: ratio / comp_total for e, ratio in complementary_ratios.items()}

    # 分配24颗珠子（使用最大余数法）
    total_beads = 24
    theoretical_beads = {e: ratio * total_beads for e, ratio in normalized_comp_ratios.items()}
    bead_allocation = {e: int(count) for e, count in theoretical_beads.items()}

    # 计算剩余珠子数量并按余数大小分配
    remaining_beads = total_beads - sum(bead_allocation.values())
    remainders = {e: count - int(count) for e, count in theoretical_beads.items()}
    sorted_elements = sorted(remainders.keys(), key=lambda e: remainders[e], reverse=True)

    for i in range(remaining_beads):
        bead_allocation[sorted_elements[i]] += 1

    return {
        "五行分数": element_scores,
        "珠子分配": bead_allocation
    }

def main():
    try:
        print("八字五行珠子分配计算器")
        print("=" * 30)

        # 输入公历年月日时
        date_str = input("请输入年月日时 (格式: YYYY.MM.DD.HH): ")
        parts = date_str.split('.')

        if len(parts) != 4:
            print("输入格式错误! 请使用YYYY.MM.DD.HH格式。")
            return

        year = int(parts[0])
        month = int(parts[1])
        day = int(parts[2])
        hour = int(parts[3])

        # 验证输入数据的合法性
        if not (1900 <= year <= 2100):
            print("年份超出范围 (1900-2100)!")
            return

        if not (1 <= month <= 12) or not (1 <= day <= 31) or not (0 <= hour <= 23):
            print("日期或时间格式错误!")
            return

        # 进一步验证日期的合法性
        try:
            datetime.datetime(year, month, day, hour)
        except ValueError:
            print("输入的日期无效!")
            return

        # 计算八字
        bazi_calculator = BaziCalculator(year, month, day, hour)

        # 获取八字
        bazi_string = bazi_calculator.get_bazi_string()
        heavenly_stems = bazi_calculator.get_heavenly_stems()
        earthly_branches = bazi_calculator.get_earthly_branches()

        # 计算珠子分配
        result = calculate_beads_distribution(heavenly_stems, earthly_branches)

        # 显示结果
        print(f"\n八字: {bazi_string}")
        print(f"天干: {''.join(heavenly_stems)}")
        print(f"地支: {''.join(earthly_branches)}")

        print("\n=== 五行分数 ===")
        for element, score in sorted(result["五行分数"].items()):
            print(f"{element}: {score}分")

        print("\n=== 珠子分配 (共24颗) ===")
        for element, count in sorted(result["珠子分配"].items()):
            print(f"{element}: {count}颗")

    except Exception as e:
        print(f"\n计算错误: {e}")

if __name__ == "__main__":
    main()