import sxtwl
from datetime import datetime

# 天干地支列表
TIANGAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
DIZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]


def get_year_gan_zhi(year, month, day, hour, minute):
    lunar = sxtwl.Lunar()
    yc = lunar.getYearCal(year)
    jq = yc.getJieQi()
    lichun = jq[2]  # 立春为索引2

    input_dt = datetime(year, month, day, hour, minute)
    lichun_dt = datetime(lichun.Y, lichun.M, lichun.D,
                         lichun.h, lichun.m, lichun.s)

    year_gan_year = year if input_dt >= lichun_dt else year - 1
    gan = TIANGAN[(year_gan_year - 4) % 10]
    zhi = DIZHI[(year_gan_year - 4) % 12]
    return gan, zhi


def get_month_gan_zhi(input_year, input_month, input_day, input_hour, input_minute, year_gan):
    lunar = sxtwl.Lunar()
    input_dt = datetime(input_year, input_month, input_day,
                        input_hour, input_minute)
    jie_list = []

    for y in [input_year - 1, input_year]:
        yc = lunar.getYearCal(y)
        jq = yc.getJieQi()
        for i in range(0, 24, 2):  # 仅获取节
            jie = jq[i]
            jie_dt = datetime(jie.Y, jie.M, jie.D, jie.h, jie.m, jie.s)
            month_idx = (i // 2)  # 小寒为0，立春为1，惊蛰为2...
            jie_list.append((jie_dt, month_idx))

    jie_list.sort(key=lambda x: x[0])
    selected_jie = next((j for j in reversed(
        jie_list) if j[0] <= input_dt), None)

    if selected_jie is None:
        raise ValueError("未找到节气")

    month_zhi_idx = (selected_jie[1] + 10) % 12  # 小寒(0)->丑(1), 立春(1)->寅(2)...
    month_zhi = DIZHI[month_zhi_idx]

    # 计算月干
    year_gan_idx = TIANGAN.index(year_gan)
    if year_gan_idx in [0, 5]:
        start_gan = 2  # 甲己之岁丙作首
    elif year_gan_idx in [1, 6]:
        start_gan = 4  # 乙庚之岁戊为头
    elif year_gan_idx in [2, 7]:
        start_gan = 6  # 丙辛必定寻庚起
    elif year_gan_idx in [3, 8]:
        start_gan = 8  # 丁壬壬位顺行流
    else:
        start_gan = 0  # 戊癸甲寅好追求

    month_seq = (month_zhi_idx - 2) % 12  # 寅月为0
    month_gan = TIANGAN[(start_gan + month_seq) % 10]
    return month_gan, month_zhi


def get_day_gan_zhi(year, month, day):
    day = sxtwl.getDay(year, month, day)
    lunar_day = day.getLunarDay()
    return TIANGAN[lunar_day.iGan], DIZHI[lunar_day.iZhi]


def get_hour_gan_zhi(day_gan, hour):
    zhi_idx = ((hour + 1) // 2) % 12
    day_gan_idx = TIANGAN.index(day_gan)

    if day_gan_idx in [0, 5]:
        start = 0
    elif day_gan_idx in [1, 6]:
        start = 2
    elif day_gan_idx in [2, 7]:
        start = 4
    elif day_gan_idx in [3, 8]:
        start = 6
    else:
        start = 8

    gan_idx = (start + zhi_idx) % 10
    return TIANGAN[gan_idx], DIZHI[zhi_idx]


def calculate_bazi(year, month, day, hour, minute):
    try:
        yg, yz = get_year_gan_zhi(year, month, day, hour, minute)
        mg, mz = get_month_gan_zhi(year, month, day, hour, minute, yg)
        dg, dz = get_day_gan_zhi(year, month, day)
        hg, hz = get_hour_gan_zhi(dg, hour)

        return {
            "年柱": yg + yz,
            "月柱": mg + mz,
            "日柱": dg + dz,
            "时柱": hg + hz
        }
    except Exception as e:
        return f"错误：{str(e)}，请检查输入日期是否合法"


# 示例使用
if __name__ == "__main__":
    # 输入公历日期和时间（请使用24小时制）
    bazi = calculate_bazi(1990, 2, 4, 10, 30)
    print(bazi)
