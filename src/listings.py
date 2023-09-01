from selenium import webdriver
from selenium.webdriver.common.by import By
import re
from time import sleep

def find_listings(browser, price_limit, city):
    base_url = "https://www.facebook.com/marketplace"
    city_url = f"{base_url}/{city}/search?query=rentals&exact=false"
    browser.get(city_url)

    # Allow some time for listings to load
    sleep(5)

    # Regex pattern to identify price-like strings
    price_pattern = r"\$\d{1,3}(,\d{3})*(\.\d{2})?"
    affordable_listings = []

    # Find all <a> elements containing a <span> that looks like a price
    a_elements = browser.find_elements(By.XPATH, "//a[.//span]")

    for a_element in a_elements:
        try:
            span_element = a_element.find_element(By.TAG_NAME, 'span')
            price_text = span_element.text
            if re.search(price_pattern, price_text):
                price = float(price_text.replace('$', '').replace(',', ''))

                if price <= price_limit:
                    listing_link = a_element.get_attribute('href')
                    affordable_listings.append(listing_link)
        except Exception as e:
            print(f"Error processing a listing: {e}")

    return affordable_listings

