#!/usr/bin/env python3
import csv
import codecs

# 读取CSV文件
courses = []
with open('data.csv', 'r', encoding='utf-8-sig') as f:
    # 先读取第一行获取列名
    header = f.readline().strip().split(',')
    header = [h.strip() for h in header]
    print(f"列名: {header}")

    # 重置文件指针
    f.seek(0)
    reader = csv.DictReader(f)
    for row in reader:
        # 打印第一行数据用于调试
        if not courses:
            print(f"第一行数据: {row}")
        courses.append({
            'name': row[header[0]].strip(),
            'credit': row[header[1]].strip(),
            'score': row[header[2]].strip(),
            'semester': int(row[header[4]].strip()),
            'type': row[header[5]].strip()
        })

# 按学期分组
semesters = {
    1: "2022-2023学年 第1学期",
    2: "2022-2023学年 第2学期",
    3: "2023-2024学年 第1学期",
    4: "2023-2024学年 第2学期",
    5: "2024-2025学年 第1学期",
    6: "2025-2026学年 第2学期"
}

# 统计各课程类型的学分
credit_types = {
    '实践': 0.0,
    '英选': 0.0,
    '语选': 0.0,
    '专选': 0.0,
    '专必': 0.0,
    '学基': 0.0,
    '通必': 0.0,
    '通选': 0.0,
    '拓必': 0.0
}

# 统计总学分和每学期课程数
total_credits = 0
total_score = 0
semester_counts = {}

# 按学期排序课程
for s in [1, 2, 3, 4, 5, 6]:
    semester_courses = [c for c in courses if c['semester'] == s]
    semester_counts[s] = len(semester_courses)
    for c in semester_courses:
        credit = float(c['credit'])
        total_credits += credit
        credit_types[c['type']] = credit_types.get(c['type'], 0) + credit
        total_score += float(c['score']) * credit

# 计算平均成绩和绩点
avg_score = total_score / total_credits
# 简单的绩点计算（可以根据实际情况调整）
avg_gpa = avg_score / 10 - 5  # 简化计算
if avg_gpa < 0:
    avg_gpa = 0

print(f"总学分: {total_credits}")
print(f"平均成绩: {avg_score:.1f}")
print(f"平均绩点: {avg_gpa:.2f}")
print("\n各课程类型学分:")
for k, v in credit_types.items():
    if v > 0:
        print(f"  {k}: {v}")
print("\n各学期课程数:")
for s in [1, 2, 3, 4, 5, 6]:
    print(f"  学期{s}: {semester_counts[s]}门")

# 生成表格行
print("\n=== 生成Typst表格代码 ===\n")

for s in [1, 2, 3, 4, 5, 6]:
    semester_courses = [c for c in courses if c['semester'] == s]
    semester_name = semesters[s]
    print(f'table.cell(colspan: 6)[{semester_name}],')
    for c in semester_courses:
        name = c['name']
        # 处理特殊字符
        if '思想' in name or '毛泽东' in name:
            name = f'#text(size: 5.5pt)[{name}]'
        elif '大国三农' in name:
            name = f'#text(size: 5pt)[{name}]'
        print(f'      [{name}], [{c["type"]}], [{c["credit"]}], [{c["score"]}], [], [],')
    print()
