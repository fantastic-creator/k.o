import sxtwl
import datetime
import struct
from tqdm import tqdm

# 配置参数
START_YEAR = 1960
END_YEAR = 2030
OUTPUT_FILE = "lunar_data.bin"

def pack_date(year, month, day):
    """将日期打包为3字节数据"""
    return struct.pack('!HBB', year, month, day)

def encode_lunar_info(lunar_day):
    """编码农历信息到4字节"""
    lunar_month = lunar_day.getLunarMonth()
    lunar_day_num = lunar_day.getLunarDay()
    is_leap = 1 if lunar_day.isLunarLeap() else 0

    # 获取节气信息
    jq_index = lunar_day.getJieQi() if lunar_day.hasJieQi() else 0xFF

    return struct.pack('!BBBB',
        (lunar_month & 0x0F) | ((is_leap & 0x01) << 4),
        lunar_day_num,
        jq_index,
        0  # 保留位
    )

def generate_data():
    total_days = (END_YEAR - START_YEAR + 1) * 365  # 近似值
    with open(OUTPUT_FILE, 'wb') as f:
        for year in tqdm(range(START_YEAR, END_YEAR + 1)):
            for month in range(1, 13):
                for day in range(1, 32):
                    try:
                        # 获取公历日期对象
                        solar_date = datetime.date(year, month, day)
                    except ValueError:
                        continue

                    # 计算农历信息
                    lunar_day = sxtwl.fromSolar(year, month, day)

                    # 打包数据
                    solar_packed = pack_date(year, month, day)
                    lunar_packed = encode_lunar_info(lunar_day)

                    # 写入文件
                    f.write(solar_packed + lunar_packed)

if __name__ == "__main__":
    print(f"生成农历数据 ({START_YEAR}-{END_YEAR})...")
    generate_data()
    print(f"数据已保存到 {OUTPUT_FILE}")