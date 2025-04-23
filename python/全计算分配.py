import sxtwl
import datetime
import time
import math
from typing import Tuple, List, Dict

class BaziCalculator:
    """精确的八字计算器，基于sxtwl天文历法库"""

    # 天干
    HEAVENLY_STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    # 地支
    EARTHLY_BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    # 天干五行
    HEAVENLY_STEMS_ELEMENTS = ["木", "木", "火", "火", "土", "土", "金", "金", "水", "水"]
    # 地支五行
    EARTHLY_BRANCHES_ELEMENTS = ["水", "土", "木", "木", "土", "火", "火", "土", "金", "金", "土", "水"]
    # 二十四节气名称
    SOLAR_TERMS = [
        "冬至", "小寒", "大寒", "立春", "雨水", "惊蛰",
        "春分", "清明", "谷雨", "立夏", "小满", "芒种",
        "夏至", "小暑", "大暑", "立秋", "处暑", "白露",
        "秋分", "寒露", "霜降", "立冬", "小雪", "大雪"
    ]
    # 时辰对应表 (24小时制)
    HOUR_TO_BRANCH = {
        23: 0, 0: 0,       # 子时 (23:00-00:59)
        1: 1, 2: 1,        # 丑时 (01:00-02:59)
        3: 2, 4: 2,        # 寅时 (03:00-04:59)
        5: 3, 6: 3,        # 卯时 (05:00-06:59)
        7: 4, 8: 4,        # 辰时 (07:00-08:59)
        9: 5, 10: 5,       # 巳时 (09:00-10:59)
        11: 6, 12: 6,      # 午时 (11:00-12:59)
        13: 7, 14: 7,      # 未时 (13:00-14:59)
        15: 8, 16: 8,      # 申时 (15:00-16:59)
        17: 9, 18: 9,      # 酉时 (17:00-18:59)
        19: 10, 20: 10,    # 戌时 (19:00-20:59)
        21: 11, 22: 11,    # 亥时 (21:00-22:59)
    }

    def __init__(self, year: int, month: int, day: int, hour: int):
        """初始化八字计算器

        Args:
            year: 公历年
            month: 公历月
            day: 公历日
            hour: 公历小时 (24小时制)
        """
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour

        # 使用sxtwl获取日期信息
        self.lunar_day = sxtwl.fromSolar(year, month, day)

        # 计算四柱
        self.year_pillar = self._calculate_year_pillar()
        self.month_pillar = self._calculate_month_pillar()
        self.day_pillar = self._calculate_day_pillar()
        self.hour_pillar = self._calculate_hour_pillar()

    def _calculate_year_pillar(self) -> Tuple[int, int]:
        """计算年柱 (干支)"""
        # 使用sxtwl计算年柱（考虑立春分界）
        # 以立春为界的天干地支
        gz = self.lunar_day.getYearGZ(False)  # False表示以立春为界
        return (gz.tg, gz.dz)

    def _calculate_month_pillar(self) -> Tuple[int, int]:
        """计算月柱 (干支)"""
        # 使用sxtwl直接获取月干支
        gz = self.lunar_day.getMonthGZ()
        return (gz.tg, gz.dz)

    def _get_current_month_terms(self, year: int, month: int) -> Tuple[Tuple[str, int], Tuple[str, int]]:
        """获取当前月的两个节气

        Returns:
            ((节气1名称, 节气1日期), (节气2名称, 节气2日期))
        """
        term_index1 = (month - 1) * 2 % 24
        term_index2 = (term_index1 + 1) % 24

        term1_day = 0
        term2_day = 0

        for day in range(1, 32):
            if day > 31:  # 防止越界
                break

            try:
                lunar_day = sxtwl.fromSolar(year, month, day)
                if lunar_day.hasJieQi():
                    jq_index = lunar_day.getJieQi()

                    if jq_index == term_index1:
                        term1_day = day
                    elif jq_index == term_index2:
                        term2_day = day
            except:
                continue

        term1 = (self.SOLAR_TERMS[term_index1], term1_day)
        term2 = (self.SOLAR_TERMS[term_index2], term2_day)

        return (term1, term2)

    def _calculate_day_pillar(self) -> Tuple[int, int]:
        """计算日柱 (干支)"""
        # 使用sxtwl直接获取日干支
        gz = self.lunar_day.getDayGZ()
        return (gz.tg, gz.dz)

    def _calculate_hour_pillar(self) -> Tuple[int, int]:
        """计算时柱 (干支)"""
        # 获取当日的日干支对象
        day_gz = self.lunar_day.getDayGZ()

        # 使用sxtwl获取时辰干支
        gz = self.lunar_day.getHourGZ(self.hour)
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

    def get_wuxing_string(self) -> str:
        """获取五行字符串表示"""
        y_stem, y_branch = self.year_pillar
        m_stem, m_branch = self.month_pillar
        d_stem, d_branch = self.day_pillar
        h_stem, h_branch = self.hour_pillar

        return f"{self.HEAVENLY_STEMS_ELEMENTS[y_stem]}{self.EARTHLY_BRANCHES_ELEMENTS[y_branch]} " \
               f"{self.HEAVENLY_STEMS_ELEMENTS[m_stem]}{self.EARTHLY_BRANCHES_ELEMENTS[m_branch]} " \
               f"{self.HEAVENLY_STEMS_ELEMENTS[d_stem]}{self.EARTHLY_BRANCHES_ELEMENTS[d_branch]} " \
               f"{self.HEAVENLY_STEMS_ELEMENTS[h_stem]}{self.EARTHLY_BRANCHES_ELEMENTS[h_branch]}"

    def get_wuxing_count(self) -> Dict[str, int]:
        """统计五行出现次数"""
        y_stem, y_branch = self.year_pillar
        m_stem, m_branch = self.month_pillar
        d_stem, d_branch = self.day_pillar
        h_stem, h_branch = self.hour_pillar

        elements = [
            self.HEAVENLY_STEMS_ELEMENTS[y_stem],
            self.EARTHLY_BRANCHES_ELEMENTS[y_branch],
            self.HEAVENLY_STEMS_ELEMENTS[m_stem],
            self.EARTHLY_BRANCHES_ELEMENTS[m_branch],
            self.HEAVENLY_STEMS_ELEMENTS[d_stem],
            self.EARTHLY_BRANCHES_ELEMENTS[d_branch],
            self.HEAVENLY_STEMS_ELEMENTS[h_stem],
            self.EARTHLY_BRANCHES_ELEMENTS[h_branch],
        ]

        count = {
            "木": 0,
            "火": 0,
            "土": 0,
            "金": 0,
            "水": 0
        }

        for element in elements:
            count[element] += 1

        return count

    def get_lunar_date_string(self) -> str:
        """获取农历日期字符串表示"""
        month_names = ["", "正", "二", "三", "四", "五", "六", "七", "八", "九", "十", "十一", "十二"]
        day_names = ["", "初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十",
                    "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十",
                    "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十"]

        lunar_month = self.lunar_day.getLunarMonth()
        lunar_day = self.lunar_day.getLunarDay()
        is_leap = self.lunar_day.isLunarLeap()

        month_str = f"{'闰' if is_leap else ''}{month_names[lunar_month]}月"
        day_str = day_names[lunar_day]

        return f"{month_str}{day_str}"

    def get_jieqi_info(self) -> str:
        """获取节气信息"""
        if not self.lunar_day.hasJieQi():
            return "无节气"

        jieqi_index = self.lunar_day.getJieQi()
        return self.SOLAR_TERMS[jieqi_index]

    def get_heavenly_stems(self) -> list:
        """获取四柱天干列表"""
        y_stem, _ = self.year_pillar
        m_stem, _ = self.month_pillar
        d_stem, _ = self.day_pillar
        h_stem, _ = self.hour_pillar

        return [
            self.HEAVENLY_STEMS[y_stem],
            self.HEAVENLY_STEMS[m_stem],
            self.HEAVENLY_STEMS[d_stem],
            self.HEAVENLY_STEMS[h_stem]
        ]

    def get_earthly_branches(self) -> list:
        """获取四柱地支列表"""
        _, y_branch = self.year_pillar
        _, m_branch = self.month_pillar
        _, d_branch = self.day_pillar
        _, h_branch = self.hour_pillar

        return [
            self.EARTHLY_BRANCHES[y_branch],
            self.EARTHLY_BRANCHES[m_branch],
            self.EARTHLY_BRANCHES[d_branch],
            self.EARTHLY_BRANCHES[h_branch]
        ]


def calculate_beads_distribution(heavenly_stems, earthly_branches):
    """
    计算八字五行珠子分配

    Args:
        heavenly_stems: 四柱天干 [年, 月, 日, 时]
        earthly_branches: 四柱地支 [年, 月, 日, 时]

    Returns:
        dict: 五行对应的珠子数量
    """
    # 定义天干到五行的映射
    stem_to_element = {
        '甲': '木', '乙': '木',
        '丙': '火', '丁': '火',
        '戊': '土', '己': '土',
        '庚': '金', '辛': '金',
        '壬': '水', '癸': '水'
    }

    # 定义地支的天干组成
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

    # 定义四柱地支总分
    branch_total_scores = {
        0: 100,  # 年柱
        1: 150,  # 月柱
        2: 100,  # 日柱
        3: 100   # 时柱
    }

    # 初始化五行分数
    element_scores = {
        '金': 0, '木': 0, '水': 0, '火': 0, '土': 0
    }

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

    # 记录每个地支的分数分配(用于显示详细计算过程)
    branch_score_details = []
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

        # 记录地支的得分明细
        details = {}
        for j, stem in enumerate(stems):
            element = stem_to_element[stem]
            if element not in details:
                details[element] = 0
            details[element] += scores[j]
        branch_score_details.append(details)

    # 验证总分
    total_score = sum(element_scores.values())
    if total_score != 610:
        raise ValueError(f"总分数错误: {total_score} ≠ 610")

    # 计算互补比例
    original_ratios = {e: score / total_score for e, score in element_scores.items()}
    complementary_ratios = {e: 1 - ratio for e, ratio in original_ratios.items()}

    # 计算互补比例总和
    comp_total = sum(complementary_ratios.values())

    # 归一化互补比例
    normalized_comp_ratios = {e: ratio / comp_total for e, ratio in complementary_ratios.items()}

    # 分配24颗珠子（使用最大余数法）
    total_beads = 24
    theoretical_beads = {e: ratio * total_beads for e, ratio in normalized_comp_ratios.items()}

    # 先分配整数部分
    bead_allocation = {e: int(count) for e, count in theoretical_beads.items()}

    # 计算剩余珠子数量
    remaining_beads = total_beads - sum(bead_allocation.values())

    # 按余数大小分配剩余珠子
    remainders = {e: count - int(count) for e, count in theoretical_beads.items()}
    sorted_elements = sorted(remainders.keys(), key=lambda e: remainders[e], reverse=True)

    for i in range(remaining_beads):
        bead_allocation[sorted_elements[i]] += 1

    return {
        "五行分数": element_scores,
        "原始比例": original_ratios,
        "互补比例": normalized_comp_ratios,
        "珠子分配": bead_allocation,
        "地支分数详情": branch_score_details
    }

def main():
    try:
        print("八字五行珠子分配计算器")
        print("=" * 40)

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

        if not (1 <= month <= 12):
            print("月份必须在1-12之间!")
            return

        if not (1 <= day <= 31):
            print("日期必须在1-31之间!")
            return

        if not (0 <= hour <= 23):
            print("小时必须在0-23之间!")
            return

        # 进一步验证日期的合法性
        try:
            datetime.datetime(year, month, day, hour)
        except ValueError:
            print("输入的日期无效!")
            return

        print("\n计算中，请稍候...")
        start_time = time.time()

        # 计算八字
        bazi_calculator = BaziCalculator(year, month, day, hour)

        # 输出八字和五行
        print("\n=== 基本信息 ===")
        print(f"公历: {year}年{month}月{day}日 {hour}时")
        print(f"农历: {bazi_calculator.get_lunar_date_string()}")
        print(f"节气: {bazi_calculator.get_jieqi_info()}")
        print(f"八字: {bazi_calculator.get_bazi_string()}")
        print(f"五行: {bazi_calculator.get_wuxing_string()}")

        # 输出五行统计
        wuxing_count = bazi_calculator.get_wuxing_count()
        print("\n=== 五行出现次数 ===")
        for element, count in wuxing_count.items():
            print(f"{element}: {count}次")

        # 计算珠子分配
        heavenly_stems = bazi_calculator.get_heavenly_stems()
        earthly_branches = bazi_calculator.get_earthly_branches()

        # 显示所用的天干地支
        print("\n=== 八字详情 ===")
        print(f"天干: {heavenly_stems}")
        print(f"地支: {earthly_branches}")

        result = calculate_beads_distribution(heavenly_stems, earthly_branches)

        # 显示计算过程和结果
        print("\n=== 计算过程 ===")

        # 天干得分
        print("天干得分:")
        for element, score in result["五行分数"].items():
            stems_count = sum(1 for stem in heavenly_stems if {'甲':'木', '乙':'木', '丙':'火', '丁':'火', '戊':'土',
                                                              '己':'土', '庚':'金', '辛':'金', '壬':'水', '癸':'水'}[stem] == element)
            if stems_count > 0:
                print(f"  {element}: {stems_count}个 × 40 = {stems_count*40}分")

        # 地支得分
        pillar_names = ["年柱", "月柱", "日柱", "时柱"]
        branch_total_scores = {0: 100, 1: 150, 2: 100, 3: 100}

        print("\n地支得分:")
        for i, (branch, details) in enumerate(zip(earthly_branches, result["地支分数详情"])):
            print(f"  {pillar_names[i]}{branch} (总分{branch_total_scores[i]}) →", end=" ")
            output = []
            for element, score in details.items():
                output.append(f"{element}+{score}")
            print(", ".join(output))

        # 总分验证
        total_score = sum(result["五行分数"].values())
        print(f"\n总分验证: {total_score} {'= 610 (✓)' if total_score == 610 else '≠ 610 (✗)'}")

        # 显示结果
        print("\n=== 五行分数 ===")
        for element, score in result["五行分数"].items():
            print(f"{element}: {score}分")

        print("\n=== 原始比例 ===")
        for element, ratio in result["原始比例"].items():
            print(f"{element}: {ratio:.4f}")

        print("\n=== 互补比例 (归一化) ===")
        for element, ratio in result["互补比例"].items():
            print(f"{element}: {ratio:.4f}")

        print("\n=== 珠子分配 (共24颗) ===")
        for element, count in result["珠子分配"].items():
            print(f"{element}: {count}颗")

        end_time = time.time()
        print(f"\n计算耗时: {end_time - start_time:.2f}秒")

    except Exception as e:
        print(f"\n发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()