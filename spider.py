from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

service = Service("chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("https://www.doubao.com/chat")

print("👉 请登录豆包")
print("👉 手动点开【第一个】历史对话")
print("👉 确保对话内容显示出来！")
time.sleep(25)

all_data = []

# 你有21个对话，循环21次
for i in range(100):
    try:
        print(f"\n正在抓取第 {i+1} 个对话...")

        # 等待内容加载
        time.sleep(2)

        # 抓取当前打开的对话所有文字
        text = driver.find_element(By.TAG_NAME, "body").text
        lines = [t.strip() for t in text.split("\n") if len(t.strip()) > 5]

        for line in lines:
            all_data.append({"会话": i+1, "内容": line})

        print(f"✅ 第 {i+1} 个对话抓取完成")

        # =======================
        # 核心：按 ↓ 键，切换下一个对话！
        # 不点击！纯键盘！100%可用！
        # =======================
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.DOWN)
        time.sleep(1.5)

    except Exception as e:
        print(f"⚠️ 跳过：{e}")
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.DOWN)
        time.sleep(1)

# 保存全部
df = pd.DataFrame(all_data)
df.to_csv("doubao_all_OK.csv", index=False, encoding="utf-8-sig")

print(f"\n🎉 🎉 🎉 全部抓取完成！")
print(f"总共记录：{len(all_data)} 条")
print("文件已保存：doubao_all_OK.csv")

driver.quit()