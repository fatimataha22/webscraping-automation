from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time
import os
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Selenium options
options = Options()
options.add_argument("--headless")  # Enable headless mode for GitHub Actions
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

# Rotate User-Agent to prevent detection
ua = UserAgent()
options.add_argument(f"user-agent={ua.random}")
# Set up ChromeDriver using webdriver_manager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Define the target website (CoinMarketCap Bitcoin page)
URL = "https://coinmarketcap.com/currencies/bitcoin/"

def scrape_bitcoin_data():
    """Scrape Bitcoin details from CoinMarketCap."""
    driver.get(URL)
    time.sleep(7)  # Allow time for elements to load

    try:
        # Extract Bitcoin Price
        price = WebDriverWait(driver, 7).until(
            EC.presence_of_element_located((By.XPATH, '//span[@data-test="text-cdp-price-display"]'))
        ).text

        # Extract Market Cap
        market_cap = WebDriverWait(driver, 7).until(
            EC.presence_of_element_located(
                (By.XPATH, "//dt[.//div[contains(normalize-space(.), 'Market cap')]]/following-sibling::dd//span")
            )
        ).text

        # Extract 24h Trading Volume
        volume_24h = WebDriverWait(driver, 7).until(
            EC.presence_of_element_located(
                (By.XPATH, "//dt[.//div[contains(normalize-space(.),'Volume (24h')]]/following-sibling::dd//span")
            )
        ).text

        # Extract Circulating Supply
        circulating_supply = WebDriverWait(driver, 7).until(
            EC.presence_of_element_located(
                (By.XPATH, "//dt[.//div[contains(normalize-space(.),'Circulating supply')]]/following-sibling::dd//span")
            )
        ).text

        # Extract 24h Price Change
        price_change_24h = WebDriverWait(driver, 7).until(
            EC.presence_of_element_located((By.XPATH, "//p[contains(@class, 'change-text')]") )
        ).text

        # Extract Community Sentiment
        bullish_sentiment_elems = driver.find_elements(By.XPATH, "(//span[contains(@class,'ratio')])[1]")
        bearish_sentiment_elems = driver.find_elements(By.XPATH, "(//span[contains(@class,'ratio')])[2]")

        bullish = bullish_sentiment_elems[0].text if bullish_sentiment_elems else "N/A"
        bearish = bearish_sentiment_elems[0].text if bearish_sentiment_elems else "N/A"

        # Capture timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Store the data in a dictionary
        bitcoin_data = {
            "timestamp": timestamp,
            "price": price,
            "market_cap": market_cap,
            "volume_24h": volume_24h,
            "circulating_supply": circulating_supply,
            "price_change_24h": price_change_24h,
            "bullish_sentiment": bullish,
            "bearish_sentiment": bearish
        }

        return bitcoin_data

    except Exception as e:
        print("Error occurred:", e)
        return None

def save_to_csv(data):
    """Save scraped data to CSV quickly."""
    file_name = "optimized_bitcoin_hourly_data.csv"
    new_row = pd.DataFrame([data])
    new_row.to_csv(file_name, mode='a', header=not os.path.exists(file_name), index=False)

if __name__ == "__main__":
    print("Scraping Bitcoin Data...")
    scraped_data = scrape_bitcoin_data()

    if scraped_data:
        save_to_csv(scraped_data)
        print("Data saved to optimized_bitcoin_hourly_data.csv")
    else:
        print("Failed to scrape data.")

    driver.quit()