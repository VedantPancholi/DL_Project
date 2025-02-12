import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Set up Selenium WebDriver
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(service=service, options=options)
url = "https://www.quora.com/What-is-your-review-of-Swiggy"
driver.get(url)
time.sleep(5)  # Allow initial load

# Scroll multiple times to load reviews
for _ in range(15):  # Scroll 15 times
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
    time.sleep(2)  # Give time for reviews to load

# Click all "Continue Reading" buttons
while True:
    try:
        button = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Continue Reading']"))
        )
        driver.execute_script("arguments[0].click();", button)
        time.sleep(2)  # Wait for full content to appear
    except:
        break  # Stop when no more "Continue Reading" buttons

# Extract reviews using the correct class
soup = BeautifulSoup(driver.page_source, "html.parser")
reviews = [
    div.get_text(strip=True)
    for div in soup.find_all("div", class_="q-box spacing_log_answer_content puppeteer_test_answer_content")
]

# Close WebDriver
driver.quit()

# Save reviews to CSV
df = pd.DataFrame(reviews, columns=["Review"])
df.to_csv("quora_reviews.csv", index=False, encoding="utf-8")

print(f"Scraping completed. {len(reviews)} reviews saved to 'quora_reviews.csv'")