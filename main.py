import pandas as pd

try:
    df = pd.read_csv('data.csv')
except FileNotFoundError:
    print("错误：找不到 data.csv 文件。")
    exit()

df.columns = df.columns.str.strip()
df['课程性质'] = df['课程性质'].str.strip()

def get_gp(score):
    gp = (score / 10) - 5
    return gp if gp >= 1 else 0

df['绩点'] = df['分数分'].apply(get_gp)
df['加权分数'] = df['农牧学分'] * df['分数分']
df['加权绩点'] = df['农牧学分'] * df['绩点']

total_credits = df['农牧学分'].sum()
avg_score = df['加权分数'].sum() / total_credits if total_credits > 0 else 0
avg_gpa = df['加权绩点'].sum() / total_credits if total_credits > 0 else 0

category_map = df.groupby('课程性质')['农牧学分'].sum().to_dict()

def get_c(key):
    return category_map.get(key, category_map.get(key.replace('课', ''), 0.0))

cat_data = {
    "实践": get_c("实践课"),
    "英选": get_c("英选课"),
    "语选": get_c("语选课"),
    "专选": get_c("专选课"),
    "专必": get_c("专必课"),
    "学基": get_c("学基课"),
    "通必": get_c("通必课"),
    "通选": get_c("通选课"),
    "拓必": get_c("拓必课"),
}

typst_output = f"""
#table(
  columns: (4fr, 1fr, 1fr),
  align: center + horizon,
  stroke: 0.5pt,
  rows: 1.4em,

  table.cell[毕业设计(论文)题目：], [平均成绩], [{avg_score:.1f}],
  table.cell[], [平均绩点], [{avg_gpa:.2f}],
)
#table(
  columns: (3fr, 3fr, 3fr) + (2fr,) * 9,
  align: center + horizon,
  stroke: 0.5pt,
  rows: 1.4em,

  [毕业应取得总学分], [已获得总学分], table.cell(rowspan: 2)[其中\\ 包括],
  [实践课], [英选课], [语选课], [专选课], [专必课], [学基课], [通必课], [通选课], [拓必课],

  [170], [{total_credits:.1f}],
  [{cat_data['实践']:.1f}], [{cat_data['英选']:.1f}], [{cat_data['语选']:.1f}], [{cat_data['专选']:.1f}], [{cat_data['专必']:.1f}], [{cat_data['学基']:.1f}], [{cat_data['通必']:.1f}], [{cat_data['通选']:.1f}], [{cat_data['拓必']:.1f}],
)
"""

print(typst_output)