import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager

options = Options()
options.add_argument("--headless")

service = Service(EdgeChromiumDriverManager().install())
driver = webdriver.Edge(service=service, options=options)

reviews_list = []
url_template = "https://www.flipkart.com/motorola-g35-5g-midnight-black-128-gb/product-reviews/itm015cbd184b0eb?pid=MOBH3YGPTSA4SZQF&lid=LSTMOBH3YGPTSA4SZQF0KIKVP&marketplace=FLIPKART&page={}"

sno = 1

for i in range(1, 30):
    driver.get(url_template.format(i))
    
    
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "ZmyHeo"))
        )
    except:
        print(f"Skipping page {i} due to timeout.")
        continue

    
    reviews = driver.find_elements(By.XPATH, '//div[@class="ZmyHeo"]/div/div')

    if not reviews:
        print(f"No reviews on page {i}. Stopping...")
        break

   
    for review in reviews:
        reviews_list.append({"S.No": sno, "Review": review.text.strip()})
        sno += 1

driver.quit()


df = pd.DataFrame(reviews_list)


df.to_csv('Product_Review.csv', index=False)
print("Reviews successfully saved to 'Product_Review.csv'")
# Plot sentiment distribution
df["Sentiment"].value_counts().plot(kind="bar", color=["green", "red", "blue"])
plt.title("Sentiment Distribution of Flipkart Reviews")
plt.xlabel("Sentiment")
plt.ylabel("Number of Reviews")
plt.show()
plt.savefig("sentiment_distribution.png")