import jieba
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd

df = pd.read_csv("doubao_chat.csv")
text = " ".join(df["content"].astype(str))

# 分词+过滤
words = jieba.lcut(text)
stop = {"的","是","我","你","了","在","就","也","都","和","什么","怎么"}
fw = [w for w in words if w not in stop and len(w)>1]

# 词频
cnt = Counter(fw).most_common(20)

# 生成词云
plt.rcParams["font.sans-serif"] = ["SimHei"]
wc = WordCloud(font_path="simhei.ttf", background_color="white", width=800, height=400)
wc.generate_from_frequencies(dict(cnt))

plt.figure(figsize=(10,5))
plt.imshow(wc)
plt.axis("off")
plt.savefig("doubao_wordcloud.png")
plt.show()
print("词云已生成完成")