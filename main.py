import time
import pandas as pd
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException, SessionNotCreatedException
import logging
import random
from fake_useragent import UserAgent
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from selenium.webdriver.common.by import By


PRODUCT_URL_TEMPLATE = "https://www.flipkart.com/poco-c75-5g-silver-stardust-64-gb/product-reviews/itm8e3f17ac2e724?pid=MOBH74433ZER9U4P&lid=LSTMOBH74433ZER9U4PIUMZCQ&marketplace=FLIPKART&page={}"
MAX_PAGES_TO_SCRAPE = 10  
OUTPUT_CSV_FILE = 'Product_Review_with_Sentiment.csv'
LOG_FILE = 'scraper_log.log'


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)


sid_analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment_vader(text):
    
    if not isinstance(text, str):
        return 'Neutral' 
    vs = sid_analyzer.polarity_scores(text)
    if vs['compound'] >= 0.05:
        return 'Positive'
    elif vs['compound'] <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'


def get_flipkart_reviews(product_url_template, num_pages):
    
    reviews_data = []
    sno = 1

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument(f"user-agent={UserAgent().random}")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage") 
    options.add_argument("--window-size=1920,1080") 
    

    driver = None 

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        logging.info("WebDriver initialized in headless mode.")

    except SessionNotCreatedException as e:
        logging.critical(f"Failed to create WebDriver session. Please ensure Chrome is installed "
                         f"and compatible with the chromedriver version. Error: {e}")
        return [] 
    except Exception as e:
        logging.critical(f"An unexpected error occurred during WebDriver initialization: {e}", exc_info=True)
        return []

    try:
        for i in range(1, num_pages + 1):
            url = product_url_template.format(i)
            logging.info(f"Navigating to page {i}: {url}")
            driver.get(url)

            time.sleep(random.uniform(2, 5))

            try:
                
                WebDriverWait(driver, 20).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "ZmyHeo"))
                )
                logging.debug(f"Review containers found on page {i}.")
            except TimeoutException:
                logging.warning(f"Timeout waiting for reviews on page {i}. This might be the last page or content not loaded.")
                
                try:
                    no_reviews_element = driver.find_elements(By.XPATH, "//*[contains(text(), 'No reviews yet')]") # Example, check Flipkart's actual text
                    if no_reviews_element:
                        logging.info(f"Explicit 'No reviews yet' message found on page {i}. Stopping.")
                        break
                except:
                    pass 
                
                
                break 
            except Exception as e:
                logging.error(f"An unexpected error occurred while waiting for elements on page {i}: {e}")
                break

            
            reviews = driver.find_elements(By.XPATH, '//div[@class="ZmyHeo"]/div/div')
            
            if not reviews:
                logging.info(f"No reviews found (or no new reviews) on page {i}. Stopping.")
                break

            for review_element in reviews:
                full_review_text = ""
                try:
                    
                    read_more_button = review_element.find_element(By.XPATH, './/span[text()="READ MORE"]')
                    if read_more_button.is_displayed() and read_more_button.is_enabled():
                        read_more_button.click()
                        logging.debug("Clicked 'READ MORE' button.")
                        time.sleep(random.uniform(0.5, 1.5)) 
                except NoSuchElementException:
                    
                    pass 
                except Exception as e:
                    logging.warning(f"Error clicking 'READ MORE' for a review on page {i}: {e}")
                    
                
                full_review_text = review_element.text.strip()
                
                
                if full_review_text:
                    reviews_data.append({"S.No": sno, "Review": full_review_text})
                    sno += 1
                else:
                    logging.warning(f"Empty review text found on page {i} for S.No {sno}. Skipping.")

    except Exception as e:
        logging.critical(f"A critical error occurred during scraping loop: {e}", exc_info=True)
    finally:
        if driver: 
            driver.quit()
            logging.info("WebDriver session closed.")
    
    return reviews_data


if __name__ == "__main__":
    logging.info("Starting Flipkart Review Scraper...")

    scraped_reviews = get_flipkart_reviews(PRODUCT_URL_TEMPLATE, MAX_PAGES_TO_SCRAPE)

    if scraped_reviews:
        df = pd.DataFrame(scraped_reviews)
        logging.info(f"Total {len(df)} reviews scraped.")

       
        logging.info("Performing sentiment analysis...")
        df["Sentiment"] = df["Review"].apply(analyze_sentiment_vader)
        logging.info("Sentiment analysis complete.")

       
        df.to_csv(OUTPUT_CSV_FILE, index=False)
        logging.info(f"Reviews with sentiment successfully saved to '{OUTPUT_CSV_FILE}'")

        
        sentiment_counts = df["Sentiment"].value_counts()
        logging.info(f"Sentiment distribution: \n{sentiment_counts}")

        
        sentiment_colors = {
            "Positive": "green",
            "Negative": "red",
            "Neutral": "blue"
        }
        
        plot_colors = [sentiment_colors.get(s, 'gray') for s in sentiment_counts.index]

        
        plt.figure(figsize=(10, 7))
        sentiment_counts.plot(kind="bar", color=plot_colors)
        plt.title("Sentiment Distribution of Flipkart Reviews", fontsize=16)
        plt.xlabel("Sentiment", fontsize=14)
        plt.ylabel("Number of Reviews", fontsize=14)
        plt.xticks(rotation=0, fontsize=12)
        plt.yticks(fontsize=12)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig("sentiment_distribution_bar.png")
        logging.info("Bar chart saved as 'sentiment_distribution_bar.png'")
        plt.show()

    else:
        logging.warning("No reviews were scraped. CSV file not created and no plots generated.")

    logging.info("Scraping process finished.")