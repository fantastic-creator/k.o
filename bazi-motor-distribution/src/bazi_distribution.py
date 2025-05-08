import sxtwl
import datetime
import math
import serial

# 串口端口配置
SERIAL_PORT = '/dev/ttyS3'  # 如有需要请修改为你的实际端口

class BaziCalculator:
    """精确的八字计算器，基于sxtwl天文历法库"""

    HEAVENLY_STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    EARTHLY_BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

    def __init__(self, year: int, month: int, day: int, hour: int):
        self.lunar_day = sxtwl.fromSolar(year, month, day)
        self.year_pillar = self._calculate_year_pillar()
        self.month_pillar = self._calculate_month_pillar()
        self.day_pillar = self._calculate_day_pillar()
        self.hour_pillar = self._calculate_hour_pillar(hour)

    def _calculate_year_pillar(self):
        gz = self.lunar_day.getYearGZ(False)
        return (gz.tg, gz.dz)

    def _calculate_month_pillar(self):
        gz = self.lunar_day.getMonthGZ()
        return (gz.tg, gz.dz)

    def _calculate_day_pillar(self):
        gz = self.lunar_day.getDayGZ()
        return (gz.tg, gz.dz)

    def _calculate_hour_pillar(self, hour):
        gz = self.lunar_day.getHourGZ(hour)
        return (gz.tg, gz.dz)

    def get_heavenly_stems(self):
        return [
            self.HEAVENLY_STEMS[self.year_pillar[0]],
            self.HEAVENLY_STEMS[self.month_pillar[0]],
            self.HEAVENLY_STEMS[self.day_pillar[0]],
            self.HEAVENLY_STEMS[self.hour_pillar[0]]
        ]

    def get_earthly_branches(self):
        return [
            self.EARTHLY_BRANCHES[self.year_pillar[1]],
            self.EARTHLY_BRANCHES[self.month_pillar[1]],
            self.EARTHLY_BRANCHES[self.day_pillar[1]],
            self.EARTHLY_BRANCHES[self.hour_pillar[1]]
        ]

def calculate_beads_distribution(heavenly_stems, earthly_branches):
    stem_to_element = {
        '甲': '木', '乙': '木',
        '丙': '火', '丁': '火',
        '戊': '土', '己': '土',
        '庚': '金', '辛': '金',
        '壬': '水', '癸': '水'
    }

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

    branch_total_scores = {0: 100, 1: 150, 2: 100, 3: 100}
    element_scores = {'金': 0, '木': 0, '水': 0, '火': 0, '土': 0}

    for stem in heavenly_stems:
        element = stem_to_element[stem]
        element_scores[element] += 40

    for i, branch in enumerate(earthly_branches):
        branch_score = branch_total_scores[i]
        stems = branch_to_stems[branch]

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

        for j, stem in enumerate(stems):
            element = stem_to_element[stem]
            element_scores[element] += scores[j]

    total_score = sum(element_scores.values())
    assert total_score == 610, f"总分数错误: {total_score} ≠ 610"

    total_beads = 24
    bead_allocation = {e: int(score / total_score * total_beads) for e, score in element_scores.items()}

    remaining_beads = total_beads - sum(bead_allocation.values())
    remainders = {e: (score / total_score * total_beads) - bead_allocation[e] for e, score in element_scores.items()}
    sorted_elements = sorted(remainders.keys(), key=lambda e: remainders[e], reverse=True)

    for i in range(remaining_beads):
        bead_allocation[sorted_elements[i]] += 1

    return bead_allocation

def send_motor_commands(bead_allocation):
    ser = serial.Serial(SERIAL_PORT, 9600, timeout=10)  # 使用前置常量
    for element, count in bead_allocation.items():
        angle = count * 30  # Each bead corresponds to 30 degrees
        motor_idx = {'土': 1, '木': 2, '水': 3, '火': 4, '金': 5}[element]
        command = f"M{motor_idx}:{angle}\n"
        ser.write(command.encode())
        # 等待 Arduino 返回 DONE
        while True:
            line = ser.readline().decode().strip()
            if line == "DONE":
                break
    ser.close()

def main():
    date_str = input("请输入年月日时 (格式: YYYY.MM.DD.HH): ")
    parts = date_str.split('.')

    year = int(parts[0])
    month = int(parts[1])
    day = int(parts[2])
    hour = int(parts[3])

    bazi_calculator = BaziCalculator(year, month, day, hour)
    heavenly_stems = bazi_calculator.get_heavenly_stems()
    earthly_branches = bazi_calculator.get_earthly_branches()

    bead_allocation = calculate_beads_distribution(heavenly_stems, earthly_branches)
    send_motor_commands(bead_allocation)

if __name__ == "__main__":
    main()