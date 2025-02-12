import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Set up Selenium WebDriver with optimized settings
options = Options()
options.add_argument("--headless")  # Run Chrome in headless mode
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-webgl")  # Prevent WebGL errors
options.add_argument("--log-level=3")  # Suppress unnecessary logs

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Lists to store reviews and ratings
Reviews = []
Ratings = []

# Loop through multiple pages
for i in range(1, 163):  
    url = f"https://www.mouthshut.com/websites/swiggy-reviews-925740914-page-{i}"
    driver.get(url)

    try:
        # Wait for reviews to load dynamically
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "review-article")))
    except:
        print(f"Skipping page {i} due to load failure.")
        continue

    # Extract review blocks
    review_blocks = driver.find_elements(By.XPATH, '//div[contains(@class, "row review-article")]')

    for block in review_blocks:
        try:
            # Extract review text
            review_div = block.find_element(By.XPATH, './/div[@class="more reviewdata"]')
            full_text = review_div.text.strip().replace("\n", " ")
            Reviews.append(full_text)
            
            # Extract rating (counting filled stars)
            rating_div = block.find_element(By.XPATH, './/div[@class="rating"]')
            rated_stars = len(rating_div.find_elements(By.XPATH, './/i[contains(@class, "icon-rating rated-star")]'))
            Ratings.append(rated_stars)
        except Exception as e:
            print(f"Error extracting data from a review block: {e}")
            continue  # Skip if elements are missing

# Close WebDriver
driver.quit()

# Convert to a DataFrame
df = pd.DataFrame({"Review": Reviews, "Rating": Ratings})

# Save to CSV
df.to_csv("swiggy_reviews_ratings.csv", index=False)

# Display DataFrame preview
print(df.head())
print(f"\nTotal Reviews Collected: {len(Reviews)}")
