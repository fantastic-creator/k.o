import math
import re

# 定义表达式常量
EXPRESSION = "sin(2'3'4') + cos(45'30') - tan(60)"

def dms_to_decimal(degrees, minutes=0, seconds=0):
    """
    将度分秒格式转换为十进制度格式。
    :param degrees: 度数
    :param minutes: 分（默认为 0）
    :param seconds: 秒（默认为 0）
    :return: 十进制度格式的角度
    """
    decimal_degrees = abs(degrees) + minutes / 60 + seconds / 3600
    return decimal_degrees if degrees >= 0 else -decimal_degrees

def parse_dms(dms_str):
    """
    解析多种格式的角度字符串并转换为十进制度格式。
    支持格式：
    - 纯度数: "30"
    - 度分: "30'23'"
    - 度分秒: "55'44'0'"
    :param dms_str: 角度字符串
    :return: (十进制度格式的角度, 角度格式类型, 解析后的部分)
    """
    # 检查是否为纯度数格式（无单引号）
    if "'" not in dms_str:
        return float(dms_str), "degrees", [float(dms_str)]

    # 检查是度分格式还是度分秒格式
    parts = dms_str.strip("'").split("'")

    if len(parts) == 2:
        # 度分格式
        degrees = int(parts[0])
        minutes = int(parts[1])
        return dms_to_decimal(degrees, minutes), "dm", [degrees, minutes]
    elif len(parts) == 3:
        # 度分秒格式
        degrees = int(parts[0])
        minutes = int(parts[1])
        seconds = int(parts[2])
        return dms_to_decimal(degrees, minutes, seconds), "dms", [degrees, minutes, seconds]
    else:
        raise ValueError(f"Invalid angle format: {dms_str}")

def increase_angle_precision(angle_str):
    """
    根据角度格式增加角度的精度。
    :param angle_str: 角度字符串
    :return: (增加精度后的十进制度, 原始十进制度)
    """
    # 解析角度字符串
    try:
        original_value, angle_format, angle_parts = parse_dms(angle_str)
    except ValueError:
        # 如果解析失败，尝试作为普通浮点数
        try:
            original_value = float(angle_str)
            angle_format = "degrees"
            angle_parts = [original_value]
        except ValueError:
            raise ValueError(f"Invalid angle format: {angle_str}")

    # 根据格式增加精度
    if angle_format == "degrees":
        # 对于纯度数，增加1度
        increased_value = original_value + 1
    elif angle_format == "dm":
        # 对于度分格式，分钟加1
        degrees, minutes = angle_parts
        minutes += 1
        if minutes >= 60:
            degrees += 1
            minutes = 0
        increased_value = dms_to_decimal(degrees, minutes)
    elif angle_format == "dms":
        # 对于度分秒格式，秒数加1
        degrees, minutes, seconds = angle_parts
        seconds += 1
        if seconds >= 60:
            minutes += 1
            seconds = 0
            if minutes >= 60:
                degrees += 1
                minutes = 0
        increased_value = dms_to_decimal(degrees, minutes, seconds)

    return increased_value, original_value

def calculate_trig_with_precision(func, angle_str):
    """
    根据新规则计算三角函数结果的精度。
    :param func: 三角函数 (如 math.sin, math.cos, math.tan)
    :param angle_str: 角度字符串
    :return: 修约后的结果
    """
    # 如果参数是算术表达式，先计算出结果
    if any(op in angle_str for op in ['+', '-', '*', '/', '(', ')']):
        angle_value = evaluate_expression(angle_str)
        angle_str = str(angle_value)

    # 增加角度精度
    increased_angle, original_angle = increase_angle_precision(angle_str)

    # 转换为弧度并计算结果
    original_radians = math.radians(original_angle)
    increased_radians = math.radians(increased_angle)

    original_result = func(original_radians)
    increased_result = func(increased_radians)

    # 比较两次结果，找到变化的那一位
    original_str = f"{original_result:.15f}"  # 保留足够多的小数位
    increased_str = f"{increased_result:.15f}"

    # 找到结果变化的那一位
    for i in range(len(original_str)):
        if i < len(increased_str) and original_str[i] != increased_str[i]:
            # 修约到变化的那一位
            decimal_pos = original_str.index('.')
            significant_digits = i - decimal_pos
            if significant_digits >= 0:
                return round(original_result, significant_digits)
            else:
                return round(original_result, 0)

    # 如果完全一致，返回原始结果（保留4位小数作为默认）
    return round(original_result, 4)

def round_to_significant_digits(value, digits):
    """
    将数字修约到指定的有效数字位数。
    :param value: 输入值
    :param digits: 有效数字位数
    :return: 修约后的值
    """
    if value == 0:
        return 0

    # 获取数值的量级
    scale = math.floor(math.log10(abs(value)))

    # 将值缩放，使第一位数在个位上
    scaled = value / (10 ** scale)

    # 修约到指定的有效数字位数
    rounded = round(scaled, digits - 1)

    # 将值缩放回原来的量级
    return rounded * (10 ** scale)

def get_significant_digits(value):
    """
    获取一个数的有效数字位数。
    :param value: 输入值
    :return: 有效数字位数
    """
    value_str = f"{value:.15g}".strip("0").replace(".", "").replace("-", "")
    return len(value_str)

def evaluate_expression(expression):
    """
    计算给定表达式，确保每次运算符合有效数字规则。
    :param expression: 输入表达式
    :return: 计算结果
    """
    # 支持的运算符和函数
    operators = {
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x * y,
        '/': lambda x, y: x / y,
        '^': lambda x, y: x ** y,
    }
    functions = {
        'sin': lambda x: calculate_trig_with_precision(math.sin, x),
        'cos': lambda x: calculate_trig_with_precision(math.cos, x),
        'tan': lambda x: calculate_trig_with_precision(math.tan, x),
        'log10': lambda x: round_to_significant_digits(math.log10(float(x)), get_significant_digits(float(x))),
    }

    # 预处理：处理DMS格式的角度
    def process_dms_angles(expr):
        # 找到所有DMS格式的角度并替换为十进制度
        pattern = r"(\d+'\d+'(?:\d+')?)|(\d+'\d+)"

        def replace_dms(match):
            dms_str = match.group(0)
            decimal_value, _, _ = parse_dms(dms_str)
            return str(decimal_value)

        return re.sub(pattern, replace_dms, expr)

    # 预处理：处理函数调用
    def process_functions(expr):
        # 处理标准函数调用格式 func(arg)
        pattern = r'(\w+)\(([^)]+)\)'

        while re.search(pattern, expr):
            expr = re.sub(pattern, lambda m: str(evaluate_function(m)), expr)

        # 处理直接函数调用格式 func60.0
        for func_name in functions:
            direct_pattern = f'{func_name}([0-9.]+)'
            if re.search(direct_pattern, expr):
                expr = re.sub(direct_pattern,
                             lambda m: str(functions[func_name](m.group(1))),
                             expr)

        return expr

    # 处理括号内的子表达式
    def process_parentheses(expr):
        # 处理括号前先处理DMS格式角度
        expr = process_dms_angles(expr)

        # 找到最内层的括号
        while '(' in expr:
            # 找到最内层的左括号位置
            left_pos = expr.rfind('(')
            # 找到对应的右括号位置
            right_pos = expr.find(')', left_pos)
            if right_pos == -1:
                raise ValueError(f"Unmatched parentheses in expression: {expr}")

            # 计算括号内的子表达式
            sub_expr = expr[left_pos + 1:right_pos]

            # 先处理子表达式中的DMS格式角度
            sub_expr = process_dms_angles(sub_expr)

            # 处理子表达式中的函数调用
            sub_expr = process_functions(sub_expr)

            # 如果子表达式中还有运算符，继续计算
            if any(op in sub_expr for op in ['+', '-', '*', '/', '^']):
                sub_result = evaluate_simple_expression(sub_expr)
            else:
                # 尝试将子表达式直接转换为浮点数
                try:
                    sub_result = float(sub_expr)
                except ValueError:
                    # 可能是函数调用
                    sub_result = process_functions(sub_expr)

            # 替换原表达式中的括号部分
            expr = expr[:left_pos] + str(sub_result) + expr[right_pos + 1:]

        return expr

    # 解析表达式中的函数调用
    def evaluate_function(match):
        func_name = match.group(1)
        arg = match.group(2).strip()

        if func_name in functions:
            try:
                result = functions[func_name](arg)
                return str(result)  # 确保返回字符串
            except Exception as e:
                raise ValueError(f"Error evaluating function {func_name}({arg}): {str(e)}")
        raise ValueError(f"Unsupported function: {func_name}")

    # 为不同运算符创建不同的处理函数
    def evaluate_power(match):
        left = float(match.group(1))
        right = float(match.group(2))
        result = operators['^'](left, right)

        # 对于幂运算，结果的有效数字位数等于底数的有效数字位数
        left_digits = get_significant_digits(left)

        # 修改：使用底数的有效数字位数，而不是取最小值
        result = round_to_significant_digits(result, left_digits)
        return str(result)

    def evaluate_mult_div(match):
        left = float(match.group(1))
        operator = match.group(2)
        right = float(match.group(3))
        result = operators[operator](left, right)
        left_digits = get_significant_digits(left)
        right_digits = get_significant_digits(right)
        result = round_to_significant_digits(result, min(left_digits, right_digits))
        return str(result)

    def evaluate_add_sub(match):
        left = float(match.group(1))
        operator = match.group(2)
        right = float(match.group(3))
        result = operators[operator](left, right)
        left_digits = get_significant_digits(left)
        right_digits = get_significant_digits(right)
        result = round_to_significant_digits(result, min(left_digits, right_digits))
        return str(result)

    # 计算简单表达式（不含嵌套括号）
    def evaluate_simple_expression(expr):
        # 处理幂运算
        while re.search(r'([0-9.]+)\s*\^\s*([0-9.]+)', expr):
            expr = re.sub(r'([0-9.]+)\s*\^\s*([0-9.]+)', evaluate_power, expr)

        # 处理乘除
        while re.search(r'([0-9.]+)\s*([*/])\s*([0-9.]+)', expr):
            expr = re.sub(r'([0-9.]+)\s*([*/])\s*([0-9.]+)', evaluate_mult_div, expr)

        # 处理加减
        while re.search(r'([0-9.]+)\s*([\+\-])\s*([0-9.]+)', expr):
            expr = re.sub(r'([0-9.]+)\s*([\+\-])\s*([0-9.]+)', evaluate_add_sub, expr)

        return float(expr)

    # 开始处理表达式
    try:
        # 1. 处理括号
        expression = process_parentheses(expression)

        # 2. 处理函数（可能在括号处理后仍有函数调用）
        expression = process_functions(expression)

        # 3. 处理算术运算
        if any(op in expression for op in ['+', '-', '*', '/', '^']):
            expression = str(evaluate_simple_expression(expression))

        # 4. 返回结果
        return float(expression)
    except Exception as e:
        print(f"Error evaluating expression '{expression}': {str(e)}")
        raise

# 计算表达式
result = evaluate_expression(EXPRESSION)
print(f"表达式 {EXPRESSION} 的计算结果为: {result}")