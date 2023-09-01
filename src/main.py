#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from listings import find_listings
from marketplace_message import send_message


import config

logger = config.get_logger(__name__)

def login_to_facebook(browser, email, password):
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


def send_message(browser, listing_url, message_text):
    browser.get(listing_url)

    # A wait time for the page to load
    sleep(5)

    message_button = browser.find_element(By.CSS_SELECTOR, '.message-button-selector')
    message_button.click()

    # A wait time for the message box to load
    sleep(5)

    message_input = browser.find_element(By.CSS_SELECTOR, '.message-input-selector')
    message_input.send_keys(message_text)
    message_input.send_keys(Keys.ENTER)

def main():
    # Initialize the browser
    browser = webdriver.Firefox()

    # Login to Facebook
    login_to_facebook(browser, config.EMAIL, config.PASSWORD)

    # Parameters for searching and messaging
    city = "seattle"
    price_limit = 1200
    with open("message.txt", "r") as f:
        message_text = f.read()

    # Find listings and send messages
    listings = find_listings(browser, price_limit, city)
    logger.info("Found %d listings", len(listings))

    for listing in listings:
        logger.info("Sending message to %s", listing)
        send_message(browser, listing, message_text)

    # Quit the browser after completing the tasks
    # browser.quit()

if __name__ == "__main__":
    main()
