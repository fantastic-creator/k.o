// Arduino 八字计算库 - 基于预计算表方法
#include <Arduino.h>

// 预定义数据
const char* HEAVENLY_STEMS[] = {"甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"};
const char* EARTHLY_BRANCHES[] = {"子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"};
const char* HEAVENLY_STEMS_ELEMENTS[] = {"木", "木", "火", "火", "土", "土", "金", "金", "水", "水"};
const char* EARTHLY_BRANCHES_ELEMENTS[] = {"水", "土", "木", "木", "土", "火", "火", "土", "金", "金", "土", "水"};
const char* SOLAR_TERMS[] = {"冬至", "小寒", "大寒", "立春", "雨水", "惊蛰", "春分", "清明", "谷雨",
                            "立夏", "小满", "芒种", "夏至", "小暑", "大暑", "立秋", "处暑", "白露",
                            "秋分", "寒露", "霜降", "立冬", "小雪", "大雪"};

// 日期结构
typedef struct {
  uint8_t month;
  uint8_t day;
} DateMD;

// 节气数据表 - 使用Python生成的数据
// 格式: [year-1960][term_index] = {month, day}
#include "solar_terms_table.h" // 这个文件需要通过Python预生成

// 日期到干支映射的基准日
const unsigned long BASE_DATE_DAYS = 693596; // 1900-01-31的天数（以0000-01-01为起点）
const uint8_t BASE_GAN = 6;  // 庚
const uint8_t BASE_ZHI = 0;  // 子

// 获取一个日期对应的天数（自0000-01-01以来的天数）
unsigned long date_to_days(int year, int month, int day) {
  // 简化的日期到天数转换
  if (month < 3) {
    year--;
    month += 12;
  }
  return 365 * year + year/4 - year/100 + year/400 + (153 * month - 457) / 5 + day - 306;
}

// 获取两个日期之间的天数
long days_between(int year1, int month1, int day1, int year2, int month2, int day2) {
  unsigned long days1 = date_to_days(year1, month1, day1);
  unsigned long days2 = date_to_days(year2, month2, day2);
  return days2 - days1;
}

// 获取某年某月的天数
uint8_t days_in_month(int year, int month) {
  const uint8_t days[] = {0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
  if (month == 2 && ((year % 4 == 0 && year % 100 != 0) || year % 400 == 0)) {
    return 29;
  }
  return days[month];
}

// 查找某年某个节气的日期
DateMD get_solar_term_date(int year, uint8_t term_index) {
  if (year < 1960 || year > 2030 || term_index >= 24) {
    return {0, 0}; // 返回无效日期
  }
  return SOLAR_TERMS_TABLE[year-1960][term_index];
}

// 判断某日期是否在立春之后
bool is_after_lichun(int year, int month, int day) {
  DateMD lichun = get_solar_term_date(year, 3); // 立春是第3个节气

  if (month > lichun.month) return true;
  if (month < lichun.month) return false;
  return day >= lichun.day;
}

// 计算年干支
void year_gz(int year, int month, int day, uint8_t *stem, uint8_t *branch) {
  // 如果在立春前，算作上一年
  if (month <= 2 && !is_after_lichun(year, month, day)) {
    year--;
  }

  *stem = (year - 4) % 10;
  *branch = (year - 4) % 12;

  if (*stem < 0) *stem += 10;
  if (*branch < 0) *branch += 12;
}

// 确定节气月
uint8_t get_solar_term_month(int year, int month, int day) {
  DateMD term1, term2;
  uint8_t term_index1 = (month - 1) * 2 % 24;
  uint8_t term_index2 = (term_index1 + 1) % 24;

  term1 = get_solar_term_date(year, term_index1);
  term2 = get_solar_term_date(year, term_index2);

  if (day < term1.day) {
    if (month > 1) return month - 1;
  } else if (day > term2.day && term2.day > 0) {
    if (month < 12) return month + 1;
  }

  return month;
}

// 计算月干支
void month_gz(int year, int month, int day, uint8_t *stem, uint8_t *branch) {
  uint8_t year_stem, year_branch;

  // 计算年干支，用于月干计算
  year_gz(year, month, day, &year_stem, &year_branch);

  // 确定节气月
  uint8_t solar_month = get_solar_term_month(year, month, day);

  // 月支计算: 正月起寅
  *branch = (solar_month + 1) % 12;
  if (*branch == 0) *branch = 12;
  *branch = (*branch + 1) % 12;

  // 月干计算: 年干确定月干起始值
  uint8_t base_stem = (year_stem % 5) * 2;
  *stem = (base_stem + solar_month - 1) % 10;

  if (*stem < 0) *stem += 10;
}

// 计算日干支
void day_gz(int year, int month, int day, uint8_t *stem, uint8_t *branch) {
  // 计算与基准日期的天数差
  long diff_days = days_between(1900, 1, 31, year, month, day);

  // 计算干支索引
  *stem = (BASE_GAN + diff_days) % 10;
  *branch = (BASE_ZHI + diff_days) % 12;

  if (*stem < 0) *stem += 10;
  if (*branch < 0) *branch += 12;
}

// 计算时干支
void hour_gz(uint8_t day_stem, int hour, uint8_t *stem, uint8_t *branch) {
  // 时辰与地支对照表
  uint8_t hour_zhi;

  if (hour >= 23 || hour < 1) hour_zhi = 0; // 子时
  else if (hour < 3) hour_zhi = 1; // 丑时
  else if (hour < 5) hour_zhi = 2; // 寅时
  else if (hour < 7) hour_zhi = 3; // 卯时
  else if (hour < 9) hour_zhi = 4; // 辰时
  else if (hour < 11) hour_zhi = 5; // 巳时
  else if (hour < 13) hour_zhi = 6; // 午时
  else if (hour < 15) hour_zhi = 7; // 未时
  else if (hour < 17) hour_zhi = 8; // 申时
  else if (hour < 19) hour_zhi = 9; // 酉时
  else if (hour < 21) hour_zhi = 10; // 戌时
  else hour_zhi = 11; // 亥时

  *branch = hour_zhi;

  // 根据日干确定时干起始值
  // 甲己日起甲时，乙庚日起丙时，丙辛日起戊时，丁壬日起庚时，戊癸日起壬时
  const uint8_t day_stem_to_hour_stem[10] = {0, 2, 4, 6, 8, 0, 2, 4, 6, 8};
  uint8_t base_stem = day_stem_to_hour_stem[day_stem];
  *stem = (base_stem + hour_zhi) % 10;
}

class BaziCalculator {
private:
  int year;
  int month;
  int day;
  int hour;

  uint8_t y_stem, y_branch;
  uint8_t m_stem, m_branch;
  uint8_t d_stem, d_branch;
  uint8_t h_stem, h_branch;

public:
  BaziCalculator(int y, int m, int d, int h) {
    year = y;
    month = m;
    day = d;
    hour = h;

    // 计算八字四柱
    year_gz(year, month, day, &y_stem, &y_branch);
    month_gz(year, month, day, &m_stem, &m_branch);
    day_gz(year, month, day, &d_stem, &d_branch);
    hour_gz(d_stem, hour, &h_stem, &h_branch);
  }

  // 获取年干支
  void getYearGZ(uint8_t *stem, uint8_t *branch) {
    *stem = y_stem;
    *branch = y_branch;
  }

  // 获取月干支
  void getMonthGZ(uint8_t *stem, uint8_t *branch) {
    *stem = m_stem;
    *branch = m_branch;
  }

  // 获取日干支
  void getDayGZ(uint8_t *stem, uint8_t *branch) {
    *stem = d_stem;
    *branch = d_branch;
  }

  // 获取时干支
  void getHourGZ(uint8_t *stem, uint8_t *branch) {
    *stem = h_stem;
    *branch = h_branch;
  }

  // 打印八字 (串口输出)
  void printBazi() {
    Serial.print("八字: ");
    Serial.print(HEAVENLY_STEMS[y_stem]);
    Serial.print(EARTHLY_BRANCHES[y_branch]);
    Serial.print(" ");
    Serial.print(HEAVENLY_STEMS[m_stem]);
    Serial.print(EARTHLY_BRANCHES[m_branch]);
    Serial.print(" ");
    Serial.print(HEAVENLY_STEMS[d_stem]);
    Serial.print(EARTHLY_BRANCHES[d_branch]);
    Serial.print(" ");
    Serial.print(HEAVENLY_STEMS[h_stem]);
    Serial.print(EARTHLY_BRANCHES[h_branch]);
    Serial.println();
  }

  // 打印五行
  void printWuxing() {
    Serial.print("五行: ");
    Serial.print(HEAVENLY_STEMS_ELEMENTS[y_stem]);
    Serial.print(EARTHLY_BRANCHES_ELEMENTS[y_branch]);
    Serial.print(" ");
    Serial.print(HEAVENLY_STEMS_ELEMENTS[m_stem]);
    Serial.print(EARTHLY_BRANCHES_ELEMENTS[m_branch]);
    Serial.print(" ");
    Serial.print(HEAVENLY_STEMS_ELEMENTS[d_stem]);
    Serial.print(EARTHLY_BRANCHES_ELEMENTS[d_branch]);
    Serial.print(" ");
    Serial.print(HEAVENLY_STEMS_ELEMENTS[h_stem]);
    Serial.print(EARTHLY_BRANCHES_ELEMENTS[h_branch]);
    Serial.println();
  }

  // 统计五行
  void countWuxing() {
    int wood = 0, fire = 0, earth = 0, metal = 0, water = 0;

    // 统计天干五行
    switch(HEAVENLY_STEMS_ELEMENTS[y_stem][0]) {
      case '木': wood++; break;
      case '火': fire++; break;
      case '土': earth++; break;
      case '金': metal++; break;
      case '水': water++; break;
    }
    // ... 对其他天干地支重复相同操作

    Serial.println("\n五行统计:");
    Serial.print("木: "); Serial.println(wood);
    Serial.print("火: "); Serial.println(fire);
    Serial.print("土: "); Serial.println(earth);
    Serial.print("金: "); Serial.println(metal);
    Serial.print("水: "); Serial.println(water);
  }
};