import sys
sys.stdout.reconfigure(encoding='utf-8')  # ✅ Fix UnicodeEncodeError

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

# ✅ Set up Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  
driver = webdriver.Chrome(options=options)

# ✅ Base URL
base_url = "https://www.ambitionbox.com/reviews/swiggy-reviews?page="

# ✅ Initialize list to store all reviews
all_reviews = []

# ✅ Loop through all 7 pages
for page in range(31,43):
    url = base_url + str(page)
    driver.get(url)
    
    # ✅ Wait for reviews to load
    wait = WebDriverWait(driver, 15)
    time.sleep(3)  

    # ✅ Click 'Read More' buttons
    while True:
        try:
            read_more_buttons = driver.find_elements(By.XPATH, "//a[contains(@class, 'read-more')]")
            if not read_more_buttons:
                break
            for button in read_more_buttons:
                driver.execute_script("arguments[0].click();", button)
                time.sleep(1)  
        except:
            break

    # ✅ Extract page source after clicking 'Read More'
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # ✅ Extract reviews
    for review_div in soup.find_all("p", class_="body-medium overflow-wrap"):
        review_text = review_div.get_text(strip=True)
        all_reviews.append(review_text)

    print(f"✔ Scraped page {page}")  # ✅ Changed emoji to avoid encoding issues

# ✅ Close browser
driver.quit()

# ✅ Convert reviews to DataFrame
df = pd.DataFrame(all_reviews, columns=["Review"])

# ✅ Save to CSV
csv_filename = "swiggy_reviews_all_pages_31_42.csv"
df.to_csv(csv_filename, index=False, encoding="utf-8")

print(f"✔ Scraped {len(all_reviews)} reviews from all pages and saved to '{csv_filename}'")