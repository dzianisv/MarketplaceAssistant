import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import utils
import config

logger = config.get_logger(__name__)

def send_message(browser, listing_url, message):
    browser.get(listing_url)
    utils.waitPageReady(browser)
    logger.info("Opened ad %s", listing_url)

    while True:
        try:
            browser.find_element(By.XPATH, "//span[text()='Message Again']")
            return True
        except selenium.common.exceptions.NoSuchElementException:
            logger.debug("✉️ `Message Again` button is located. It means we already sent message to the owner of this ad")

        for element in browser.find_elements(By.XPATH, "//textarea[contains(text(), 'this available?')]"):
            try:
                element.clear()  # Clear the default text.
                element.send_keys(message)
            except selenium.common.exceptions.ElementNotInteractableException as e:
                continue
        
        try:
            # Find the Send button and click it.
            send_button = browser.find_element(By.XPATH, "//span[text()='Send']")
            # Click the element with JavaScript
            browser.execute_script("arguments[0].scrollIntoView(true); arguments[0].click();", send_button)
            break
        except selenium.common.exceptions.NoSuchElementException:
            logger.debug("🧐 `Send` button is not located")
            continue

    utils.wait(driver,60)
    logger.info("📤 Message sent")

