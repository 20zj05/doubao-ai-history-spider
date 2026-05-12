from selenium import webdriver
from selenium.webdriver.common.by import By  # 这次加上了！
from selenium.webdriver.chrome.service import Service
import time
import pandas as pd

# 启动浏览器
service = Service("chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("https://www.doubao.com/chat")

print("👉 请登录豆包 → 手动点开一个对话")
print("👉 点开后等消息加载出来，再等10秒！")
time.sleep(20)

# 直接抓取整个页面所有文字
all_text = driver.find_element(By.TAG_NAME, "body").text

# 清洗数据
lines = []
for line in all_text.split("\n"):
    line = line.strip()
    if len(line) > 5:  # 只保留有效对话
        lines.append(line)

# 保存CSV
df = pd.DataFrame({"对话内容": lines})
df.to_csv("doubao_ok.csv", index=False, encoding="utf-8-sig")

print(f"\n🎉 抓取成功！一共抓到 {len(lines)} 条记录")
print("📁 文件已保存：doubao_ok.csv")

driver.quit()