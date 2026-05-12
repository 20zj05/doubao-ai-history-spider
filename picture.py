# -*- coding: utf-8 -*-
import pandas as pd
import jieba
from wordcloud import WordCloud
from collections import Counter
import matplotlib.pyplot as plt

# ======================
# 1. 读取你的对话数据
# ======================
df = pd.read_csv("doubao_all_OK.csv", encoding="utf-8-sig")

# 把所有对话内容合并成一段文本
text = " ".join(df["内容"].astype(str))

# ======================
# 2. 中文分词 + 过滤无用词
# ======================
word_list = jieba.lcut(text)

# 过滤掉无意义的停用词（可自己添加）
stop_words = {
    "的", "是", "我", "你", "了", "在", "和", "就", "也", "都",
    "可以", "一个", "我们", "这个", "有", "不", "要", "会", "能",
    "吗", "吧", "呢", "啊", "什么", "怎么", "哪里", "这"
}

# 只保留长度≥2、不是停用词的有效词汇
filtered_words = [word for word in word_list if len(word) >= 2 and word not in stop_words]

# ======================
# 3. 词频统计（输出前20个高频词）
# ======================
word_count = Counter(filtered_words)
print("=" * 50)
print("📊 豆包对话高频词统计（前20名）")
print("=" * 50)
for word, count in word_count.most_common(20):
    print(f"{word}：{count} 次")

# ======================
# 4. 生成高清中文词云
# ======================
wc = WordCloud(
    font_path="C:/Windows/Fonts/simhei.ttf",  # 系统黑体，Windows通用
    background_color="white",                 # 白色背景
    width=1200,
    height=800,
    max_words=100,
    margin=2
).generate(" ".join(filtered_words))

# 保存词云图片
wc.to_file("豆包对话词云.png")
print("\n✅ 词云已保存：豆包对话词云.png")

# ======================
# 5. 显示词云图（可选）
# ======================
plt.figure(figsize=(12,8))
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.show()