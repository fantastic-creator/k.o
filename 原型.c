#include <stdio.h>
#include <string.h>
#include <math.h>
#include <time.h>

// 天干和地支
const char* heavenly_stems[] = {"甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"};
const char* earthly_branches[] = {"子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"};

// 天干和地支对应的五行
const char* heavenly_stems_elements[] = {"木", "木", "火", "火", "土", "土", "金", "金", "水", "水"};
const char* earthly_branches_elements[] = {"水", "土", "木", "木", "土", "火", "火", "土", "金", "金", "土", "水"};

// 二十四节气 (按照公历月份排列，每月两个)
const char* solar_terms[] = {
    "小寒", "大寒", // 1月
    "立春", "雨水", // 2月
    "惊蛰", "春分", // 3月
    "清明", "谷雨", // 4月
    "立夏", "小满", // 5月
    "芒种", "夏至", // 6月
    "小暑", "大暑", // 7月
    "立秋", "处暑", // 8月
    "白露", "秋分", // 9月
    "寒露", "霜降", // 10月
    "立冬", "小雪", // 11月
    "大雪", "冬至"  // 12月
};

// 节气的平均日期 (仅作为参考，实际需要天文计算)
const int solar_term_days[] = {
    6, 20,   // 1月 小寒、大寒
    4, 19,   // 2月 立春、雨水
    6, 21,   // 3月 惊蛰、春分
    5, 20,   // 4月 清明、谷雨
    6, 21,   // 5月 立夏、小满
    6, 21,   // 6月 芒种、夏至
    7, 23,   // 7月 小暑、大暑
    8, 23,   // 8月 立秋、处暑
    8, 23,   // 9月 白露、秋分
    8, 24,   // 10月 寒露、霜降
    8, 22,   // 11月 立冬、小雪
    7, 22    // 12月 大雪、冬至
};

// 计算公历日期的儒略日数
double julian_day(int year, int month, int day) {
    int a = (14 - month) / 12;
    int y = year + 4800 - a;
    int m = month + 12 * a - 3;

    double jd = day + (153 * m + 2) / 5 + 365 * y + y / 4 - y / 100 + y / 400 - 32045.5;

    return jd;
}

// 获取某年某月的节气日期 (简化版本，实际需要天文计算)
int get_solar_term_day(int year, int month, int term_index) {
    // term_index: 0=节气1, 1=节气2
    int base_day = solar_term_days[(month-1)*2 + term_index];

    // 对特殊年份进行修正 (简化处理，实际应根据天文算法)
    int correction = 0;
    if (year >= 2000) {
        // 简化的修正值，实际应该基于天文算法
        correction = (year - 2000) / 100;
    }

    return base_day + correction;
}

// 判断某日期是否在立春后
int is_after_lichun(int year, int month, int day) {
    int lichun_month = 2; // 立春通常在2月
    int lichun_day = get_solar_term_day(year, 2, 0);

    if (month > lichun_month) return 1;
    if (month < lichun_month) return 0;
    return day >= lichun_day;
}

// 计算年干支 (考虑立春)
void year_gz(int year, int month, int day, int *stem, int *branch) {
    // 如果在立春前，应算作上一年
    if (month <= 2 && !is_after_lichun(year, month, day)) {
        year--;
    }

    *stem = (year - 4) % 10;
    *branch = (year - 4) % 12;

    if (*stem < 0) *stem += 10;
    if (*branch < 0) *branch += 12;
}

// 确定节气月
int get_solar_term_month(int year, int month, int day) {
    // 首先检查是否在当月的第二个节气之后，如果是，月份可能要增加
    int second_term_day = get_solar_term_day(year, month, 1);

    // 如果在第二个节气后，且不是12月，月份加1
    if (day > second_term_day && month < 12) {
        return month + 1;
    }

    // 如果在当月第一个节气之前，且不是1月，月份可能要减少
    if (month > 1) {
        int first_term_day = get_solar_term_day(year, month, 0);
        if (day < first_term_day) {
            return month - 1;
        }
    }

    return month;
}

// 计算月干支 (考虑节气)
void month_gz(int year, int month, int day, int *stem, int *branch) {
    int year_stem, year_branch;

    // 计算年干支，用于月干计算
    year_gz(year, month, day, &year_stem, &year_branch);

    // 确定节气月
    int solar_month = get_solar_term_month(year, month, day);

    // 月支计算: 正月起寅
    *branch = (solar_month + 1) % 12;
    if (*branch == 0) *branch = 12;
    *branch = (*branch + 1) % 12;

    // 月干计算: 年干确定月干起始值
    int base_stem = (year_stem % 5) * 2;
    *stem = (base_stem + solar_month - 1) % 10;

    if (*stem < 0) *stem += 10;
}

// 计算日干支
void day_gz(int year, int month, int day, int *stem, int *branch) {
    // 使用较准确的基准日: 1900年1月31日为庚子日
    double base_date = julian_day(1900, 1, 31);
    double current_date = julian_day(year, month, day);

    // 计算日期差
    int days_diff = (int)round(current_date - base_date);

    // 转换为干支索引，庚子日: 干="庚"(6), 支="子"(0)
    *stem = (6 + days_diff) % 10;
    *branch = (0 + days_diff) % 12;

    if (*stem < 0) *stem += 10;
    if (*branch < 0) *branch += 12;
}

// 计算时干支 (考虑日跨越)
void hour_gz(int day_stem, int hour, int *stem, int *branch) {
    // 子时从23点开始，是新的一天的开始
    int day_adjustment = 0;
    if (hour >= 23) {
        // 23:00-23:59属于子时，是新一天的开始
        day_adjustment = 1;
    }

    // 调整日干
    day_stem = (day_stem + day_adjustment) % 10;

    // 将小时映射到地支 (子时是第一个时辰)
    if (hour == 23) {
        *branch = 0; // 子时 (23:00-00:59)
    } else {
        *branch = ((hour + 1) / 2) % 12;
    }

    // 根据日干确定时干的起始值
    int start_stem = (day_stem * 2) % 10;
    *stem = (start_stem + *branch) % 10;
}

int main() {
    int year, month, day, hour;
    printf("请输入年月日时 (格式: YYYY.MM.DD.HH): ");

    if (scanf("%d.%d.%d.%d", &year, &month, &day, &hour) != 4) {
        printf("输入格式错误!\n");
        return 1;
    }

    // 检查日期和时间的有效性
    if (month < 1 || month > 12 || day < 1 || day > 31 || hour < 0 || hour > 23) {
        printf("输入的日期或时间无效!\n");
        return 1;
    }

    // 计算八字四柱
    int y_stem, y_branch, m_stem, m_branch, d_stem, d_branch, h_stem, h_branch;

    // 计算年柱 (考虑立春)
    year_gz(year, month, day, &y_stem, &y_branch);

    // 计算月柱 (考虑节气)
    month_gz(year, month, day, &m_stem, &m_branch);

    // 计算日柱
    day_gz(year, month, day, &d_stem, &d_branch);

    // 计算时柱 (考虑日跨越)
    hour_gz(d_stem, hour, &h_stem, &h_branch);

    // 获取对应的五行
    const char* y_stem_element = heavenly_stems_elements[y_stem];
    const char* y_branch_element = earthly_branches_elements[y_branch];
    const char* m_stem_element = heavenly_stems_elements[m_stem];
    const char* m_branch_element = earthly_branches_elements[m_branch];
    const char* d_stem_element = heavenly_stems_elements[d_stem];
    const char* d_branch_element = earthly_branches_elements[d_branch];
    const char* h_stem_element = heavenly_stems_elements[h_stem];
    const char* h_branch_element = earthly_branches_elements[h_branch];

    // 输出八字
    printf("八字: %s%s %s%s %s%s %s%s\n",
           heavenly_stems[y_stem], earthly_branches[y_branch],
           heavenly_stems[m_stem], earthly_branches[m_branch],
           heavenly_stems[d_stem], earthly_branches[d_branch],
           heavenly_stems[h_stem], earthly_branches[h_branch]);

    // 输出五行
    printf("五行: %s%s %s%s %s%s %s%s\n",
           y_stem_element, y_branch_element,
           m_stem_element, m_branch_element,
           d_stem_element, d_branch_element,
           h_stem_element, h_branch_element);

    // 统计五行频次
    int wood_count = 0, fire_count = 0, earth_count = 0, metal_count = 0, water_count = 0;

    const char* elements[] = {
        y_stem_element, y_branch_element,
        m_stem_element, m_branch_element,
        d_stem_element, d_branch_element,
        h_stem_element, h_branch_element
    };

    for (int i = 0; i < 8; i++) {
        if (strcmp(elements[i], "木") == 0) wood_count++;
        else if (strcmp(elements[i], "火") == 0) fire_count++;
        else if (strcmp(elements[i], "土") == 0) earth_count++;
        else if (strcmp(elements[i], "金") == 0) metal_count++;
        else if (strcmp(elements[i], "水") == 0) water_count++;
    }

    printf("\n五行统计:\n");
    printf("木: %d\n", wood_count);
    printf("火: %d\n", fire_count);
    printf("土: %d\n", earth_count);
    printf("金: %d\n", metal_count);
    printf("水: %d\n", water_count);

    return 0;
}