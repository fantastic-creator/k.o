// 八字五行珠子分配计算器 - Arduino精简版
#include "bazi_beads.h"
#include "bazi_mappings.h" 

// 存储计算结果的结构体
struct BaziResult {
  byte heavenly_stems[4];   // 天干
  byte earthly_branches[4]; // 地支
  int element_scores[5];    // 五行分数 (金木水火土)
  byte beads_allocation[5]; // 珠子分配 (金木水火土)
};

// 计算八字
void calculateBazi(uint16_t year, uint8_t month, uint8_t day, uint8_t hour,
                   BaziResult &result) {
  // 1. 计算年柱 (需要考虑立春)
  uint8_t lichun_day = 0;
  if (year >= 1950 && year <= 2050) {
    lichun_day = LICHUN_DAYS[year - 1950];
  } else {
    lichun_day = 4; // 默认2月4日
  }

  // 判断是否过立春
  bool afterLichun = false;
  if (month > 2 || (month == 2 && day >= lichun_day)) {
    afterLichun = true;
  }

  // 根据是否过立春确定年份
  uint16_t lunarYear = year;
  if (!afterLichun) {
    lunarYear = year - 1;
  }

  // 计算年干支
  uint8_t year_offset = lunarYear - BASE_YEAR;
  result.heavenly_stems[0] = (BASE_YEAR_STEM + year_offset) % 10;
  result.earthly_branches[0] = (BASE_YEAR_BRANCH + year_offset) % 12;

  // 2. 计算月柱
  // 根据年干和月份确定月干支
  uint8_t yearStem = result.heavenly_stems[0];
  uint8_t monthBase = MONTH_STEM_BASE[yearStem];

  // 月的地支顺序是：寅卯辰巳午未申酉戌亥子丑
  // 即正月是寅月，二月是卯月，依次类推
  // 我们需要转换公历月到农历月
  uint8_t lunarMonth = 0;

  // 简单的公历月到农历月的大致映射 (考虑立春)
  if (afterLichun) {
    lunarMonth = month + 1;
    if (lunarMonth > 12)
      lunarMonth = 1;
  } else {
    lunarMonth = month;
    if (lunarMonth == 1)
      lunarMonth = 12;
  }

  // 农历月对应的地支索引
  result.earthly_branches[1] = (lunarMonth + 1) % 12;

  // 确定月干
  result.heavenly_stems[1] = (monthBase + lunarMonth - 1) % 10;

  // 3. 计算日柱
  uint32_t dayNum = dayNumber(year, month, day);
  getDayPillar(dayNum, result.heavenly_stems[2], result.earthly_branches[2]);

  // 4. 计算时柱
  getHourPillar(hour, result.heavenly_stems[2], result.heavenly_stems[3],
                result.earthly_branches[3]);
}

// 计算五行得分和珠子分配
void calculateBeadsDistribution(const BaziResult &bazi, BaziResult &result) {
  // 复制八字信息
  for (int i = 0; i < 4; i++) {
    result.heavenly_stems[i] = bazi.heavenly_stems[i];
    result.earthly_branches[i] = bazi.earthly_branches[i];
  }

  // 初始化五行分数
  for (int i = 0; i < 5; i++) {
    result.element_scores[i] = 0;
  }

  // 1. 计算天干分数
  for (int i = 0; i < 4; i++) {
    byte element = STEM_TO_ELEMENT[result.heavenly_stems[i]];
    result.element_scores[element] += 40;
  }

  // 2. 计算地支分数
  for (int i = 0; i < 4; i++) {
    int branch_score = BRANCH_TOTAL_SCORES[i];
    byte branch_index = result.earthly_branches[i];
    byte stem_count = BRANCH_STEM_COUNT[branch_index];

    // 分配分数
    int scores[3] = {0, 0, 0};

    if (stem_count == 1) {
      scores[0] = branch_score;
    } else if (stem_count == 2) {
      scores[0] = (branch_score * 7) / 10;  // 70%
      scores[1] = branch_score - scores[0]; // 剩余部分
    } else if (stem_count == 3) {
      scores[0] = (branch_score * 7) / 10;              // 70%
      scores[1] = (branch_score * 2) / 10;              // 20%
      scores[2] = branch_score - scores[0] - scores[1]; // 剩余部分
    }

    // 分配到对应五行
    for (int j = 0; j < stem_count; j++) {
      byte stem_code = BRANCH_STEMS[branch_index][j];
      if (stem_code != 255) { // 255是无效值
        byte element = STEM_TO_ELEMENT[stem_code];
        result.element_scores[element] += scores[j];
      }
    }
  }

  // 3. 计算珠子分配
  // 计算总分
  int total_score = 0;
  for (int i = 0; i < 5; i++) {
    total_score += result.element_scores[i];
  }

  // 计算原始比例和互补比例
  float original_ratios[5];
  float complementary_ratios[5];
  float comp_total = 0;

  for (int i = 0; i < 5; i++) {
    original_ratios[i] = (float)result.element_scores[i] / total_score;
    complementary_ratios[i] = 1.0 - original_ratios[i];
    comp_total += complementary_ratios[i];
  }

  // 归一化互补比例
  float normalized_comp_ratios[5];
  for (int i = 0; i < 5; i++) {
    normalized_comp_ratios[i] = complementary_ratios[i] / comp_total;
  }

  // 分配24颗珠子
  const byte total_beads = 24;
  float theoretical_beads[5];

  // 初始分配(取整数部分)
  byte allocated_beads = 0;
  for (int i = 0; i < 5; i++) {
    theoretical_beads[i] = normalized_comp_ratios[i] * total_beads;
    result.beads_allocation[i] = (byte)theoretical_beads[i];
    allocated_beads += result.beads_allocation[i];
  }

  // 计算剩余珠子数量并按余数大小分配
  byte remaining_beads = total_beads - allocated_beads;

  // 按余数大小排序并分配剩余珠子
  if (remaining_beads > 0) {
    // 创建索引数组并计算余数
    byte indices[5] = {0, 1, 2, 3, 4};
    float remainders[5];

    for (int i = 0; i < 5; i++) {
      remainders[i] = theoretical_beads[i] - (int)theoretical_beads[i];
    }

    // 冒泡排序，按余数从大到小排序
    for (int i = 0; i < 4; i++) {
      for (int j = 0; j < 4 - i; j++) {
        if (remainders[indices[j]] < remainders[indices[j + 1]]) {
          byte temp = indices[j];
          indices[j] = indices[j + 1];
          indices[j + 1] = temp;
        }
      }
    }

    // 分配剩余珠子
    for (int i = 0; i < remaining_beads; i++) {
      result.beads_allocation[indices[i]]++;
    }
  }
}

void setup() {
  Serial.begin(9600);
  Serial.println(F("八字五行珠子分配计算器 - Arduino精简版"));
  Serial.println(F("============================="));
  Serial.println(F("请输入公历日期时间 (YYYYMMDDHH)"));
  Serial.println(F("例如: 19850312 (1985年3月12日0时)"));
}

void loop() {
  // 检查是否有输入
  if (Serial.available() >= 8) {
    // 读取日期时间 (YYYYMMDDHH)
    char input[11]; // 多一位存储结束符
    int i = 0;

    while (Serial.available() && i < 10) {
      char c = Serial.read();
      if (c >= '0' && c <= '9') {
        input[i++] = c;
      }
    }
    input[i] = '\0';

    // 清空多余输入
    while (Serial.available()) {
      Serial.read();
    }

    // 解析日期和时间
    uint16_t year = 0;
    uint8_t month = 0, day = 0, hour = 0;

    if (i >= 8) {
      year = (input[0] - '0') * 1000 + (input[1] - '0') * 100 +
             (input[2] - '0') * 10 + (input[3] - '0');
      month = (input[4] - '0') * 10 + (input[5] - '0');
      day = (input[6] - '0') * 10 + (input[7] - '0');

      if (i >= 10) {
        hour = (input[8] - '0') * 10 + (input[9] - '0');
      }

      // 验证输入合法性
      if (year < 1950 || year > 2050 || month < 1 || month > 12 || day < 1 ||
          day > 31 || hour > 23) {
        Serial.println(F("输入数据错误! 年份必须在1950-2050之间"));
        return;
      }

      // 计算八字
      BaziResult bazi;
      calculateBazi(year, month, day, hour, bazi);

      // 计算珠子分配
      BaziResult result;
      calculateBeadsDistribution(bazi, result);

      // 显示八字结果
      Serial.println(F("\n===== 八字信息 ====="));
      Serial.print(F("公历: "));
      Serial.print(year);
      Serial.print(F("年"));
      Serial.print(month);
      Serial.print(F("月"));
      Serial.print(day);
      Serial.print(F("日 "));
      Serial.print(hour);
      Serial.println(F("时"));

      Serial.print(F("八字: "));
      const char *pillar_names[4] = {"年柱", "月柱", "日柱", "时柱"};
      for (int i = 0; i < 4; i++) {
        Serial.print(pillar_names[i]);
        Serial.print(F("("));
        Serial.print(HEAVENLY_STEMS[bazi.heavenly_stems[i]]);
        Serial.print(EARTHLY_BRANCHES[bazi.earthly_branches[i]]);
        Serial.print(F(") "));
      }
      Serial.println();

      // 显示五行分数
      Serial.println(F("\n===== 五行分数 ====="));
      const char *element_names[5] = {"金", "木", "水", "火", "土"};
      for (int i = 0; i < 5; i++) {
        Serial.print(element_names[i]);
        Serial.print(F(": "));
        Serial.print(result.element_scores[i]);
        Serial.println(F("分"));
      }

      // 显示珠子分配
      Serial.println(F("\n===== 珠子分配 (共24颗) ====="));
      for (int i = 0; i < 5; i++) {
        Serial.print(element_names[i]);
        Serial.print(F(": "));
        Serial.print(result.beads_allocation[i]);
        Serial.println(F("颗"));
      }

      Serial.println(F("\n============================="));
      Serial.println(F("请输入下一个日期 (YYYYMMDDHH):"));
    }
  }

  delay(100);
}