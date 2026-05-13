from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# 启动
service = Service("chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("https://www.doubao.com/chat")
driver.maximize_window()

print("👉 请在 30 秒内登录豆包！登录完别动！")
time.sleep(30)

# ==============================================
# 【核心修复】一直等，直到左侧历史记录出现！
# ==============================================
print("⏳ 等待左侧会话列表加载...")
wait = WebDriverWait(driver, 20)

# 最稳的选择器：豆包左侧历史会话
items = wait.until(
    EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "div[class*='item'] div, div[class*='history']")
    )
)

total = len(items)
print(f"✅ 成功找到会话总数：{total}")
all_data = []

# ==============================================
# 开始逐个点击（JS 鼠标点击，真人速度）
# ==============================================
for i in range(total):
    try:
        # 每次重新获取
        time.sleep(1.5)
        current_items = driver.find_elements(By.CSS_SELECTOR, "div[class*='item'] div, div[class*='history']")
        if i >= len(current_items):
            break

        ele = current_items[i]

        # 滚动到视图 + 等待
        driver.execute_script("arguments[0].scrollIntoView(true);", ele)
        time.sleep(1)

        # JS 点击（和你手点 100% 一样）
        driver.execute_script("arguments[0].click();", ele)
        print(f"\n🖱️  已点击第 {i+1} 个对话")

        # 等内容加载
        time.sleep(3)

        # 抓内容
        text = driver.find_element(By.TAG_NAME, "body").text
        lines = [x.strip() for x in text.split("\n") if len(x.strip()) > 5]

        for line in lines:
            all_data.append({"会话": i+1, "内容": line})

        print(f"✅ 第 {i+1} 个对话抓取完成")

    except Exception as e:
        print(f"⚠️ 跳过：{str(e)[:60]}")
        continue

# 保存
df = pd.DataFrame(all_data)
df.to_csv("doubao.csv", index=False, encoding="utf-8-sig")

print("\n🎉 🎉 🎉 全部爬取完成！")
print(f"总共记录：{len(all_data)} 条")
driver.quit()