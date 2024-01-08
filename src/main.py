#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from listings import find_listings
from marketplace_message import send_message

import pickle
import os
import config

logger = config.get_logger(__name__)


COOKIES_FILE="fbAssistantCookies.pkl"

def save_cookies(driver):
    with open(COOKIES_FILE, "wb") as fd:
        pickle.dump(driver.get_cookies(), fd)

def load_coockies(driver):
    if not os.path.exists(COOKIES_FILE):
        return False

    with open(COOKIES_FILE, "rb") as fd:
        cookies = pickle.load(fd)
        for cookie in cookies:
            driver.add_cookie(cookie)
            return True

def login_to_facebook(browser, email, password):
    load_coockies(browser)

    browser.get('https://www.facebook.com/')

    # Input email
    email_element = browser.find_element(By.CSS_SELECTOR, 'input[name="email"]')
    email_element.send_keys(email)

    # Input password
    password_element = browser.find_element(By.CSS_SELECTOR, 'input[name="pass"]')
    password_element.send_keys(password)
    password_element.send_keys(Keys.ENTER)

    # Give some time for the login to process
    sleep(5)
    save_cookies(browser)


def main():
    # Initialize the browser
    browser = webdriver.Firefox()

    # Login to Facebook
    login_to_facebook(browser, config.EMAIL, config.PASSWORD)

    # Parameters for searching and messaging
    city = "miami"
    price_limit = 1200


    # Find listings and send messages
    listings = find_listings(browser, price_limit, city)
    logger.info("Found %d listings", len(listings))

    for listing in listings:
        logger.info("Sending message to %s", listing)
        send_message(browser, listing, config.MESSAGE)

    # Quit the browser after completing the tasks
    # browser.quit()

if __name__ == "__main__":
    main()
