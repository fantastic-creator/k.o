import sxtwl
import json

def generate_solar_terms_table():
    # 生成1960-2030年间的二十四节气日期表
    start_year = 1960
    end_year = 2030

    # 输出C格式数组
    output = "// 预计算的节气表 (1960-2030)\n"
    output += "// 格式: [year-1960][term_index] = {month, day}\n"
    output += "const DateMD SOLAR_TERMS_TABLE[%d][24] = {\n" % (end_year - start_year + 1)

    for year in range(start_year, end_year + 1):
        output += "  { // %d年\n    " % year

        terms = []
        for i in range(24):
            # 获取该年的节气
            jqs = sxtwl.getJieQiByYear(year)
            jq = jqs[i]

            # 转换节气日期
            t = sxtwl.JD2DD(jq.jd)
            month = t.M
            day = t.D

            terms.append("{%d, %d}" % (month, day))

        output += ", ".join(terms)
        output += "\n  }%s\n" % ("," if year < end_year else "")

    output += "};\n"

    # 写入文件
    with open("solar_terms_table.h", "w") as f:
        f.write(output)

if __name__ == "__main__":
    generate_solar_terms_table()