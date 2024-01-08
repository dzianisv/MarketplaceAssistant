import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import utils
import config
from time import sleep
import datetime

logger = config.get_logger(__name__)

def send_message(browser, listing_url, message):
    browser.get(listing_url)
    utils.waitPageReady(browser)
    logger.info("Listing: %s", listing_url)

    for _ in range(3):
        try:
            browser.find_element(By.XPATH, "//span[text()='Message Again']")
            logger.info("✉️ `Message Again` button is located. It means we already sent message to the owner of this ad")
            return True
        except selenium.common.exceptions.NoSuchElementException:
            pass
        
        for element in browser.find_elements(By.XPATH, "//textarea[@placeholder='Send a private message…']"):
            try:
                element.clear()
                element.send_keys(message)
            except selenium.common.exceptions.ElementNotInteractableException:
                logger.debug("⚠️ Invalid textare item")

        try:
            send_button = browser.find_element(By.XPATH, "//span[text()='Send']")
            browser.execute_script("arguments[0].scrollIntoView(true); arguments[0].click();", send_button)
            browser.save_full_page_screenshot(f"message-{datetime.datetime.now().isoformat()}.png")
            break
        except selenium.common.exceptions.NoSuchElementException:
            logger.info("🧐 `Send` button is not located")
            continue
    else:
        logger.warning("⚠️ Failed to locate `Send` or `Message Again` buttons")
        return False

    logger.info("📤 Message sent")
    
    try:
        browser.find_element(By.XPATH, "//*[contains(text(), 'Something goes wrong')]")
        logger.warning("Failed to sena a message, probably we are blocked")
        return False
    except selenium.common.exceptions.NoSuchElementException:
        pass

    return True
