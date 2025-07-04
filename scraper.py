from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
import time

URL = "https://www.amazon.de/-/en/gp/bestsellers/computers/429868031/"

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)
driver.get(URL)

# Scroll to bottom using WheelInput
last_height = driver.execute_script("return document.body.scrollHeight")
SCROLL_PAUSE_TIME = 2

while True:
    scroll_origin = ScrollOrigin.from_viewport(0, 0)
    ActionChains(driver)\
        .scroll_from_origin(scroll_origin, 0, 1000)\
        .perform()
    
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Wait a bit for last products to render
time.sleep(2)

# Extract product titles and prices
titles = driver.find_elements(By.CSS_SELECTOR, "div.p13n-sc-truncate, span.zg-item > div > span > a > div")
prices = driver.find_elements(By.CSS_SELECTOR, "span.p13n-sc-price")

# Terminal log: Print all entries
print("\n📦 Amazon Bestseller (Computer) - Extracted Products\n" + "-"*60)
for i in range(min(len(titles), len(prices))):
    title_text = titles[i].text.strip()
    price_text = prices[i].text.strip()
    print(f"{i+1:02d}. {title_text} | 💶 {price_text}")

driver.quit()
