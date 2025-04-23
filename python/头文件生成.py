import sxtwl
import datetime
from collections import defaultdict

def generate_bazi_mappings():
    """
    生成1950-2050年公历日期到八字的映射表
    采用压缩格式以节省Arduino存储空间
    """
    print("开始生成八字映射表头文件...")

    # 天干地支
    heavenly_stems = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    earthly_branches = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

    # 五行
    stem_to_element = {
        '甲': '木', '乙': '木', '丙': '火', '丁': '火', '戊': '土',
        '己': '土', '庚': '金', '辛': '金', '壬': '水', '癸': '水'
    }

    # 地支的天干组成 - 用于生成头文件
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

    # 开始生成头文件
    header_content = """// 八字映射表 (1950-2050) - 自动生成
// 用于快速获取公历日期对应的八字
// 不要手动修改此文件

#ifndef BAZI_MAPPINGS_H
#define BAZI_MAPPINGS_H

// 五行编码
#define METAL 0  // 金
#define WOOD  1  // 木
#define WATER 2  // 水
#define FIRE  3  // 火
#define EARTH 4  // 土

"""

    # 1. 生成天干地支基础数据
    header_content += "// 天干字符表\n"
    header_content += "const char* HEAVENLY_STEMS[10] = {\"甲\", \"乙\", \"丙\", \"丁\", \"戊\", \"己\", \"庚\", \"辛\", \"壬\", \"癸\"};\n\n"

    header_content += "// 地支字符表\n"
    header_content += "const char* EARTHLY_BRANCHES[12] = {\"子\", \"丑\", \"寅\", \"卯\", \"辰\", \"巳\", \"午\", \"未\", \"申\", \"酉\", \"戌\", \"亥\"};\n\n"

    # 2. 天干到五行的映射
    header_content += "// 天干到五行的映射\n"
    header_content += "const byte STEM_TO_ELEMENT[10] = {\n"
    element_to_code = {"金": 0, "木": 1, "水": 2, "火": 3, "土": 4}

    for i, stem in enumerate(heavenly_stems):
        element = stem_to_element[stem]
        header_content += f"    {element_to_code[element]},  // {stem} -> {element}\n"
    header_content = header_content.rstrip(",\n") + "\n};\n\n"

    # 3. 地支天干组成
    header_content += "// 地支中天干的数量\n"
    header_content += "const byte BRANCH_STEM_COUNT[12] = {\n"
    for i, branch in enumerate(earthly_branches):
        stems = branch_to_stems[branch]
        header_content += f"    {len(stems)},  // {branch}: {', '.join(stems)}\n"
    header_content = header_content.rstrip(",\n") + "\n};\n\n"

    header_content += "// 地支中的天干编码\n"
    header_content += "const byte BRANCH_STEMS[12][3] = {\n"
    for i, branch in enumerate(earthly_branches):
        stems = branch_to_stems[branch]
        stem_codes = [str(heavenly_stems.index(stem)) for stem in stems]
        # 填充255作为无效值
        while len(stem_codes) < 3:
            stem_codes.append("255")
        header_content += f"    {{{', '.join(stem_codes)}}},  // {branch}: {', '.join(stems)}\n"
    header_content = header_content.rstrip(",\n") + "\n};\n\n"

    # 4. 生成年份到年干支的映射
    # 我们只存储1950年的基准干支，其他年份可以通过计算得到
    base_year = 1950
    header_content += "// 基准年份(1950)的干支索引 (用于计算其他年份)\n"
    lunar_day = sxtwl.fromSolar(base_year, 1, 1)
    gz = lunar_day.getYearGZ(False)  # 以立春为界
    header_content += f"#define BASE_YEAR {base_year}\n"
    header_content += f"#define BASE_YEAR_STEM {gz.tg}  // {heavenly_stems[gz.tg]}\n"
    header_content += f"#define BASE_YEAR_BRANCH {gz.dz}  // {earthly_branches[gz.dz]}\n\n"

    # 5. 生成月干支表
    # 月干支与月份以及年干有关，使用更紧凑的表示
    header_content += "// 月干支起始值 (根据年干确定)\n"
    header_content += "const byte MONTH_STEM_BASE[10] = {\n"
    month_stems = {}
    # 计算不同年干下的月干
    for stem_index in range(10):
        # 取第一个月的月干作为基准
        first_month_stem_index = (stem_index * 2) % 10
        header_content += f"    {first_month_stem_index},  // {heavenly_stems[stem_index]}年\n"
    header_content = header_content.rstrip(",\n") + "\n};\n\n"

    # 6. 生成立春日期表 - 月份的分界点
    # 对于年份范围内的每一年，我们都需要计算立春的日期
    # 这是因为年柱以立春为界
    header_content += "// 立春日期表 (1950-2050)\n"
    header_content += "const byte LICHUN_DAYS[101] = {\n"

    lichun_days = []
    for year in range(1950, 2051):
        # 查找立春日期 (通常在2月4日或5日左右)
        lichun_day = 0
        for day in range(3, 7):  # 检查2月3日-2月6日
            lunar_day = sxtwl.fromSolar(year, 2, day)
            if lunar_day.hasJieQi() and lunar_day.getJieQi() == 3:  # 3是立春的索引
                lichun_day = day
                break

        if lichun_day == 0:  # 如果没找到，使用默认值
            lichun_day = 4  # 默认2月4日

        lichun_days.append(lichun_day)

        # 每行最多10个值，使输出更整洁
        if (year - 1950) % 10 == 0:
            header_content += f"    /* {year} - {year+9} */ "

        header_content += f"{lichun_day}"

        if year < 2050:
            header_content += ", "

        if (year - 1950) % 10 == 9:
            header_content += "\n"

    header_content = header_content.rstrip(",\n") + "\n};\n\n"

    # 7. 生成简化的日干支计算方法
    # 对于日干支，我们可以使用简单的算法，不需要完整的表格
    # 提供日期到公元原点的天数差计算方法
    header_content += """// 计算日期到公元原点的天数差函数
// 这是一个简化版的算法，用于计算1900年后的日期
uint32_t dayNumber(uint16_t y, uint8_t m, uint8_t d) {
  // 基于Keith Thompson的算法，简化为仅适用于1900年后
  if (m < 3) {
    y--;
    m += 12;
  }
  return 365 * y + y / 4 - y / 100 + y / 400 + (153 * m - 457) / 5 + d - 306;
}

// 根据天数差计算日柱
void getDayPillar(uint32_t dayNum, uint8_t& stem, uint8_t& branch) {
  // 计算日干支 (参考点: 1900-01-01 是 庚子日)
  stem = (dayNum + 9) % 10;  // 干
  branch = (dayNum + 11) % 12;  // 支
}

// 计算时柱
void getHourPillar(uint8_t hour, uint8_t dayStem, uint8_t& stem, uint8_t& branch) {
  // 将小时转换为时辰 (0-11)
  branch = hour / 2;
  if (hour == 23) branch = 0;  // 23点属于子时

  // 根据日干推算时干
  // 甲己日起甲子时，乙庚日起丙子时，丙辛日起戊子时，丁壬日起庚子时，戊癸日起壬子时
  uint8_t baseHourStem = 0;
  switch(dayStem % 5) {
    case 0: baseHourStem = 0; break;  // 甲己日起甲子时
    case 1: baseHourStem = 2; break;  // 乙庚日起丙子时
    case 2: baseHourStem = 4; break;  // 丙辛日起戊子时
    case 3: baseHourStem = 6; break;  // 丁壬日起庚子时
    case 4: baseHourStem = 8; break;  // 戊癸日起壬子时
  }

  stem = (baseHourStem + branch) % 10;
}
"""

    # 8. 完成头文件
    header_content += "\n#endif // BAZI_MAPPINGS_H\n"

    # 写入头文件
    with open("bazi_mappings.h", "w", encoding="utf-8") as f:
        f.write(header_content)

    print("八字映射表头文件生成完成: bazi_mappings.h")

    # 9. 附加信息: 生成珠子分配映射表
    # 为Arduino提供珠子分配的核心数据
    beads_header = """// 八字珠子分配映射表
// 用于计算五行珠子分配
// 自动生成，请勿手动修改

#ifndef BAZI_BEADS_H
#define BAZI_BEADS_H

// 四柱地支总分
const int BRANCH_TOTAL_SCORES[4] = {100, 150, 100, 100};  // 年月日时

#endif // BAZI_BEADS_H
"""

    with open("bazi_beads.h", "w", encoding="utf-8") as f:
        f.write(beads_header)

    print("珠子分配头文件生成完成: bazi_beads.h")

if __name__ == "__main__":
    generate_bazi_mappings()