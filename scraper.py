from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

URL = "https://www.amazon.de/gp/bestsellers/computers/429868031/"

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)
driver.get(URL)

wait = WebDriverWait(driver, 15)

# Wait for initial list to load
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".p13n-sc-uncoverable-faceout")))

# Scroll step-by-step to ensure lazy loading
SCROLL_PAUSE_TIME = 2
for _ in range(10):  # 반복 횟수는 필요에 따라 조정
    scroll_origin = ScrollOrigin.from_viewport(0, 0)
    ActionChains(driver).scroll_from_origin(scroll_origin, 0, 1000).perform()
    time.sleep(SCROLL_PAUSE_TIME)

# 수집: 각 제품 div에서 정보 추출
product_cards = driver.find_elements(By.CSS_SELECTOR, "div.p13n-sc-uncoverable-faceout")

print("\n📦 Amazon Bestseller (Computer) - Extracted Products\n" + "-"*60)
for i, card in enumerate(product_cards):
    try:
        title = card.find_element(By.CSS_SELECTOR, "._cDEzb_p13n-sc-css-line-clamp-3_g3dy1").text.strip()
        price = card.find_element(By.CSS_SELECTOR, ".p13n-sc-price").text.strip()
        print(f"{i+1:02d}. {title} | 💶 {price}")
    except Exception:
        continue  # 가격이 없거나 title이 없으면 무시

driver.quit()
