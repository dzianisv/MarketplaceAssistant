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
    logger.info("Listing: %s", listing_url)

    element = utils.wait_for(browser, (By.XPATH, "//span[text()='Message Again']"), (By.XPATH, "//span[text()='Message']"))
    if 'Message Again' in element.get_attribute('innerHTML'):
        logger.info("✉️ `Message Again` button is located. It means we already sent message to the owner of this ad")
        return True
    else:
        ActionChains(browser).move_to_element(element).click().perform()
    
    # type in message
    element = WebDriverWait(browser, 20).until(
        EC.visibility_of_element_located((
            By.XPATH, 
            "//span[contains(text(), 'Please type your message to the seller')]/following-sibling::textarea"
    )))
    element.clear()
    element.send_keys(message)
    # ActionChains(browser).scroll_to_element(element).click(element).send_keys(message).perform()


    # click "Send message" button
    element = browser.find_element(By.XPATH, "//span[text()='Send message']") 
    element.click()
    
    # wait for a message delivery
    sleep(10)
    browser.save_full_page_screenshot(f"message-{datetime.datetime.now().isoformat()}.png")
    logger.info("📤 Message sent")

    try:
        browser.find_element(By.XPATH, "//*[contains(text(), 'Something goes wrong')]")
        logger.warning("Failed to sena a message, probably we are blocked")
        return False
    except selenium.common.exceptions.NoSuchElementException:
        pass

    return True
