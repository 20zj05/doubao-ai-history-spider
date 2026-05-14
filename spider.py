from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# 启动浏览器
service = Service("chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("https://www.doubao.com/chat")
driver.maximize_window()

print("👉 请登录豆包")
print("👉 手动点开【任意一个历史对话】")
print("👉 点开后别动，等待程序自动抓取！")
time.sleep(30)  # 给你足够时间操作
print("✅程序开启抓取")

all_data = []
total_catch = 25  # 最多抓25条，足够你用

# ==============================
# 从你点开的对话开始，自动往下遍历
# 纯键盘 ↓ 操作，绝不乱点！
# ==============================
for i in range(total_catch):
    try:
        print(f"\n正在抓取第 {i + 1} 个对话...")

        # 等待内容加载
        time.sleep(2)

        # 抓取当前对话所有文字
        text = driver.find_element(By.TAG_NAME, "body").text
        lines = [x.strip() for x in text.split("\n") if len(x.strip()) > 5]

        for line in lines:
            all_data.append({
                "会话": i + 1,
                "内容": line
            })

        print(f"✅ 第 {i + 1} 个对话抓取完成")

        # ==========================
        # 核心：按 ↓ 键，切换到【下一个历史对话】
        # 只在历史记录里切换，不会跑到菜单！
        # ==========================
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.DOWN)
        time.sleep(1.5)

    except Exception as e:
        print(f"⚠️ 已到最后一条或出错，结束抓取")
        break

# 保存所有历史对话
df = pd.DataFrame(all_data)
df.to_csv("doubao.csv", index=False, encoding="utf-8-sig")

print("\n🎉 抓取完成！所有历史对话已保存！")
print(f"总记录数：{len(all_data)}")
driver.quit()