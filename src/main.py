#!/usr/bin/env python3

import selenium
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from listings import find_listings
from marketplace_message import send_message
import utils

import config

logger = config.get_logger(__name__)


def login_to_facebook(browser, email, password):
    browser.get("https://www.facebook.com/")
    try:
        # Input email
        email_element = browser.find_element(By.CSS_SELECTOR, 'input[name="email"]')
        email_element.send_keys(email)

        # Input password
        password_element = browser.find_element(By.CSS_SELECTOR, 'input[name="pass"]')
        password_element.send_keys(password)
        password_element.send_keys(Keys.ENTER)
    except selenium.common.exceptions.NoSuchElementException:
        logger.info(
            "`email` and `pass` fields are not found, looks like we are logged in..."
        )

    logger.debug("waiting for `Marketplace` menu item")
    utils.waitFor(browser, (By.XPATH, "//span[text()='Marketplace']"))


def main():
    # Initialize the browse
    profile_path = "FacebookAssistantState"
    options = selenium.webdriver.firefox.options.Options()
    options.add_argument("--profile")
    options.add_argument(profile_path)
    browser = webdriver.Firefox(options=options)

    try:
        # Login to Facebook
        login_to_facebook(browser, config.EMAIL, config.PASSWORD)

        # Parameters for searching and messaging
        # seattle, miami, sanjuan
        city = 'sanjuan'
        price_limit = 1200

        # Find listings and send messages
        listings = find_listings(browser, price_limit, city)
        logger.info("Found %d listings", len(listings))

        for listing in listings:
            if not send_message(browser, listing, config.MESSAGE):
                logger.error("Failed to send a message")
                break
    finally:
        # Quit the browser after completing the tasks
        # browser.quit()
        pass


if __name__ == "__main__":
    main()
