# -*- coding: utf-8 -*-
import pandas as pd
import jieba
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud

# ----------------------
# 1. 读取数据
# ----------------------
df = pd.read_csv("doubao.csv", encoding="utf-8-sig")
text = " ".join(df["内容"].astype(str))

# ----------------------
# 2. 分词 + 过滤无效词
# ----------------------
words = jieba.lcut(text)
stop_words = {"的", "是", "我", "你", "了", "在", "和", "就", "也", "都",
              "可以", "一个", "我们", "这个", "有", "不", "要", "会", "能",
              "吗", "吧", "呢", "啊", "什么", "怎么", "哪里", "这", "那"}

valid_words = [w for w in words if len(w) >= 2 and w not in stop_words]

# ----------------------
# 3. 统计高频词 TOP20
# ----------------------
word_count = Counter(valid_words)
top20 = word_count.most_common(20)
words_20 = [w[0] for w in top20]
counts_20 = [w[1] for w in top20]

print("="*50)
print("高频词 TOP20")
print("="*50)
for w, c in top20:
    print(f"{w}: {c}")

# ----------------------
# 4. 设置中文字体
# ----------------------
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# ----------------------
# 图1：高频词柱状图
# ----------------------
plt.figure(figsize=(12, 6))
plt.bar(words_20, counts_20, color="#4285F4")
plt.title("高频词统计 TOP20", fontsize=16)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("高频词柱状图.png")

# ----------------------
# 图2：高频词饼图
# ----------------------
top10_words, top10_counts = zip(*word_count.most_common(10))
plt.figure(figsize=(8, 8))
plt.pie(top10_counts, labels=top10_words, autopct="%1.1f%%", startangle=90)
plt.title("高频词占比饼图 TOP10", fontsize=16)
plt.tight_layout()
plt.savefig("高频词占比饼图.png")

# ----------------------
# 图3：词云图
# ----------------------
wc = WordCloud(
    font_path="C:/Windows/Fonts/simhei.ttf",
    background_color="white",
    width=1200, height=600
)
wc.generate(" ".join(valid_words))
wc.to_file("对话词云图.png")


# ----------------------
# 完成提示
# ----------------------
print("\n所有图表已生成完成！")
print("1. 对话词云图.png")
print("2. 高频词柱状图.png")
print("3. 高频词占比饼图.png")


plt.show()