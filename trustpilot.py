import requests
from bs4 import BeautifulSoup
import pandas as pd

Reviews = []
Ratings = []

for i in range(1, 36):  # Scrape the first page
    url = f"https://www.trustpilot.com/review/swiggy.com?page={i}"
    r = requests.get(url)

    soup = BeautifulSoup(r.text, "lxml")

    # Extract reviews
    review_elements = soup.find_all("p", class_="typography_body-l__v5JLj typography_appearance-default__t8iAq typography_color-black__wpn7m")
    
    for review in review_elements:
        review_text = review.text.strip()
        Reviews.append(review_text)

    # Extract ratings from img alt attribute
    rating_divs = soup.find_all("div", class_="star-rating_starRating__sdbkn star-rating_medium__Oj7C9")

    for div in rating_divs:
        img_tag = div.find("img")  # Find img inside the div
        if img_tag and 'alt' in img_tag.attrs:
            rating_text = img_tag["alt"]  # Extract text from alt attribute
            
            print(f"Extracted Rating Text: {rating_text}")  # Debugging line

            words = rating_text.split()
            if len(words) >= 3 and words[0] == "Rated":  # Ensure correct format
                try:
                    rating_number = int(words[1])  # Extract number
                    Ratings.append(rating_number)
                except ValueError:
                    print(f"Skipping invalid rating: {rating_text}")  # Handle unexpected values
            else:
                print(f"Skipping unexpected rating format: {rating_text}")

# Ensure both lists have the same length
min_length = min(len(Reviews), len(Ratings))
Reviews = Reviews[:min_length]
Ratings = Ratings[:min_length]

# Create a DataFrame
df = pd.DataFrame({"Review": Reviews, "Rating": Ratings})

# Display DataFrame
print(df.head(10))

# Save to CSV (optional)
df.to_csv("trustpilot_reviews.csv", index=False)
