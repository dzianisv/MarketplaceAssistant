import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
from time import sleep
import utils
import config


logger = config.get_logger(__name__)

def find_listings(browser, price_limit, city):
    # base_url = "https://www.facebook.com/marketplace"
    # url = f"{base_url}/{city}/search?query=rentals&exact=false"

    url = "https://www.facebook.com/marketplace/category/propertyrentals"
    browser.get(url)
    sleep(5)

    # Regex pattern to identify price-like strings
    price_pattern = r"\$\d{1,3}(,\d{3})*(\.\d{2})?"
    affordable_listings = []
    recent_len = -1

    while len(affordable_listings) > recent_len:
        recent_len = len(affordable_listings)
        # Find all <a> elements containing a <span> that looks like a price 
        a_elements = browser.find_elements(By.XPATH, "//a[.//span]")

        for a_element in a_elements:
            try:
                span_element = a_element.find_element(By.TAG_NAME, "span")
                price_text = span_element.text
                listing_link = a_element.get_attribute("href")

                if re.search(price_pattern, price_text):
                    # price could contain a discount price, in this case it will look like: '$550\n$600'
                    price_str = price_text.replace("$", "").replace(",", "").split('\n')[0]

                    if price_str == 'Free':
                        price = 0.0
                    else:
                        price = float(price_str)

                    if price <= price_limit:
                        affordable_listings.append(listing_link)
            except Exception as e:
                logger.error(f"Error processing a listing `{listing_link}: {e}")
            
        try:
            browser.find_element(By.XPATH, "//*[contains(text(), 'Results from outside your search')]")
            break
        except selenium.common.exceptions.NoSuchElementException:
            pass

        utils.scrollToBottom(browser)
        utils.wait(browser, 10)

    return affordable_listings
