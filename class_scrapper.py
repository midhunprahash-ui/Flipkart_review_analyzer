import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# Run in headless mode for faster performance
options = Options()
options.add_argument("--headless")

# Setup WebDriver for Edge
service = Service(EdgeChromiumDriverManager().install())
driver = webdriver.Edge(service=service, options=options)

# Flipkart product URLs to check
urls = [
    "https://www.flipkart.com/realme-xt-pearl-blue-64-gb/product-reviews/itm731360fdbd273?pid=MOBFJYBE9FHXFEFJ&lid=LSTMOBFJYBE9FHXFEFJXVJLXQ&marketplace=FLIPKART&page=1",
    "https://www.flipkart.com/apple-iphone-14-blue-128-gb/product-reviews/itmdb32e8757072d?pid=MOBGHWFHXPC3NFFY&lid=LSTMOBGHWFHXPC3NFFYZXMTAG&marketplace=FLIPKART&page=1",
    "https://www.flipkart.com/samsung-galaxy-m14-5g-smoky-teal-128-gb/product-reviews/itm7e22bd9e6a183?pid=MOBGZWM7JFGVQ9JX&lid=LSTMOBGZWM7JFGVQ9JXFGMYW0&marketplace=FLIPKART&page=1"
]

# Set to store unique class names
unique_classes = set()

for url in urls:
    driver.get(url)

    # Wait until the reviews section loads
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div"))
        )
    except:
        print(f"Skipping URL due to timeout: {url}")
        continue

    # Get all div elements to check for class names
    all_divs = driver.find_elements(By.TAG_NAME, "div")

    # Extract class names from all divs
    for div in all_divs:
        class_name = div.get_attribute("class")
        if class_name:
            unique_classes.update(class_name.split())

driver.quit()

# Save class names to a CSV file
df = pd.DataFrame({"Class Name": list(unique_classes)})
df.to_csv("flipkart_review_classes.csv", index=False)
print("Class names successfully saved to 'flipkart_review_classes.csv'")
# Print the unique class names
print("Unique class names found:")
for class_name in unique_classes:
    print(class_name)
# Plot sentiment distribution
df["Sentiment"].value_counts().plot(kind="bar", color=["green", "red", "blue"])
plt.title("Sentiment Distribution of Flipkart Reviews")
plt.xlabel("Sentiment")
plt.ylabel("Number of Reviews")
plt.show()
plt.savefig("sentiment_distribution.png")
