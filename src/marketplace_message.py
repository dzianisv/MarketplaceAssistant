import selenium
from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
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
        
        try:
            send_message_button = browser.find_element(By.XPATH, "//span[text()='Message']")
            ActionChains(browser).click(send_message_button).perform()
            sleep(3)
            
            element = browser.find_element(By.XPATH, "//span[contains(text(), 'Please type your message to the seller')]/following-sibling::textarea")
            element.clear()
            ActionChains(browser).click(element).send_keys(message).perform()
        
            element = browser.find_element(By.XPATH, "//span[text()='Send message']")   
            ActionChains(browser).click(element).perform()
                
            sleep(10)
            browser.save_full_page_screenshot(f"message-{datetime.datetime.now().isoformat()}.png")
            break
        except selenium.common.exceptions.NoSuchElementException as e:
            logger.warning(f"🧐 Failed to locate message dialog controls: {e}")
            continue
    else:
        return False

    logger.info("📤 Message sent")
    try:
        browser.find_element(By.XPATH, "//*[contains(text(), 'Something goes wrong')]")
        logger.warning("Failed to sena a message, probably we are blocked")
        return False
    except selenium.common.exceptions.NoSuchElementException:
        pass

    return True
