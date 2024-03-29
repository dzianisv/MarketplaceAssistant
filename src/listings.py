import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re
from time import sleep
import utils
import config


logger = config.get_logger(__name__)


def endOfListings(browser):
    try:
        browser.find_element(By.XPATH, "//*[contains(text(), 'Results from outside your search')]")
        return True
    except selenium.common.exceptions.NoSuchElementException:
        return False

def find_listings(browser, prices, city):
    # base_url = "https://www.facebook.com/marketplace"
    # url = f"{base_url}/{city}/search?query=rentals&exact=false"

    url = "https://www.facebook.com/marketplace/category/propertyrentals"
    browser.get(url)

    min_input = utils.wait_for(browser, (By.XPATH, "//input[@placeholder='Min']"))
    min_input.send_keys(str(prices[0]))
    min_input.send_keys(Keys.ENTER)

    max_input = utils.wait_for(browser, (By.XPATH, "//input[@placeholder='Max']"))
    max_input.send_keys(str(prices[1]))
    max_input.send_keys(Keys.ENTER)

    # Regex pattern to identify price-like strings
    price_pattern = r"\$\d{1,3}(,\d{3})*(\.\d{2})?"
    affordable_listings = set()
    recent_len = -1


    for i in range(30):
        if endOfListings(browser):
            break
        logger.debug("Scrolling to bottom of page, iteration %d", i)
        utils.scrollToBottom(browser)
        utils.wait(browser, 3)
        
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

                if price >= prices[0] and price <= prices[1]:
                    affordable_listings.add(listing_link)
                    logger.debug("Added listing %f %s", price, listing_link)

        except Exception as e:
            logger.error(f"Error processing a listing `{listing_link}: {e}")
        
    return list(affordable_listings)
