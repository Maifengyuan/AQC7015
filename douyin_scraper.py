
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# 配置 Chrome 驱动
chrome_options = Options()
chrome_options.add_argument("--headless")  # 如果你希望 Chrome 在后台运行

# 替换为你的 Chrome 驱动路径
service = Service(executable_path='/path/to/chromedriver')
driver = webdriver.Chrome(service=service, options=chrome_options)

# 打开抖音网页
driver.get("https://www.douyin.com/")

# 等待页面加载
time.sleep(3)

# 搜索指定关键词
search_box = driver.find_element(By.XPATH, '//input[@placeholder="搜索"]')
search_query = "你想要搜索的关键词"  # 替换为你的搜索关键词
search_box.send_keys(search_query)
search_box.send_keys(Keys.RETURN)

# 等待搜索结果加载
time.sleep(5)

# 初始化数据列表
titles = []
descriptions = []
tags = []

# 获取搜索结果
videos = driver.find_elements(By.XPATH, '//div[@class="your_video_selector"]')  # 替换为实际的搜索结果定位器

for video in videos:
    try:
        title = video.find_element(By.XPATH, './/h1').text  # 替换为标题的定位器
        description = video.find_element(By.XPATH, './/p').text  # 替换为简介的定位器
        tag_elements = video.find_elements(By.XPATH, './/span[@class="your_tag_selector"]')  # 替换为标签的定位器
        video_tags = [tag.text for tag in tag_elements]
        
        titles.append(title)
        descriptions.append(description)
        tags.append(", ".join(video_tags))
    except Exception as e:
        print(f"Error extracting data from video: {e}")

# 关闭浏览器
driver.quit()

# 创建 DataFrame 并导出到 Excel
df = pd.DataFrame({
    "Title": titles,
    "Description": descriptions,
    "Tags": tags
})

df.to_excel("douyin_videos.xlsx", index=False)

print("Data exported to douyin_videos.xlsx")
