"""
定义 天干到元素的映射表：
    甲、乙 → 木
    丙、丁 → 火
    戊、己 → 土
    庚、辛 → 金
    壬、癸 → 水

定义 地支的天干组成表：
    子 → [癸]                     # 1个天干
    丑 → [己, 癸, 辛]            # 3个天干（顺序：己→癸→辛）
    寅 → [甲, 丙, 戊]            # 3个天干（顺序：甲→丙→戊）
    卯 → [乙]                    # 1个天干
    辰 → [戊, 乙, 癸]            # 3个天干（顺序：戊→乙→癸）
    巳 → [丙, 庚, 戊]            # 3个天干（顺序：丙→庚→戊）
    午 → [丁, 己]                # 2个天干（顺序：丁→己）
    未 → [己, 丁, 乙]            # 3个天干（顺序：己→丁→乙）
    申 → [庚, 壬, 戊]            # 3个天干（顺序：庚→壬→戊）
    酉 → [辛]                    # 1个天干
    戌 → [戊, 辛, 丁]            # 3个天干（顺序：戊→辛→丁）
    亥 → [壬, 甲]                # 2个天干（顺序：壬→甲）定义 四柱地支总分：
    年柱地支总分 = 100
    月柱地支总分 = 150
    日柱地支总分 = 100
    时柱地支总分 = 100

输入八字的天干（4个字符）：例 [甲, 乙, 丙, 丁]
输入八字的地支（4个字符）：例 [寅, 卯, 午, 未]

初始化五行分数：
    金 = 0, 木 = 0, 水 = 0, 火 = 0, 土 = 0

遍历每个天干：
    根据映射表找到对应五行
    该五行分数 += 40（每个天干固定40分）

遍历四柱（年、月、日、时）：
    当前地支总分 = 对应柱的总分（100/150/100/100）
    获取该地支对应的天干列表

    if 天干数量 == 1:
        分数分配 = [当前地支总分]
    elif 天干数量 == 2:
        第一分数 = floor(当前地支总分 × 0.7)
        第二分数 = 当前地支总分 - 第一分数
    elif 天干数量 == 3:
        第一分数 = floor(当前地支总分 × 0.7)
        第二分数 = floor(当前地支总分 × 0.2)
        第三分数 = 当前地支总分 - 第一分数 - 第二分数

    按顺序将分数累加到对应五行

总分数 = 金 + 木 + 水 + 火 + 土
断言 总分数 == 610，否则报错

原始比例 = 各五行分数 / 610
互补比例 = 1 - 原始比例
归一化互补比例 = 互补比例 / 互补比例总和

分配24颗珠子：
    按归一化互补比例计算每个五行的理论数量（含小数）
    使用最大余数法分配整数颗数（先取整，再按余数补足剩余）


使用示例：输入：
    天干 = [甲, 乙, 丙, 丁]
    地支 = [寅, 卯, 午, 未]

计算过程：
    天干得分：木(40×2) + 火(40×2) = 80木 + 80火
    地支得分（示例）：
        年柱寅 → 木+70, 火+20, 土+10
        月柱卯 → 木+105
        日柱午 → 火+105, 土+45
        时柱未 → 土+105, 火+20, 木+15
    总分验证：610 → 通过
    珠子分配：按互补比例计算后分配24颗珠子
"""
import math

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
        "珠子分配": bead_allocation
    }

def main():
    """主函数，处理用户输入并显示结果"""
    print("八字五行珠子分配计算器")
    print("请按年、月、日、时的顺序输入:")

    # 获取用户输入
    heavenly_stems = input("请输入四柱天干 (如：甲乙丙丁): ")
    earthly_branches = input("请输入四柱地支 (如：寅卯午未): ")

    # 验证输入长度
    if len(heavenly_stems) != 4 or len(earthly_branches) != 4:
        print("错误: 天干和地支都应该是4个字符")
        return

    # 转换为列表
    stems = list(heavenly_stems)
    branches = list(earthly_branches)

    try:
        result = calculate_beads_distribution(stems, branches)

        # 显示结果
        print("\n===== 计算结果 =====")
        print("五行分数:")
        for element, score in result["五行分数"].items():
            print(f"  {element}: {score}")

        print("\n原始比例:")
        for element, ratio in result["原始比例"].items():
            print(f"  {element}: {ratio:.4f}")

        print("\n互补比例 (归一化):")
        for element, ratio in result["互补比例"].items():
            print(f"  {element}: {ratio:.4f}")

        print("\n珠子分配 (共24颗):")
        for element, count in result["珠子分配"].items():
            print(f"  {element}: {count}颗")

        # 验证珠子总数
        total_beads = sum(result["珠子分配"].values())
        print(f"\n珠子总数: {total_beads}")

    except Exception as e:
        print(f"计算出错: {e}")

if __name__ == "__main__":
    main()